from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from nautical.log import get_logger


log = get_logger()


def get_noaa_forecast_url(buoy):
    '''NOAA is kind enough to post all of their data from their buoys at 
    the same url ONLY requiring the id of buoy to change at the end of the link 
    (https://www.ndbc.noaa.gov/station_page.php?station=).
    This function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    :param buoy: id of the buoy
    :return: full url if buoy is not empty, otherwise None
    '''
    if buoy:
        return f"https://www.ndbc.noaa.gov/station_page.php?station={buoy}"
    log.warning("No buoy ID provided to get_noaa_forecast_url")


def get_url_source(url_name):
    '''If you already know the url_name or if you have run through the 
    get_noaa_forecast_url(), then you can send in the url here. Get the source 
    information for the url and place the information into a BeautifulSoup
    object, so that we can do any lookups of the data that we need.

    :param url_name: name of the url to search for
    :return: BeautifulSoup Object on success otherwise none
    '''
    try:
        open_url = urlopen(url_name)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    except (AttributeError, TypeError, ValueError, HTTPError) as error:
        log.error(error)
        raise
