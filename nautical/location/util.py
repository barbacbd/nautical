from ..error import NauticalError
from math import radians, sin, cos, atan2, sqrt
from .point import Point

_EARTH_RADIUS_METERS = 6372800


def haversine(p1: Point, p2: Point) -> float:
    """
    :return: Find the distance between two points using the Haversine methodology
    """
    lat1 = radians(p1.latitude)
    lat2 = radians(p2.latitude)

    diff1 = radians(p1.latitude - p2.latitude)
    diff2 = radians(p1.longitude - p2.longitude)

    a = sin(diff1 / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(diff2 / 2.0) ** 2

    return 2.0 * _EARTH_RADIUS_METERS * atan2(sqrt(a), sqrt(1 - a))


def in_range_ll(lat1_deg: float, lon1_deg: float, lat2_deg: float, lon2_deg: float, distance_m) -> bool:
    """
    :return: whether or on the lat, lon points are within a range of each other
    """
    return in_range(Point(lat1_deg, lon1_deg), Point(lat2_deg, lon2_deg), distance_m)


def in_range(p1: Point, p2: Point, distance_m) -> bool:
    """
    :return: whether or not these two points are within a range of each other
    """
    return haversine(p1, p2) <= distance_m


def area_converter(area: [Point]) -> [Point]:
    """
    Pass in a list of points, determine the maximum and minimum latitude and longitude
    values, create a square (4 points) from the list.

    :param area: original list of points
    :return: list of Points
    """
    max_lat = -float("inf")
    min_lat = float("inf")
    max_lon = -float("inf")
    min_lon = float("inf")

    for point in area:
        if isinstance(point, Point):
            max_lat = point.latitude if point.latitude > max_lat else max_lat
            min_lat = point.latitude if point.latitude < min_lat else min_lat
            max_lon = point.longitude if point.longitude > max_lon else max_lon
            min_lon = point.longitude if point.longitude < min_lon else min_lon

    return [Point(min_lat, min_lon), Point(max_lat, max_lon)]


def in_area(p: Point, area: [Point]) -> bool:
    """
    Determine if point p is in the area. NOTE: the user should pass the original
    list of points through the area_converter. This will provide an approximate area.

    :param p: Point to determine if it is in the area
    :param area: 2 point area min, min -> max, max
    :return: true if it is in the area false otherwise
    """
    if len(area) != 2:
        raise NauticalError("area should be 2 points (min, min) -> (max, max).")

    max_lat = max(area[0].lat, area[1].lat)
    min_lat = min(area[0].lat, area[1].lat)

    max_lon = max(area[0].lon, area[1].lon)
    min_lon = min(area[0].lon, area[1].lon)

    return max_lat >= p.latitude >= min_lat and max_lon >= p.longitude >= min_lon
