from logging import getLogger
from haversine import haversine, Unit
from nautical.units import DistanceUnits


log = getLogger()


class Point:

    '''A 3D point containing latitude, longitude and altitude coordinates.'''

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        '''The latitude, longitude, and altitude are supplied to
        the base class as the x, y, z parameters respectively.
        '''
        self._latitude = lat
        self._longitude = lon
        self._altitude = alt

        # aliases
        self.x = self.latitude
        self.y = self.longitude
        self.z = self.altitude
        
    @property
    def latitude(self):
        '''Latitude Property (degrees)
        :return: latitude (degrees)
        '''
        return self._latitude

    @property
    def longitude(self):
        '''Longitude Property (degrees)
        :return: longitude (degrees)
        '''
        return self._longitude

    @property
    def altitude(self):
        '''Altitude Property (meters)
        :return: altitude (meters)
        '''
        return self._altitude

    def as_tuple(self):
        '''Get the values of the object as a simple tuple. The
        lat and lon are used but not the altitude. The altitude
        is omitted for use with haverine.

        :return: Tuple of lat, lon
        '''
        return self.latitude, self.longitude
    
    def __str__(self) -> str:
        '''
        Python version of the to string function. Turn this object into a string

        :return: string representation of this object
        '''
        return "{}, {}, {}".format(self.latitude, self.longitude, self.altitude)

    def distance(self, other, units = DistanceUnits.METERS):
        '''Get the distance using the Haversine function. The function will
        determine the distance between this instance and another `Point`.
        
        :param other: The other `Point`
        :param units: Units used for measurement
        :return: Distance between the points in units specified
        '''
        if not isinstance(units, DistanceUnits):
            raise TypeError("DistanceUnits not found: {}".format(str(type(units))))
        elif not isinstance(other, Point):
            raise TypeError("Distance should be calculated between two points")
        
        if units == DistanceUnits.CENTIMETERS:
            log.error("haversine does not support units: {}".format(units.name))
            return
        
        hav_units = getattr(Unit, str(units.name), Unit.METERS)
        log.debug("haversine executed with units: {}".format(hav_units))
        
        return haversine(self.as_tuple(), other.as_tuple(), hav_units)

    def in_range(self, other, distance, units = DistanceUnits.METERS):
        '''Deteremine if the points are within a specific distance of eachother.
        
        :param other: The other `Point`
        :param distance: Max distance between the points
        :param units: Units used for measurement
        :return: True when points are within the specified distance
        '''
        try:
            return self.distance(other, units) <= distance
        except TypeError as e:
            log.error(e)
            return False
        
    @staticmethod
    def parse(data):
        '''Parse the string containing lon, lat, alt [optional] values respectively.

        :param data: A string containing lon, lat, altitude.
        :return: instance of Point on success, None on failure
        '''
        try:
            data = data.lower()
            split_data = data.split(",")
            
            # flip positions to lat, lon
            args = [float(split_data[1].strip()), float(split_data[0].strip())]
            if len(split_data) > 2:
                # add altitude if exists
                args.append(float(split_data[2].strip()))
                
            return Point(*args)
                    
        except (IndexError, TypeError) as e:
            log.error(e)
            raise # save stack information

    @staticmethod
    def parse_noaa_kml_format(data):
        '''Parse the string containing lon, lat, alt [optional] values respectively.
        See `Point.parse` for implementation and notes.
        '''
        return Point.parse(data)
