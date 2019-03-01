
def valid_lat(lat) -> bool:
    """
    return true if the latitude value is valid
    :param lat: latitude to check
    :return: bool
    """
    return -90.0 <= lat <= 90.0


def valid_lon(lon) -> bool:
    """
    return true if the longitude value is valid
    :param lon: longitude value
    :return: bool
    """
    return -180.0 <= lon <= 180.0


class Point:

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """
        A 3D point containing a latitude, longitude and altitude coordinate
        :param lat: latitude value
        :param lon: longitude value
        :param alt: altitude value
        """
        self.lat = 0.0
        self.lon = 0.0

        self.set_latitude(lat)
        self.set_longitude(lon)
        self.alt = alt

    def set_latitude(self, lat) -> None:
        """
        Set the latitude value if it is valid, if it is not valid use the previous value, if there
        was not one set, default to 0.0
        :param lat: latitude value
        :return: none
        """
        self.lat = lat if valid_lat(lat) else self.lat if self.lat else 0.0

    def set_longitude(self, lon) -> None:
        """
        Set the longitude value if it is valid, if it is not valid use the previous value, if there
        was not one set, default to 0.0
        :param lon: longitude value
        :return: none
        """
        self.lon = lon if valid_lon(lon) else self.lon if self.lon else 0.0

    def parse(self, data: str) -> None:
        """
        Read in a string contain lat, lon, altitude. Note, all whitespace is ignored but it is NOT a delimiter

        If data is comma separated it is parsed as lat, lon, alt [altitude is optional -> default to 0.0].

        Ex: 76.45, -110.123, 0.0
        Ex: 76.45, -110.123

        If the data is colon separated with commas, a string identifier should be added to denote the field, AND the
        arguments should be comma delimited

        Ex: Lat: 76.45, LONGITUDE: -110.123, AltitudE: 0.0

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
            if ":" in data:

                for x in split_data:
                    kv = x.split(":")

                    if len(kv) == 2:
                        if 'lat' in kv[0]:
                            try:
                                self.set_latitude(float(kv[1]))
                            except ValueError:
                                pass
                        elif 'lon' in kv[0]:
                            try:
                                self.set_longitude(float(kv[1]))
                            except ValueError:
                                pass
                        elif 'alt' in kv[0]:
                            try:
                                self.alt = float(split_data[2])
                            except ValueError:
                                pass
            else:
                if len(split_data) == 2:
                    """" Latitude, Longitude """
                    try:
                        lat = float(split_data[0])
                        self.set_latitude(lat)
                    except ValueError:
                        pass

                    try:
                        lon = float(split_data[1])
                        self.set_longitude(lon)
                    except ValueError:
                        pass
                elif len(split_data) == 3:
                    """ Latitude, Longitude, Altitude"""
                    try:
                        lat = float(split_data[0])
                        self.set_latitude(lat)
                    except ValueError:
                        pass

                    try:
                        lon = float(split_data[1])
                        self.set_longitude(lon)
                    except ValueError:
                        pass

                    try:
                        self.alt = float(split_data[2])
                    except ValueError:
                        pass
