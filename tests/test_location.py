from nautical.location.point import Point
from nautical.location.util import haversine
from math import fabs
import pytest


def test_latitude_valid_positive():
    """Test a valid latitude point -90.0 <= lat >= 90.0"""
    p = Point(67.23, 0, 0)
    assert p.latitude == 67.23


def test_latitude_valid_negative():
    """Test a valid latitude point -90.0 <= lat >= 90.0"""
    p = Point(-67.23, 0, 0)
    assert p.latitude == -67.23


def test_latitude_invalid_string():
    """Test a invalid latitude point -90.0 <= lat >= 90.0
    The value can be a string if it can be converted
    """
    p = Point()
    p.latitude = "abgsdf"
    assert p.latitude == 0


def test_latitude_oob():
    """Test a valid latitude point -90.0 <= lat >= 90.0"""
    p3 = Point(-90.23, 0, 0)
    assert p3.latitude == 0


def test_longitude_valid_positive():
    """Test a valid longitude point -180.0 <= lon >= 180.0"""
    p1 = Point(0, 0.23, 0)
    assert p1.longitude == 0.23

def test_longitude_valid_negative():
    """Test a valid longitude point -180.0 <= lon >= 180.0"""
    p2 = Point(0, -167.23, 0)
    assert p2.longitude == -167.23

def test_longitude_invalid_string():
    """Test a invalid longitude point -180.0 <= lon >= 180.0
    The value can be a string if it can be converted
    """
    p2 = Point()
    p2.longitude = "dasdf"
    assert p2.longitude == 0

def test_longitude_invalid_oob():
    """Test a valid longitude point -180.0 <= lon >= 180.0"""
    p3 = Point(0, 180.23, 0)
    assert p3.longitude == 0.0
    
    
def test_altitude_valid():
    """
    Test both a valid and invalid altitude value checking the whether the values were set or not
    after each attempt.
    """
    p1 = Point(0, 0, 1251231.2342)
    assert p1.altitude == 1251231.2342, 4


def test_altitude_bad_string():
    p1 = Point()
    p1.altitude = "123123jnnkjk"
    assert p1.altitude == 0

def test_parser_3():
    """
    Test the parse function of the Point
    """
    p1 = Point()
    p1.parse("-110.123, 76.45, 123.67")

    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 123.67
    

def test_parser_2():
    """
    Test the parse function of the Point
    """
    p1 = Point()
    p1.parse("-110.123, 76.45")
    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 0.0


def test_parser_bad_third():
    """
    Test the parse function of the Point
    """
    p1 = Point()
    with pytest.raises(ValueError):
        p1.parse("-110.123, 76.45, dfasdfasd")


def test_parser_bad_second():
    """
    Test the parse function of the Point
    """
    p1 = Point()
    with pytest.raises(ValueError):
        p1.parse("-110.123, sdasdf")


def test_parser_bad_missing_data():
    """
    Test the parse function of the Point
    """
    p1 = Point()
    with pytest.raises(IndexError):
        p1.parse("-110.123")


def test_distance():
    """
    Test the haversine distance function of the Point class

    test distance from virginia beach to norfolk Virginia

    """
    # location of virginia beach
    p = Point(36.8529, -75.9780)

    # location of norfolk
    dist = haversine(p, Point(36.8508, -76.2859))

    # roughly 27 km but it is closer to 27404.727 .... meters
    assert fabs(dist-27404.73) <= 0.01

