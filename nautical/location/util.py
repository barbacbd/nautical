from .point import Point
from ..error import NauticalError


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
            max_lat = point.lat if point.lat > max_lat else max_lat
            min_lat = point.lat if point.lat < min_lat else min_lat
            max_lon = point.lon if point.lon > max_lon else max_lon
            min_lon = point.lon if point.lon < min_lon else min_lon

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

    return max_lat >= p.lat >= min_lat and max_lon >= p.lon >= min_lon
