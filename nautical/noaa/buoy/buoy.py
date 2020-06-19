from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.error import NauticalError
from nautical.location.point import Point


class Buoy:

    """
    This class is meant to serve as the combination of past and present NOAA
    data for a particular buoy location. This will will include:

    present wave data
    present swell data
    past data [currently wave data and swell data]
    """

    def __init__(self, station, description: str = None, location=None) -> None:
        """
        :param station: ID of the station
        :param description: snippet of information to describe this station
        :param location: nautical.location.point.Point [optional]
        """
        self._station = station

        self._description = description

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
    def description(self):
        """
        Don't provide the user with public means of altering
        the description once it is created.
        """
        return self._description

    @property
    def location(self):
        """
        Location (nuatical.location.point) of the buoy
        """
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
        return self._past

    @past.setter
    def past(self, p):
        """
        The user may pass in a single instance of NOAAData or a list of these
        objects to fill in the past data with.

        :param p: list or since instance of BuoyData that is used to fill in the past
        """
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
            return str(self._station)
        else:
            return "{} at {}".format(self._station, str(self._location))

    def __eq__(self, other):
        """
        :return: station id is the same
        """
        return type(self) == type(other) and self._station == other.station

    def __ne__(self, other):
        """
        :return: station ids are not the same
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        The reason behind a private station and description is that they are used for the
        hash function. The hash shouldn't be able to change during execution.

        :return: hash of the station combined with the hash of the description.
        """
        return hash(str(self._station)) * hash(self._description) if self._description else hash(str(self._station))
