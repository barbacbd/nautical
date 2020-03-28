from math import sin, cos, sqrt, radians, atan2
from logging import getLogger


log = getLogger(__name__)


class Point:

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """
        A 3D point containing latitude, longitude and altitude coordinates
        """
        self._latitude = 0.0
        self._longitude = 0.0
        self._altitude = 0.0

        # use the protected setters
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def altitude(self):
        return self._altitude

    @latitude.setter
    def latitude(self, latitude):
        try:
            if -90.0 <= float(latitude) <= 90.0:
                self._latitude = float(latitude)
        except Exception:
            pass

    @longitude.setter
    def longitude(self, longitude):
        try:
            if -180.0 <= float(longitude) <= 180.0:
                self._longitude = float(longitude)
        except Exception:
            pass

    @altitude.setter
    def altitude(self, altitude):
        try:
            self._altitude = float(altitude)
        except Exception:
            pass

    def __str__(self) -> str:
        """
        Python version of the to string function. Turn this object into a string
        :return: string representation of this object
        """
        return "[{}, {}, {}]".format(self._latitude, self._longitude, self.altitude)

    def parse(self, data: str) -> None:
        """
        Read in a string contain lat, lon, altitude. Note, all whitespace is ignored but it is NOT a delimiter

        If data is comma separated it is parsed as lon, lat, alt [altitude is optional -> default to 0.0].
        NOTE: NOAA data is in the form LON, LAT

        Ex: -110.123, 76.45, 0.0
        Ex: -110.123, 76.45

        If the data is colon separated with commas, a string identifier should be added to denote the field, AND the
        arguments should be comma delimited

        Ex: Lat: 76.45, LONGITUDE: -110.123, Altitude: 0.0

        Note: the spelling does not matter

        Values that can be parsed AND are valid will be set, Other values will REMAIN

        :param data: String to be parsed
        :return: None, the values are set internally
        """
        if data:
            """ Remove all whitespace and lower case the value"""
            data = data.lower()
            data = "".join(data.split())
            split_data = data.split(",")

            print(split_data)

            if len(split_data) == 2:
                """" Latitude, Longitude """
                self.longitude = split_data[0]
                self.latitude = split_data[1]
            elif len(split_data) == 3:
                """ Latitude, Longitude, Altitude"""
                self.longitude = split_data[0]
                self.latitude = split_data[1]
                self.altitude = split_data[2]
