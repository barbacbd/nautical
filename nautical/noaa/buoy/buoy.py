"""
Author: barbacbd
"""
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.error import NauticalError
from nautical.location.point import Point


class Buoy:

    def __init__(self, station, location=None) -> None:
        """
        This class is meant to serve as the combination of past and present NOAA
        data for a particular buoy location. This will will include:

        present wave data
        present swell data
        past data [currently wave data and swell data]

        :param station: ID of the station
        :param location: nautical.location.point.Point [optional]

        """
        self._station = station

        self._location = None
        if location:
            self.location = location

        self._present = None
        self._past = []

    @property
    def station(self):
        """
        Don't provide the user with public means of altering
        the station once it is created.
        """
        return self._station

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, l):
        """
        Force the user to add a location as a Point object
        :param l: location of this buoy/station
        """
        if isinstance(l, Point):
            self._location = l

    @property
    def present(self):
        return self._present

    @present.setter
    def present(self, p):
        """
        If this instance of present data is a NOAAData object and the time is
        more recent that the previous present data, then the old present data
        is moved to the past data and the new instance is kept as the present data.
        """
        if isinstance(p, BuoyData):
            if self._present:
                if p.epoch_time > self._present.epoch_time:
                    self._update_past(self._present)
                else:
                    raise NauticalError("Failed to set present data, time is in the past.")

            self._present = p

    @property
    def past(self):
        return self._past

    @past.setter
    def past(self, p):
        """
        The user may pass in a single instance of NOAAData or a list of these
        objects to fill in the past data with.
        """
        if isinstance(p, BuoyData):
            self._update_past(p)
        elif isinstance(p, list):
            [self._update_past(x) for x in p if isinstance(x, BuoyData)]

    def _update_past(self, p):
        """
        Attempt to update the past data, but make sure that this particular
        NOAA data does not already have a time entry that matches.
        """
        data = next((x for x in self._past if x.epoch_time == p.epoch_time), None)

        if not data:
            self._past.append(p)

    def __str__(self):
        """
        If the location of this buoy is known return the location and the name,
        otherwise just return the name
        """
        if not self._location:
            return str(self._station)
        else:
            return "{} at {}".format(self._station, str(self._location))

    def __eq__(self, other):
        return type(self) == type(other) and self._station == other.station

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Customize the hash
        """
        return hash(self._station) * hash(id(self))
