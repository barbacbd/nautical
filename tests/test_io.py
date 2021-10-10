from nautical.io.web import get_noaa_forecast_url, get_url_source
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pytest


def test_beautiful_soup_good():
    """
    Test that an invalid and valid url return the proper data
    """
    url = get_noaa_forecast_url(44099)
    soup = get_url_source(url)
    assert isinstance(soup, BeautifulSoup)

    
def test_beautiful_soup_bad():
    with pytest.raises(HTTPError):
        bad_url = get_noaa_forecast_url("afasdfasdjfna")
        bad_soup = get_url_source(bad_url)

    
def test_forecast_url_good():
    """
    Test valid and invalid sets of data passed to the create forecast url
    """
    assert get_noaa_forecast_url(44099) is not None

def test_forecast_url_bad():
    assert get_noaa_forecast_url("") is None
 
