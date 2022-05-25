from nautical.units import DistanceUnits
from .point import Point


def haversine(point_one, point_two, units=DistanceUnits.METERS) -> float:
    '''Wrapper for the Haversine for the `Point` class in this module

    :param p1: `Point` 1
    :param point_two: `Point` 2
    :param units: nautical.units.DistanceUnits
    :return: Distance between the points, in units
    '''
    if not isinstance(point_one, Point):
        raise TypeError("The first parameter must be a Point object")
    return point_one.distance(point_two, units)


# pylint: disable=too-many-arguments
def in_range_ll(lat1_deg, lon1_deg, lat2_deg, lon2_deg, distance, units=DistanceUnits.METERS):
    '''Determine if points are within a distance of each other provided
    with the latitude, longitude of each point

    :param lat1_deg: Latitude of point 1 in degrees
    :param lon1_deg: Longitude of point 1 in degrees
    :param lat2_deg: Latitude of point 2 in degrees
    :param lon2_deg: Longitude of point 2 in degrees
    :param distance_m: Max allowed distance between points to return true (meters).
    :return: True when the distance between P1 and P2 is less than (or equal to) distance_m
    '''
    return in_range(Point(lat1_deg, lon1_deg), Point(lat2_deg, lon2_deg), distance, units)


def in_range(point_one, point_two, distance, units=DistanceUnits.METERS):
    '''Determine if the points are within a distance of each other.

    :param point_one: Point 1
    :param point_two: Point 2
    :param distance: Max allowed distance between points to return true.
    :param units: Units of measurement [default=METERS]
    :return: True when the distance between P1 and P2 is less than (or equal to) distance_m
    '''
    if not isinstance(point_one, Point):
        raise TypeError("The first parameter must be a Point object")
    if not isinstance(point_two, Point):
        raise TypeError("The second parameter must be a Point object")
    return point_one.in_range(point_two, distance, units)


def _create_square(geometry):
    '''When there are only two points in a geometry, instead of using a 
    line, create a square/rectangle out of the max/mins

    :param geometry: Ordered list of `Point` objects
    :return: 4 point geometry
    '''
    min_lat = min(geometry[0].latitude, geometry[1].latitude)
    max_lat = max(geometry[0].latitude, geometry[1].latitude)
    min_lon = min(geometry[0].longitude, geometry[1].longitude)
    max_lon = max(geometry[0].longitude, geometry[1].longitude)

    return [
        Point(min_lat, min_lon), 
        Point(min_lat, max_lon),
        Point(max_lat, max_lon),
        Point(max_lat, min_lon)
    ]


def _find_intersections(geometry, point):
    '''Find the number of times that the point intesects with 
    the edges of the geometry when extending a ray towards the 
    edges of the geometry.

    :param geometry: Ordered list of `Point` objects
    :param point: `Point` to calculate the intersections
    :return: Number of times the ray instersects with the geometry
    '''
    # number of times hit an edge
    intersected = 0
    for i, geo_point in enumerate(geometry):
        curr = geo_point
        nxt = geometry[(i + 1) % len(geometry)]

        if curr.y == nxt.y:
            continue

        if max(curr.y, nxt.y) >= point.y > min(curr.y, nxt.y):
            if point.x <= max(curr.x, nxt.x):
                xinters = (point.y - curr.y) * (nxt.x - curr.x) / (nxt.y - curr.y) + curr.x
                if curr.x == nxt.x or point.x <= xinters:
                    intersected += 1

    return intersected


def in_area(geometry, point):
    '''Determine if a point exists within a geometry of points. The algorithm
    can be found here:
    https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html

    :param geometry: Ordered list of `Point` objects
    :param point: `Point` that should be checked if exists in the geometry
    :return: True when the value lies in the geometry, false otherwise
    '''
    if not isinstance(point, Point):
        raise TypeError("The second parameter must be a Point object")

    if len(geometry) < 2:
        raise TypeError("Geometry must be a set of points with a length of 2 or more")

    if len(geometry) == 2:
        geo_points = _create_square(geometry)
    else:
        for pnt in geometry:
            if not isinstance(pnt, Point):
                raise TypeError("All values of geometry must be Point objects")

        geo_points = geometry

    intersected = _find_intersections(geo_points, point)

    # There will be an odd number for points in a geometry, even for those that
    # do not reside in the geometry
    return intersected % 2 == 1
