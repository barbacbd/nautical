class Point:

    """
    A 3D point containing latitude, longitude and altitude coordinates
    """

    __slots__ = ['_latitude', '_longitude', '_altitude']

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """

        :param lat: latitude degrees
        :param lon: Longitude degrees
        :param alt: Altitude meters
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
        """
        :return: latitude (degrees)
        """
        return self._latitude

    @property
    def longitude(self):
        """
        :return: longitude (degrees)
        """
        return self._longitude

    @property
    def altitude(self):
        """
        :return: altitude (meters)
        """
        return self._altitude

    @latitude.setter
    def latitude(self, latitude):
        """
        :param latitude: latitude (degrees) that must fall between -90 and 90
        """
        if isinstance(latitude, float):
            if -90.0 <= latitude <= 90.0:
                self._latitude = float(latitude)

    @longitude.setter
    def longitude(self, longitude):
        """
        :param longitude: longitude (degrees) that must fall between -180 and 80
        """
        if isinstance(longitude, float):
            if -180.0 <= longitude <= 180.0:
                self._longitude = longitude

    @altitude.setter
    def altitude(self, altitude):
        """
        :param altitude: any floating point value is accepted, but all negative values are considered depth
        """
        if isinstance(altitude, float):
            self._altitude = altitude

    def __str__(self) -> str:
        """
        Python version of the to string function. Turn this object into a string

        :return: string representation of this object
        """
        return "{}, {}, {}".format(self._latitude, self._longitude, self.altitude)

    def __hash__(self):
        """
        Each 3D point should be unique and there can only be one 3D point in the world that matches lat, lon, alt

        :return: hash of the latitude * longitude * altitude
        """
        _h = [x for x in (self.latitude, self.longitude, self.altitude) if x != 0.0]

        _prod = 1.0
        for _i in _h:
            _prod *= _i

        return hash(str(_prod))

    def parse(self, data: str) -> None:
        """
        :param data: A string containing (whitespace ignored and not a delimiter) lat, lon, altitude.

        .. note::
            If data is comma separated it is parsed as lon, lat, alt [altitude is optional -> default to 0.0].

        Ex: -110.123, 76.45, 0.0
        Ex: -110.123, 76.45
        """
        if data:
            """ Remove all whitespace and lower case the value"""
            data = data.lower()
            data = "".join(data.split())
            split_data = data.split(",")

            try:
                self.longitude = float(split_data[0])  # should ALWAYS exist
                self.latitude = float(split_data[1])   # should ALWAYS exist
                if len(split_data) > 2:
                    self.altitude = float(split_data[2])   # may or may not exist
            except (IndexError, TypeError) as e:
                raise # save stack information
