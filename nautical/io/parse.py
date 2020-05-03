from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from pykml import parser
from ..noaa.NOAAData import NOAAData, CombinedNOAAData
from ..location.point import Point
from re import sub
from ..error import NauticalError
from . import DEFAULT_BUOY_WAVE_TEXT_SEARCH, SWELL_DATA_TEXT_SEARCH, PREVIOUS_OBSERVATION_SEARCH


def get_buoys_information(only_wave_data: bool = False):
    """
    NOAA is kind enough to provide all of names, ids, and other information about ALL of their known buoys
    in a kml document hosted at the link provided.

    https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml

    Let's read through this document and parse the buoy information to determine their id and location.
    The ID can be used to provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys. NOTE: the SHIP ID may not be able to be looked up. The coordinates are used aas general information
    to determine distance from other points, or for display purposes.

    NOTE: we could download the kml and pass in the data file, but some of the locations and information of
    the buoys is updated a half hourly rate, so we will attempt to read the live data

    All Buoy information that is read in as a set of coordinates with a buoy name, will be saved and stored.

    :param: only_wave_data - bool to tell us that we only want buoys that contain wave data
    :return: dictionary containing all buoy information where the key is the ID and the value is the Point()
    """
    buoys = {}

    """
    This is the ONLY known location of the kml file, this file contains the link to the 
    next kml file that contains all of the information we need!
    """
    url = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"

    try:
        fileobject = urlopen(url)
    except URLError:
        return buoys

    root = parser.parse(fileobject).getroot()

    """ 
    Grab the REAL link to the kml document we are really after
    """
    real_kml = root.Document.NetworkLink.Link.href

    if real_kml:
        real_fileobject = urlopen(str(real_kml))
        real_root = parser.parse(real_fileobject).getroot()

        """ 
        Traverse the KML markup 

        Document
        --- Folder
            --- Placemark
                --- DATA (name, coordinates, other)
        """
        for folder in real_root.Document.Folder:

            for subfolder in folder.Folder:

                for pm in subfolder.Placemark:

                    description = str(pm.description)

                    if (only_wave_data and 'Wave' in description) or not only_wave_data:
                        """
                        Point.coordinates are in the format <LON, LAT, ALT>
                        NOTE: We could also search for LookAT and search further for, longitude, latitude, or altitude
                        """
                        p = Point()
                        p.parse(str(pm.Point.coordinates))
                        buoys[str(pm.name)] = p

    if not buoys:
        raise NauticalError("no buoy information found")

    return buoys


def buoy_workup(buoy):
    """
    Provide a full workup for a specific buoy. If the buoy is nNone or it cannot be found
    then the data returned will be considered invalid as None

    NOTE: while the other function do NOT hve partial data, we may fill out the
    CombinedNOAAData partially

    :param buoy: id of the buoy to do a workup on
    :return: CombinedNOAAData if successful else None
    """
    if buoy is not None:
        url = get_noaa_forecast_url(buoy)

        soup = get_url_source(url)

        data = CombinedNOAAData()

        current_buoy_data = NOAAData()

        get_current_data(
            soup,
            search=DEFAULT_BUOY_WAVE_TEXT_SEARCH.format(buoy),
            data=current_buoy_data
        )

        get_current_data(
            soup,
            search=SWELL_DATA_TEXT_SEARCH,
            data=current_buoy_data
        )

        # print(current_buoy_data)

        data.past_data = get_past_data(soup)

        return data

    else:
        return None


def get_noaa_forecast_url(buoy):
    """
    NOAA is kind enough to post all of their data from their buoys at the same url ONLY requiring
    the id of buoy to change at the end of the link.

    https://www.ndbc.noaa.gov/station_page.php?station=

    this function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    NOTE: this does not check to ensure that this is a valid url.

    The next step(s) would be to pass this url and buoy value to several other functions for forecast data.
    get_current_data(search_url, id)
    get_detailed_wave_summary(search_url)
    get_swell_data(search_url)
    get_wave_data(search_url)

    :param buoy: id of the buoy
    :return: if buoy is not empty , return the full url, otherwise return nothing
    """
    if buoy:
        return "https://www.ndbc.noaa.gov/station_page.php?station={}".format(buoy)
    else:
        raise NauticalError("no buoy id provided")


def get_url_source(url_name):
    """
    If you already know the url_name or if you have run through the get_noaa_forecast_url(), then you can
    send in the url here. NOTE: we make no assumptions about the validity of the url and any data that it
    may contain.

    Get the source information for the url and place the information into a BeautifulSoup object, so that we
    can do any lookups of the data that we need.

    :param url_name: name of the url to search for
    :return: BeautifulSoup Object on success otherwise none
    """
    try:
        open_url = urlopen(url_name)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    except (ValueError, HTTPError):
        raise NauticalError("failed to create beautiful soup object")


def get_current_data(soup, **kwargs):
    """
    Search the beautiful soup object for a TABLE containing the search string. The function will
    grab the data from the table and create a NOAAData object and return the data
    :param soup: beautiful soup object generated from the get_url_source()
    :param search: text to search for in the soup object. The text MUST be an exact match as this is
    a possible limitation of beautiful soup searching
    :return: NOAAData object if successful otherwise NONE
    """

    search = kwargs.get("search", None)
    data = kwargs.get("data", NOAAData())

    if not search:
        return

    if isinstance(soup, BeautifulSoup):

        try:
            table = soup.find(text=search).findParent("table")

            for i, row in enumerate(table.findAll('tr')):

                # the first table is another table and it is no use to use -- skipping
                if i >= 1:
                    cells = row.findAll('td')

                    if cells:

                        key_data = cells[1].next.split()
                        key = sub('[():]', '', key_data[len(key_data) - 1]).lower()
                        value = cells[2].next.split()[0]
                        # print("{} = {}".format(key, value))

                        data(var=key, value=value)

        except Exception:
            raise NauticalError("table lookup failed")


def get_past_data(soup):
    """
    Get a list of all swell data from the past.
    :param soup: beautiful soup object generated from the get_url_source()
    :return: list of swell data
    """

    past_data = []
    if isinstance(soup, BeautifulSoup):
        try:

            # Get a list of all tables of the type dataTable, we know that is what
            # type of xml tag we need information from
            tables = soup.findAll(
                name="table",
                attrs={"class": "dataTable"}
            )

            for table in tables:

                # Let's only use the tables whose information is in a table
                # call Previous Observations
                if str(table.find(
                    name="caption",
                    attrs={"class": "dataHeader"}
                ).next) in PREVIOUS_OBSERVATION_SEARCH:

                    # find the variable names for each of the noaa data points
                    header_info = table.findAll(
                        name="th",
                        attrs={"class": "dataHeader"}
                    )
                    noaa_var_names = [str(x.next).lower() for x in header_info]


                    # find all of the rows of this table, then determine if the number
                    # of cells in the row matches the number of variables we just set, if
                    # so then this is the data set that we are looking for

                    for table_row in table.findAll("tr"):

                        cells = table_row.findAll("td")

                        if len(cells) == len(noaa_var_names):

                            for i, cell in enumerate(cells):
                                print("{} = {}".format(noaa_var_names[i], "".join(str(cell.next).split())))
                    #
                    #
                    # print(noaa_var_names)

            return

            tables = soup.findAll("table", {"class": "dataTable"})

            for table in tables:

                # list of header information from the table
                headers = []

                print(table.findAll("th", {"class": "dataHeader"}))
                return


                for row in table.findAll("tr"):

                    print("row = ", row)

                    # grab the header information so we can compare it to each row of the table
                    header_info = row.findAll("th", {"class": "dataHeader"})

                    # print(header_info)

                    headers = [str(x.next).lower() for x in header_info]
                    # print("Boom: ", headers)
                    #
                    # for info in header_info:
                    #
                    #     print(info.next)
                    #     headers.append(str(info.next).lower())

                    # Get all of the information in the table that is NOT part of the header
                    cells = row.findAll("td")

                    if len(cells) == len(headers) and len(cells) > 0:

                        # Header and length of the rows matched - we have a proper amount of data to store

                        nd = NOAAData()

                        for i in range(0, len(cells)):

                            value = "".join(str(cells[i].next).split())

                            # for some reason NOAA has added - for data without entries
                            if value is not None and value != "-":
                                setattr(nd, headers[i], value)

                        past_data.append(nd)
        except Exception:
            raise NauticalError("table lookup failed")

    return past_data
