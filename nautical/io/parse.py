"""
Author: barbacbd
"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from pykml import parser
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.noaa.buoy.buoy import Buoy
from nautical.noaa.buoy.source import Source
from nautical.location.point import Point
from re import sub
from nautical.error import NauticalError
from . import (
    KML_LINK,
    DEFAULT_BUOY_WAVE_TEXT_SEARCH,
    SWELL_DATA_TEXT_SEARCH,
    PREVIOUS_OBSERVATION_SEARCH
)


def get_buoy_sources():
    """
    NOAA is kind enough to provide all of names, ids, and other information about ALL of their known buoys
    in a kml document hosted at the link provided.

    https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml

    Let's read through this document and parse the buoy information to determine their id and location.
    The ID can be used to provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys. NOTE: the SHIP ID may not be able to be looked up. The coordinates are used aas general information
    to determine distance from other points, or for display purposes.

    :return: dictionary all source names mapped to their respective source.
    """
    sources = {}

    try:
        fileobject = urlopen(KML_LINK)
    except URLError:
        return sources

    root = parser.parse(fileobject).getroot()

    # grab the embedded link that will provide the kml to all buoys
    real_kml = root.Document.NetworkLink.Link.href

    if real_kml:
        real_fileobject = urlopen(str(real_kml))
        real_root = parser.parse(real_fileobject).getroot()

        for category in real_root.Document.Folder.Folder:

            s = Source(category.name, category.description)

            for pm in category.Placemark:

                p = Point()
                p.parse(str(pm.Point.coordinates))
                b = Buoy(pm.name, location=p)

                s.add_buoy(b)

            sources[s.name] = s

    return sources


def create_buoy(buoy):
    """
    Provide a full workup for a specific buoy. If the buoy is None or it cannot be found
    then the data returned will be considered invalid as None
    :param buoy: id of the buoy to do a workup on
    :return: BuoyWorkup if successful else None
    """
    if buoy is not None:
        url = get_noaa_forecast_url(buoy)
        soup = get_url_source(url)

        current_buoy_data = BuoyData()
        get_current_data(soup, current_buoy_data, DEFAULT_BUOY_WAVE_TEXT_SEARCH.format(buoy))
        get_current_data(soup, current_buoy_data, SWELL_DATA_TEXT_SEARCH)
        past_data = get_past_data(soup)

        buoy_data = Buoy(buoy)
        buoy_data.present = current_buoy_data
        buoy_data.past = past_data

        return buoy_data

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


def get_current_data(soup: BeautifulSoup, buoy: BuoyData, search: str):
    """
    Search the beautiful soup object for a TABLE containing the search string. The function will
    grab the data from the table and create a NOAAData object and return the data
    :param soup: beautiful soup object generated from the get_url_source()
    :param buoy: BuoyData object that should be filled with data as this function parses the data.
    :param search: text to search for in the soup object. The text MUST be an exact match as this is
                   a possible limitation of beautiful soup searching
    """
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

                buoy.update(var=key, value=value)


def get_past_data(soup: BeautifulSoup):
    """
    Find all Previous Observations or Past Data.
    :param soup: beautiful soup object generated from the get_url_source()
    :return: list of all previous observations from the url. The buoy data returned in the list
             may be a comprehension of swell and wave data.
    """

    past_data = {}

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

                    data = {
                        noaa_var_names[i]: "".join(str(cell.next).split())
                        for i, cell in enumerate(cells)
                    }

                    if "time" in data:
                        nd = past_data.get(data["time"], BuoyData())
                        nd.from_dict(data)

                        # update the dictionary even if this one already existed
                        past_data[data["time"]] = nd

    return past_data.values()
