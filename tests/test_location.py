from nautical.location.point import Point
from nautical.location.util import haversine, in_range, in_range_ll, in_area
from nautical.units import DistanceUnits, TimeUnits
from math import fabs
import pytest


def test_create_no_altitude():
    '''Test the creation of a point. Even though no altitude is
    provided it should not throw an error on altitude or z getter
    '''
    p1 = Point(76.45, -110.123)
    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 0.0

    
def test_create_with_altitude():
    '''Base Test for a fully valid creation'''
    p1 = Point(76.45, -110.123, 123.67)
    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 123.67
    
    
def test_parse_altitude():
    '''Test the parse static method with altitude'''
    p1 = Point.parse("-110.123, 76.45, 123.67")
    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 123.67


def test_parse_no_altitude():
    '''Test the parse static method without altitude'''
    p1 = Point.parse("-110.123, 76.45")
    assert p1.latitude == 76.45 and p1.longitude == -110.123


def test_parse_no_altitude_bad():
    '''Test the parse static method without altitude
    but there is a second comma which should provide a bad 
    return value
    '''
    with pytest.raises(ValueError):
        p1 = Point.parse("-110.123, 76.45,")

        
def test_parse_bad_latitude():
    '''Test the parse static method with altitude, fail on bad value'''
    with pytest.raises(ValueError):
        p1 = Point.parse("-110.123, sdffgsdfg, 123.67")


def test_parse_noaa_altitude():
    '''Test the parse static method with altitude'''
    p1 = Point.parse_noaa_kml_format("-110.123, 76.45, 123.67")
    assert p1.latitude == 76.45 and p1.longitude == -110.123 and p1.altitude == 123.67


def test_parse_noaa_no_altitude():
    '''Test the parse static method without altitude'''
    p1 = Point.parse_noaa_kml_format("-110.123, 76.45")
    assert p1.latitude == 76.45 and p1.longitude == -110.123


def test_parse_noaa_no_altitude_bad():
    '''Test the parse static method without altitude
    but there is a second comma which should provide a bad 
    return value
    '''
    with pytest.raises(ValueError):
        p1 = Point.parse_noaa_kml_format("-110.123, 76.45,")

        
def test_parse_noaa_bad_latitude():
    '''Test the parse static method with altitude, fail on bad value'''
    with pytest.raises(ValueError):
        p1 = Point.parse_noaa_kml_format("-110.123, sdffgsdfg, 123.67")


def test_haversine_valid():
    '''Test a known distance between two points and determine that it is
    correct with base units
    '''
    assert 142665 == int(haversine(Point(36, -75), Point(37, -76)))

    
def test_haversine_new_units_valid():
    '''Test a known distance between two points and determine that it is
    correct with the units modified
    '''
    assert 143 == int(round(haversine(Point(36, -75), Point(37, -76), DistanceUnits.KILOMETERS)))

    
def test_haversine_invalid_units():
    '''Test haversine by providing incorrect type of units'''
    with pytest.raises(TypeError):
        assert haversine(Point(36, -75), Point(37, -76), TimeUnits.SECONDS)


def test_haversine_centimeters():
    '''Centimeters is not supported and should return None'''
    with pytest.raises(AttributeError):
        assert haversine(Point(36, -75), Point(37, -76), DistanceUnits.CENTIMETERS) is None

    
def test_haversine_p2_incorrect():
    '''Test providing a value for P2 that is not a point'''
    with pytest.raises(TypeError):
        assert haversine(Point(36, -75), 123)

        
def test_haversine_p1_incorrect():
    '''Test providing type for p1 is incorrect'''
    with pytest.raises(TypeError):
        assert haversine(1234, Point(36, -75))


def test_in_range_valid_base_units():
    '''Test a known distance between points is valid
    using the base units
    '''
    assert in_range(Point(36, -75), Point(37, -76), 150000)

    
def test_in_range_valid_modified_units():
    '''Test a known distance between points is valid
    using the modified units
    '''
    assert in_range(Point(36, -75), Point(37, -76), 150, DistanceUnits.KILOMETERS)


def test_in_range_false_base_units():
    '''Test two points not in range with base units'''
    assert not in_range(Point(36, -75), Point(37, -76), 140000)
    

def test_in_range_false_base_units():
    '''Test two points not in range with modified units'''
    assert not in_range(Point(36, -75), Point(37, -76), 140, DistanceUnits.KILOMETERS)
        

def test_in_range_invalid_p2_not_point():
    '''P2 is not a point throws an error in comparison'''
    with pytest.raises(TypeError):
        assert not in_range(Point(36, -75), "erser", 140000)
    

def test_in_range_invalid_p1_not_point():
    '''P1 is not a point throws an error in comparison'''
    with pytest.raises(TypeError):
        assert not in_range("serser", Point(36, -75), 140000)

    
def test_in_range_unsupported_units():
    '''Test in range using an unsupported type = Centimeters'''
    with pytest.raises(TypeError):
        assert not in_range("serser", Point(36, -75), 140000, DistanceUnits.CENTIMETERS)


def test_in_range_ll_valid_base_units():
    '''Test a known distance between points is valid
    using the base units
    '''
    assert in_range_ll(36, -75, 37, -76, 150000)
    

def test_in_range_ll_valid_modified_units():
    '''Test a known distance between points is valid
    using the modified units
    '''
    assert in_range_ll(36, -75, 37, -76, 150, DistanceUnits.KILOMETERS)


def test_in_range_ll_false_base_units():
    '''Test two points not in range with base units'''
    assert not in_range_ll(36, -75, 37, -76, 140000)

    
def test_in_range_ll_false_modified_units():
    '''Test two points not in range with modified units'''
    assert not in_range_ll(36, -75, 37, -76, 140, DistanceUnits.KILOMETERS)

    

def test_in_area_simple():
    '''Provide two points which should make a square around max 
    and min for lat and lon. The point should be in it.
    '''
    geo = [Point(36.849403, -75.9408287), Point(36.867840, -75.813113)]
    assert in_area(geo, Point(36.854422, -75.854998))


def test_in_area_simple_invalid():
    '''Provide two points which should make a square around max 
    and min for lat and lon. The point should NOT be in it.
    '''
    geo = [Point(36.849403, -75.9408287), Point(36.867840, -75.813113)]
    assert not in_area(geo, Point(36.876079, -75.736208))


def test_simple_square_in():
    '''Test that 4 points making a square contains the point'''
    geo = [
        Point(36.849403, -75.9408287),
        Point(36.849403, -75.813113),
        Point(36.867840, -75.813113),
        Point(36.867840, -75.9408287)
    ]
    assert in_area(geo, Point(36.854422, -75.854998))

    
def test_simple_square_edge_out():
    '''Test that 4 points making a square does not contain the point
    When the point resides on the edge of the square'''
    geo = [
	Point(36.849403, -75.9408287),
        Point(36.849403, -75.813113),
        Point(36.867840, -75.813113),
        Point(36.867840, -75.9408287)
    ]
    assert not in_area(geo, Point(36.854422, -75.9408287))


def test_simple_corner_out():
    '''Test that 4 points making a square does not contain the point
    When the point is a corner of the square
    '''
    geo = [
	Point(36.849403, -75.9408287),
        Point(36.849403, -75.813113),
        Point(36.867840, -75.813113),
        Point(36.867840, -75.9408287)
    ]
    assert not in_area(geo, Point(36.867840, -75.9408287))


def test_simple_invalid():
    '''Test 4 points making a square and the point is outside'''
    geo = [
        Point(36.849403, -75.9408287),
        Point(36.849403, -75.813113),
        Point(36.867840, -75.813113),
        Point(36.867840, -75.9408287)
    ]
    assert not in_area(geo, Point(36.876079, -75.736208))

    
def test_complex_valid():
    '''Test a complex shape where the point is in the shape
    '''
    geo = [
        Point(36.932651, -75.852713),
        Point(36.824144, -75.800303),
        Point(36.862386, -75.784889),
        Point(36.808101, -75.700108),
	Point(36.916631, -75.650781)
    ]
    assert in_area(geo, Point(36.84, -75.742))
    
def test_complex_invalid():
    '''Test a complex shape where the point is not in the shape
    on a concave section
    '''
    geo = [
        Point(36.932651, -75.852713),
        Point(36.824144, -75.800303),
        Point(36.862386, -75.784889),
        Point(36.808101, -75.700108),
	Point(36.916631, -75.650781)
    ]
    assert not in_area(geo, Point(36.84, -75.784889))

def test_json_complete_set():
    '''Test a full work up of json for the Point'''
    p = Point(36.0, -75.0, 500.0)
    json_dict = p.to_json()
    
    assert json_dict["latitude"] == 36.0
    assert json_dict["longitude"] == -75.0
    assert json_dict["altitude"] == 500.0
    
    json_dict["latitude"] = 35.45
    json_dict["longitude"] = -78.234
    json_dict["altitude"] = 10
    
    p = Point.from_json(json_dict)
    
    assert p.latitude == 35.45
    assert p.longitude == -78.234
    assert p.altitude == 10