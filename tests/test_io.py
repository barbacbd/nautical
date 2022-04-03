from nautical.io.web import get_noaa_forecast_url, get_url_source
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pytest


def test_beautiful_soup_good():
    """
    Test that a valid url can be created using a known buoy ID 
    in the integer format. The format function is not the one
    being tested here (that is tested as part of python and not
    necessary here).

    If interested the 44099 buoy resides in the Chesapeake Bay
    off of the coast of Virginia.
    """
    url = get_noaa_forecast_url(44099)
    soup = get_url_source(url)
    assert isinstance(soup, BeautifulSoup)

    
def test_beautiful_soup_bad():
    """
    Test that a buoy ID that has no meaning and no known
    matching buoy will not pass the lookup/creation.
    """
    with pytest.raises(HTTPError):
        bad_url = get_noaa_forecast_url("afasdfasdjfna")
        bad_soup = get_url_source(bad_url)

        
def test_beautiful_soup_bad_empty_str_entry():
    """
    Test that an empty buoy ID will not make a valid lookup request
    """
    with pytest.raises(AttributeError):
        bad_url = get_noaa_forecast_url("")
        # returns but causes bad_url
        bad_soup = get_url_source(bad_url)


def test_beautiful_soup_bad_empty_none_entry():
    """
    Test that an empty buoy ID will not make a valid lookup request
    """
    with pytest.raises(TypeError):
        bad_url = get_noaa_forecast_url()
        bad_soup = get_url_source(bad_url)

    
def test_forecast_url_good():
    """
    Test valid and invalid sets of data passed to the create forecast url
    """
    assert get_noaa_forecast_url(44099) is not None

    
def test_forecast_url_bad():
    """
    Test invalid forecast url
    """
    with pytest.raises(AssertionError):
        assert get_noaa_forecast_url("sfsdfasdfa") is None

    
def test_forecast_url_bad_empty_entry():
    """
    Test invalid forecast url - Empty String
    """
    assert get_noaa_forecast_url("") is None
 

def test_forecast_url_bad_none_entry():
    """
    Test invalid forecast url - None
    """
    with pytest.raises(TypeError):
        assert get_noaa_forecast_url() is None
