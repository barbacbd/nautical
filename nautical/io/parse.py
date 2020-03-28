from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from pykml import parser
from ..noaa.NOAAData import NOAAData, CombinedNOAAData
from ..location.point import Point
from re import sub
from ..error import NauticalError
from . import _BuoyDataPositions, _BuoyHeaderPositions


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

        current_wave_search = "Conditions at {} as of".format(buoy)
        data.present_wave_data = get_current_data(soup, current_wave_search)

        detailed_search = "Detailed Wave Summary"
        data.present_swell_data = get_current_data(soup, detailed_search)

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


def get_current_data(soup, search: str):
    """
    Search the beautiful soup object for a TABLE containing the search string. The function will
    grab the data from the table and create a NOAAData object and return the data
    :param soup: beautiful soup object generated from the get_url_source()
    :param search: text to search for in the soup object. The text MUST be an exact match as this is
    a possible limitation of beautiful soup searching
    :return: NOAAData object if successful otherwise NONE
    """
    if isinstance(soup, BeautifulSoup):

        try:
            table = soup.find(text=search).findParent("table")

            nd = NOAAData()

            for row in table.findAll('tr'):
                cells = row.findAll('td')

                """
                I really don't like this way of doing the parsing but I believe that I am limited ...
                cell[0] -> href data that we do not care about
                cell[1] -> somewhere in here is the same abbreviation use for past data - parse that out
                cell[2] -> this is the value that we want 

                ... like I said I don't like this because it makes it less dynamic 
                """

                if len(cells) > 0:

                    key = None
                    value = None
                    units = None

                    for i in range(1, len(cells)):

                        split_data = cells[i].next.split()

                        if i == _BuoyHeaderPositions.KEY and len(split_data) > 0:
                            # The key is embedded so let's extract it.
                            # Swell Direction (SwD): Split the data and strip off the (): from the last entry.
                            key = sub('[():]', '', split_data[len(split_data) - 1]).lower()

                        # The value is just the first entry in this split data
                        elif i == _BuoyHeaderPositions.VALUE and len(split_data) > 0:

                            num_entries = len(split_data)

                            # Grab the value, if there is a unit associated with the data,
                            # attempt to save the units to the NOAA Data too..

                            if num_entries >= _BuoyDataPositions.VALUE:
                                value = split_data[_BuoyDataPositions.VALUE]

                            if num_entries >= _BuoyDataPositions.UNITS:
                                units = " ".join(split_data[_BuoyDataPositions.UNITS:])

                    if key is not None and value is not None and value != "-":
                        setattr(nd, key, value)

                        # save the units if they existed
                        if units is not None:
                            setattr(nd, key+"_units", units)

            return nd

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
            tables = soup.findAll("table", {"class": "dataTable"})

            for table in tables:

                # list of header information from the table
                headers = []

                for row in table.findAll("tr"):

                    # grab the header information so we can compare it to each row of the table
                    header_info = row.findAll("th", {"class": "dataHeader"})

                    for info in header_info:

                        headers.append(str(info.next).lower())

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
