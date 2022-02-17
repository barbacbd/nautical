from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.error import NauticalError
from nautical.location.point import Point
from typing import List
from warnings import warn
from copy import copy


class Buoy:

    def __init__(self, station, description: str = None, location=None) -> None:
        """
        :param station: ID of the station
        :param description: snippet of information to describe this station
        :param location: nautical.location.point.Point [optional]
        """
        self.station = station
        self.description = description
        self._location: Point = None
        self._present: BuoyData = None
        self._past: List[BuoyData] = []

        if location is not None:
            self.location = location

    @property
    def location(self):
        return copy(self._location)
    
    @location.setter
    def location(self, l):
        if isinstance(l, Point):
            self._location = l

    @property
    def data(self):
        return self.present

    @property
    def present(self):
        return copy(self._present)

    @data.setter
    def data(self, p):
        self.present = p

    @present.setter
    def present(self, p):
        """
        If this instance of present data is a BuoyData object and the time is
        more recent that the previous present data, then the old present data
        is moved to the past data and the new instance is kept as the present data.

        :param p: instance or candidate for present data (BuoyData)
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
        warn("%s past is deprecated" % str(self.__class__.__name__), DeprecationWarning, stacklevel=2)
        return self._past[:]

    @past.setter
    def past(self, p):
        """
        The user may pass in a single instance of NOAAData or a list of these
        objects to fill in the past data with.

        :param p: list or since instance of BuoyData that is used to fill in the past
        """
        warn("%s past is deprecated" % str(self.__class__.__name__), DeprecationWarning, stacklevel=2)
        if isinstance(p, BuoyData):
            self._update_past(p)
        elif isinstance(p, list):
            [self._update_past(x) for x in p if isinstance(x, BuoyData)]

    def _update_past(self, p):
        """
        Attempt to update the past data, but make sure that this particular
        NOAA data does not already have a time entry that matches.

        :param p: Buoy Data attempting to be added to the past information.
        """
        data = next((x for x in self._past if x.epoch_time == p.epoch_time), None)

        if not data:
            self._past.append(p)

    def __str__(self):
        """
        If the location of this buoy is known return the location and the name,
        otherwise just return the name

        :return: string representation of this Buoy
        """
        if not self._location:
            return str(self.station)
        else:
            return "{} at {}".format(self.station, str(self._location))

    def __eq__(self, other):
        """
        The stations are considered equal if their station ID is the same as the
        station IDs are meant to be unique. The special case is `SHIP`.
        """
        return type(self) == type(other) and self.station == other.station

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        The reason behind a private station and description is that they are used for the
        hash function. The hash shouldn't be able to change during execution.

        :return: hash of the station combined with the hash of the description.
        """
        return hash(str(self.station)) * hash(self.description) if self.description else hash(str(self.station))
