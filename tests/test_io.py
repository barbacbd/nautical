from nautical.io.web import get_noaa_forecast_url, get_url_source
from nautical.io.cdata import (
    parse_winds,
    parse_location,
    parse_time,
    parse_cdata,
    fill_buoy_with_cdata
)
from nautical.location import Point
from nautical.time import NauticalTime
from nautical.noaa.buoy import Buoy, BuoyData
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pytest
from os.path import abspath, dirname, join
from unittest.mock import Mock, patch


class MockResponse:
    '''Class to mock the behavior and results of the requests.get function
    in the NCEI module of the Nautical library.
    '''

    def __init__(self, data, status_code):
        '''Fill the class with the required data for a response
        expected from the NCEI API.

        :param data: String data from the request
        :param status_code: Mock of the requests.get status_code
        '''
        self.data = data
        self.code = status_code

    def read(self):
        '''Mock function for the requests.get.json return type
        :return: data that was input 
        '''
        return self.data


def create_good_response():
    '''Create a mock response with good data'''
    with open(join(abspath(dirname(__file__)), "GoodWebpage.html"), "r") as good_data:
        mock_resp = MockResponse(good_data.read(), 200)

    return mock_resp
    
def create_bad_response(data, code):
    '''Create a mock response with bad data'''
    mock_resp = MockResponse(data, code)
    return mock_resp


def test_beautiful_soup_good():
    '''Test that a valid url can be created using a known buoy ID 
    in the integer format. The format function is not the one
    being tested here (that is tested as part of python and not
    necessary here).

    If interested the 44099 buoy resides in the Chesapeake Bay
    off of the coast of Virginia.
    '''
    with patch("nautical.io.web.urlopen") as get_patch:
        get_patch.return_value = create_good_response()
        url = get_noaa_forecast_url(44099)
        soup = get_url_source(url)
        assert isinstance(soup, BeautifulSoup)


def test_beautiful_soup_bad():
    '''Test that a buoy ID that has no meaning and no known
    matching buoy will not pass the lookup/creation.
    '''
    with patch("nautical.io.web.urlopen", side_effect=HTTPError("", 404, "", {}, "")) as get_patch:
        get_patch.return_value = create_bad_response("", 404)

        with pytest.raises(HTTPError):
            bad_url = get_noaa_forecast_url("afasdfasdjfna")
            bad_soup = get_url_source(bad_url)


def test_beautiful_soup_bad_empty_str_entry():
    '''Test that an empty buoy ID will not make a valid lookup request
    '''
    with patch("nautical.io.web.urlopen", side_effect=HTTPError("", 404, "", {}, "")) as get_patch:
        get_patch.return_value = create_bad_response("", 404)

        with pytest.raises(HTTPError):
            bad_url = get_noaa_forecast_url("")
            bad_soup = get_url_source(bad_url)


def test_beautiful_soup_bad_empty_none_entry():
    '''Test that an empty buoy ID will not make a valid lookup request
    '''
    with pytest.raises(AttributeError):
        bad_soup = get_url_source(None)

    
def test_forecast_url_good():
    '''Test valid and invalid sets of data passed to the create forecast url
    '''
    assert get_noaa_forecast_url(44099) is not None

    
def test_forecast_url_bad():
    '''Test invalid forecast url
    '''
    with pytest.raises(AssertionError):
        assert get_noaa_forecast_url("sfsdfasdfa") is None

    
def test_forecast_url_bad_empty_entry():
    '''Test invalid forecast url - Empty String
    '''
    assert get_noaa_forecast_url("") is None
 

def test_forecast_url_bad_none_entry():
    '''Test invalid forecast url - None
    '''
    with pytest.raises(TypeError):
        assert get_noaa_forecast_url() is None

 
def test_cdata_date_24_afternoon():
    '''Test a valid date that occurs after noon
    that way there is no ambiguity for parsing
    '''
    time_data = "05/10/2022 1434 UTC"
    parsed = parse_time(time_data)

    assert parsed["mm"] == 5
    assert parsed["dd"] == 10
    assert parsed["year"] == 2022
    assert parsed["time"].minutes == 34
    assert parsed["time"].hours == 14
    

def test_cdata_date_24_morning():
    '''Test a valid date that occurs before noon
    causing the assumption to be made that the 
    time is 24 hour
    '''
    time_data = "05/10/2022 0100 UTC"
    parsed = parse_time(time_data)

    assert parsed["mm"] == 5
    assert parsed["dd"] == 10
    assert parsed["year"] == 2022
    assert parsed["time"].minutes == 00
    assert parsed["time"].hours == 1

    
def test_cdata_bad_date_empty():
    '''Test an invalid date, no data except
    UTC'''
    time_data = "UTC"
    parsed = parse_time(time_data)

    assert parsed["mm"] == None
    assert parsed["dd"] == None
    assert parsed["year"] == None
    assert parsed["time"] == None


def test_cdata_bad_date_missing_values():
    '''Test a bad date value with missing values
    for the date
    '''
    time_data = "10/2022 0100 UTC"
    parsed = parse_time(time_data)

    assert parsed["mm"] == 10
    assert parsed["dd"] == 2022
    assert parsed["year"] == None
    assert parsed["time"] == None


def test_cdata_bad_time_missing_values():
    '''Test a bad time/date value with missing values
    for the time
    '''
    time_data = "05/10/2022 UTC"
    parsed = parse_time(time_data)

    assert parsed["mm"] == 5
    assert parsed["dd"] == 10
    assert parsed["year"] == 2022
    assert parsed["time"] == None


def test_cdata_good_wind_and_gust():
    '''Test a valid wind and gust value combo'''
    wind_data = " E (90&#176;) at 15.6 kts gusting at 19.6 kts"
    parsed_wind_data = parse_winds(wind_data)
    assert parsed_wind_data["wspd"] == 15.6
    assert parsed_wind_data["gst"] == 19.6
    

def test_cdata_good_wind_no_gust():
    '''Test valid wind but no gust information'''
    wind_data = " E (90&#176;) at 15.6 kts"
    parsed_wind_data = parse_winds(wind_data)
    assert parsed_wind_data["wspd"] == 15.6
    assert parsed_wind_data["gst"] == None

    
def test_cdata_bad_wind_data_no_values():
    '''Test wind and gust information missing'''
    wind_data = " E (90&#176;) at a15.6 kts"
    parsed_wind_data = parse_winds(wind_data)
    assert parsed_wind_data["wspd"] == None
    assert parsed_wind_data["gst"] == None
    

def test_cdata_valid_location():
    '''Parse a valid location'''
    data = "69.7S 87.34E"
    parsed_data_dict = parse_location(data)
    assert parsed_data_dict["location"].latitude == -69.7
    assert parsed_data_dict["location"].longitude == 87.34
    

def test_cdata_bad_location_string():
    '''Test a completely invalid string for latitude/longitude'''
    data = "adsad asdsad"
    parsed_data_dict = parse_location(data)
    assert "location" not in parsed_data_dict
    
    
def test_cdata_valid_location_string_bad_values():
    '''Test that the string is parsed but the values
    are not within the valid limits of lat and lon
    '''
    data = "99.7N 187.34W"
    parsed_data_dict = parse_location(data)
    assert parsed_data_dict["location"].latitude == 99.7
    assert parsed_data_dict["location"].longitude == -187.34


def test_cdata_no_latitude():
    '''Test a valid string that is missing latitude
    data
    '''
    data = "65.7E"
    parsed_data_dict = parse_location(data)
    assert "location" not in parsed_data_dict


def test_cdata_no_longitude():
    '''Test a valid string but missing longitude
    data
    '''
    data = "65.7N"
    parsed_data_dict = parse_location(data)
    assert "location" not in parsed_data_dict


def test_cdata_lat_no_sign():
    '''Latitude is missing N/S value, no assumptions
    are made, so the value cannot be found.
    '''
    data = "65.7 13.6W"
    parsed_data_dict = parse_location(data)
    assert "location" not in parsed_data_dict

    
def test_cdata_lon_no_sign():
    '''Longitude is missing E/W value, no assumptions
    are made, so the value cannot be found
    '''
    data = "65.7N 13.6"
    parsed_data_dict = parse_location(data)
    assert "location" not in parsed_data_dict


def test_good_cdata_min_values():
    '''Create a minimum string of data to parse'''
    cdata = """
<b>Location:</b> 65.7N 13.6W
<br /><b>05/10/2022 0100 UTC</b><br /><b>Significant Wave Height:</b> 4.6 ft<br />
<b>Dominant Wave period:</b> 5 sec<br />"""

    parsed_cdata_dict = parse_cdata(cdata)

    assert "location" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["location"], Point)

    assert "time" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["time"], NauticalTime)
    
    expected = {
        "mm": 5,
        "dd": 10,
        "year": 2022,
        "wvht": 4.6,
        "dpd": 5
    }

    for key, value in expected.items():
        assert key in parsed_cdata_dict
        assert value == parsed_cdata_dict[key]
    
def test_good_cdata_large_string():
    '''Create a large string of data to parse
    simulating one that comes from the kml
    '''
    cdata = """
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />"""
    parsed_cdata_dict = parse_cdata(cdata)

    assert "location" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["location"], Point)

    assert "time" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["time"], NauticalTime)
    
    expected = {
        "mm": 5,
        "dd": 10,
        "year": 2022,
        "pres": 29.75,
        "atmp": 84.2,
        "wtmp": 83.5,
        "dewp": 80.6,
        "wvht": 1.6,
        "dpd": 3,
        "vis": 11,
        "wspd": 15.6
    }

    for key, value in expected.items():
        assert key in parsed_cdata_dict
        assert value == parsed_cdata_dict[key]
    

def test_good_cdata_large_missing_values():
    '''Create a large string of data to parse 
    simulating one that comes from the kml - 
    but is missing fields
    '''
    cdata = """
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Random Test Data:</b> 11 nmi<br />"""
    parsed_cdata_dict = parse_cdata(cdata)

    assert "location" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["location"], Point)

    assert "time" in parsed_cdata_dict
    assert isinstance(parsed_cdata_dict["time"], NauticalTime)

    expected = {
        "mm": 5,
        "dd": 10,
        "year": 2022,
        "pres": 29.75,
        "atmp": 84.2,
        "wtmp": 83.5,
        "dewp": 80.6,
        "wvht": 1.6,
        "dpd": 3,
        # "vis": 11,  # missing
        "wspd": 15.6
    }
    
    for key, value in expected.items():
        assert key in parsed_cdata_dict
        assert value == parsed_cdata_dict[key]

    
def test_full_cdata_bad_location():
    '''Test a string of cdata information
    where the location is bad. In this case the
    latitude value is unknown
    '''
    cdata = """
<b>Location:</b> 9.0 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />"""
    parsed_cdata_dict = parse_cdata(cdata)

    assert "location" not in parsed_cdata_dict


def test_full_cdata_bad_wind():
    '''Test a string of cdata information
    where the wind is bad
    '''
    cdata = """
<b>Location:</b> 9.0 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at a15.6 kts gusting at ad19.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />"""
    parsed_cdata_dict = parse_cdata(cdata)

    assert "wspd" not in parsed_cdata_dict
    assert "gst" not in parsed_cdata_dict
    

def test_full_cdata_bad_time():
    '''Test a string of cdata information
    where the time/date is bad
    '''
    cdata = """
<b>Location:</b> 9.0 120.4E
<br /><b>05/10/2022 UTC</b><br /><b>Winds:</b> E (90&#176;) at a15.6 kts gusting at ad19.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />"""
    parsed_cdata_dict = parse_cdata(cdata)

    assert "time" not in parsed_cdata_dict

    
def test_cdata_good_buoy():
    '''Test cdata string that is good and is placed 
    into a buoy object
    '''
    cdata = """
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0023 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />"""
    buoy = Buoy("test")
    fill_buoy_with_cdata(buoy, cdata)

    assert buoy.location.latitude == 9.0
    assert buoy.location.longitude == 120.4

    assert buoy.data.time.minutes == 23.0
    assert buoy.data.time.hours == 0.0
    
    expected = {
        "mm": 5,
        "dd": 10,
        "year": 2022,
        "pres": 29.75,
        "atmp": 84.2,
        "wtmp": 83.5,
        "dewp": 80.6,
        "wvht": 1.6,
        "dpd": 3,
        "vis": 11,
        "wspd": 15.6
    }

    for k, v in buoy.data:
        if k == "time":
            continue

        if k in expected:
            assert v == expected[k]


def test_cdata_bad_buoy():
    '''Test cdata string that is bad and cannot be set into
    a buoy object
    '''
    cdata = """
Some Random Bad Data"""
    buoy = Buoy("test")
    fill_buoy_with_cdata(buoy, cdata)

    values = {}

    # Time information is automatically filled out, so we can
    # skip this information
    for k, v in buoy.data:
        if k not in ("mm", "dd", "year", "time"):
            values[k] = v
        
    assert not values
