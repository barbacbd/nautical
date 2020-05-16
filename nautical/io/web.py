"""
Author: barbacbd
Date:   5/16/2020
"""
from nautical.error import NauticalError
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


# The same format is used to find all stations online
_STATION_LINK = "https://www.ndbc.noaa.gov/station_page.php?station={}"


def get_noaa_forecast_url(buoy):
    """
    NOAA is kind enough to post all of their data from their buoys at the same url ONLY requiring
    the id of buoy to change at the end of the link.

    https://www.ndbc.noaa.gov/station_page.php?station=

    this function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    NOTE: this does not check to ensure that this is a valid url.

    :param buoy: id of the buoy
    :return: if buoy is not empty , return the full url, otherwise return nothing
    """
    if buoy:
        return _STATION_LINK.format(buoy)
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
    except (ValueError, HTTPError) as e:
        raise NauticalError("failed to get the url source: {}".format(e))

