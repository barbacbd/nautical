from __future__ import annotations

from haversine import Unit, haversine

from nautical.exceptions import DistanceCalculationError, UnsupportedConversionError
from nautical.log import get_logger
from nautical.units import DistanceUnits

log = get_logger(__name__)


class Point:
    """A 3D point containing latitude, longitude and altitude coordinates."""

    def __init__(self, lat: float = 0.0, lon: float = 0.0, alt: float = 0.0) -> None:
        """The latitude, longitude, and altitude are supplied to
        the base class as the x, y, z parameters respectively.
        """
        self._latitude = lat
        self._longitude = lon
        self._altitude = alt

    @property
    def latitude(self) -> float:
        """Latitude Property (degrees)
        :return: latitude (degrees)
        """
        return self._latitude

    @property
    def longitude(self) -> float:
        """Longitude Property (degrees)
        :return: longitude (degrees)
        """
        return self._longitude

    @property
    def altitude(self) -> float:
        """Altitude Property (meters)
        :return: altitude (meters)
        """
        return self._altitude

    @property
    def x(self) -> float:
        return self._latitude

    @property
    def y(self) -> float:
        return self._longitude

    @property
    def z(self) -> float:
        return self._altitude

    def as_tuple(self) -> tuple[float, float]:
        """Get the values of the object as a simple tuple. The
        lat and lon are used but not the altitude. The altitude
        is omitted for use with haverine.

        :return: Tuple of lat, lon
        """
        return self.latitude, self.longitude

    def __str__(self) -> str:
        """Python version of the to string function. Turn this object into a string

        :return: string representation of this object
        """
        return f"{self.x}, {self.y}, {self.z}"

    def to_json(self) -> dict[str, float]:
        """Convert the instance to a json dictionary"""
        return {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "altitude": self._altitude,
        }

    @staticmethod
    def from_json(json_dict: dict[str, float]) -> "Point":
        """Fill the instance from a json dictionary"""
        loc = Point()
        loc.from_dict(json_dict)
        return loc

    def from_dict(self, point_dict: dict[str, float]) -> None:
        """Fill the instance from a json dictionary"""
        self._latitude = point_dict.get("latitude", self._latitude)
        self._longitude = point_dict.get("longitude", self._longitude)
        self._altitude = point_dict.get("altitude", self._altitude)

    def distance(self, other: "Point", units: DistanceUnits = DistanceUnits.METERS) -> float:
        """Get the distance using the Haversine function. The function will
        determine the distance between this instance and another `Point`.

        :param other: The other `Point`
        :param units: Units used for measurement
        :return: Distance between the points in units specified
        """
        if not isinstance(units, DistanceUnits):
            raise DistanceCalculationError(f"DistanceUnits not found: {str(type(units))}")
        if not isinstance(other, Point):
            raise DistanceCalculationError("Distance should be calculated between two points")

        if units == DistanceUnits.CENTIMETERS:
            raise UnsupportedConversionError("Centimeters not accepted")

        hav_units = getattr(Unit, str(units.name), Unit.METERS)
        log.debug("haversine executed with units: %s", hav_units.name)

        return haversine(self.as_tuple(), other.as_tuple(), hav_units)

    def in_range(self, other: "Point", distance: float, units: DistanceUnits = DistanceUnits.METERS) -> bool:
        """Deteremine if the points are within a specific distance of eachother.

        :param other: The other `Point`
        :param distance: Max distance between the points
        :param units: Units used for measurement
        :return: True when points are within the specified distance
        """
        try:
            return self.distance(other, units) <= distance
        except TypeError as error:
            log.error(error)
            return False

    @staticmethod
    def parse(data: str) -> "Point":
        """Parse the string containing lon, lat, alt [optional] values respectively.

        :param data: A string containing lon, lat, altitude.
        :return: instance of Point on success, None on failure
        """
        try:
            data = data.lower()
            split_data = data.split(",")

            # flip positions to lat, lon
            args = [float(split_data[1].strip()), float(split_data[0].strip())]
            if len(split_data) > 2:
                # add altitude if exists
                args.append(float(split_data[2].strip()))
            return Point(*args)

        except (IndexError, TypeError) as error:
            log.error(error)
            raise  # save stack information

    @staticmethod
    def parse_noaa_kml_format(data: str) -> "Point":
        """Parse the string containing lon, lat, alt [optional] values respectively.
        See `Point.parse` for implementation and notes.
        """
        return Point.parse(data)
