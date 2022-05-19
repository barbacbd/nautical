from ..error import NauticalError
from math import radians, sin, cos, atan2, sqrt
from .point import Point
from nautical.units import DistanceUnits


def haversine(p1, p2, units = DistanceUnits.METERS) -> float:
    '''Wrapper for the Haversine for the `Point` class in this module
    
    :param p1: `Point` 1
    :param p2: `Point` 2
    :param units: nautical.units.DistanceUnits
    :return: Distance between the points, in units
    '''
    if not isinstance(p1, Point):
        raise TypeError("The first parameter must be a Point object")
    return p1.distance(p2, units)


def in_range_ll(
        lat1_deg,
        lon1_deg,
        lat2_deg,
        lon2_deg,
        distance,
        units = DistanceUnits.METERS
):
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


def in_range(p1, p2, distance, units = DistanceUnits.METERS):
    '''Determine if the points are within a distance of each other.
    
    :param p1: Point 1
    :param p2: Point 2
    :param distance: Max allowed distance between points to return true.
    :param units: Units of measurement [default=METERS]
    :return: True when the distance between P1 and P2 is less than (or equal to) distance_m
    '''
    if not isinstance(p1, Point):
        raise TypeError("The first parameter must be a Point object")
    elif not isinstance(p2, Point):
        raise TypeError("The second parameter must be a Point object")
    return p1.in_range(p2, distance, units)


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
    elif len(geometry) == 2:
        min_lat = min(geometry[0].latitude, geometry[1].latitude)
        max_lat = max(geometry[0].latitude, geometry[1].latitude)
        min_lon = min(geometry[0].longitude, geometry[1].longitude)
        max_lon = max(geometry[0].longitude, geometry[1].longitude)

        geo_points = [
            Point(min_lat, min_lon),
            Point(min_lat, max_lon),
            Point(max_lat, max_lon),
            Point(max_lat, min_lon)
        ]
    else:
        for p in geometry:
            if not isinstance(p, Point):
                raise TypeError("All values of geometry must be Point objects")
        
        geo_points = geometry


    # number of times hit an edge
    intersected = 0
    for i in range(len(geo_points)):
        curr = geo_points[i]
        next = geo_points[(i+1) % len(geo_points)]

        if curr.y == next.y:
            continue
        
        if max(curr.y, next.y) >= point.y > min(curr.y, next.y):
            if point.x <= max(curr.x, next.x):
                xinters = (point.y - curr.y)*(next.x-curr.x)/(next.y-curr.y)+curr.x
                if curr.x == next.x or point.x <= xinters:
                    intersected += 1

    # There will be an odd number for points in a geometry, even for those that
    # do not reside in the geometry
    return intersected % 2 == 1
