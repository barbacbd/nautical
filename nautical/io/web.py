from nautical.error import NauticalError
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from logging import getLogger


log = getLogger()

# The same format is used to find all stations online
_STATION_LINK = "https://www.ndbc.noaa.gov/station_page.php?station={}"


def get_noaa_forecast_url(buoy):
    """
    NOAA is kind enough to post all of their data from their buoys at the same url ONLY requiring
    the id of buoy to change at the end of the link (https://www.ndbc.noaa.gov/station_page.php?station=).
    This function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    .. note::
        There is no check that the provided url is correct/valid.

    :param buoy: id of the buoy
    :return: if buoy is not empty , return the full url, otherwise return nothing
    """
    if buoy:
        return _STATION_LINK.format(buoy)
    else:
        log.warning("No buoy ID provided to get_noaa_forecast_url")


def get_url_source(url_name):
    """
    If you already know the url_name or if you have run through the get_noaa_forecast_url(), then you can
    send in the url here. Get the source information for the url and place the information into a BeautifulSoup
    object, so that we can do any lookups of the data that we need.

    .. note::
        The function makes no assumptions about the validity of the url.

    :param url_name: name of the url to search for
    :return: BeautifulSoup Object on success otherwise none
    """
    try:
        open_url = urlopen(url_name)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    except (ValueError, HTTPError) as e:
        log.error(e)
        raise 

