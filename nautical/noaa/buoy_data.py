"""
Author: barbacbd
"""
from .noaa_data import NOAAData
from nautical.error import NauticalError


class BuoyWorkup:

    def __init__(self, station) -> None:
        """
        This class is meant to serve as the combination of past and present NOAA
        data for a particular buoy location. This will will include:

        present wave data
        present swell data
        past data [currently wave data and swell data]
        """
        self._station = station

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
    def present(self):
        return self._present

    @present.setter
    def present(self, p):
        """
        If this instance of present data is a NOAAData object and the time is
        more recent that the previous present data, then the old present data
        is moved to the past data and the new instance is kept as the present data.
        """
        if isinstance(p, NOAAData):
            if p.station == self._station:

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
        if isinstance(p, NOAAData):
            self._update_past(p)
        elif isinstance(p, list):
            [self._update_past(x) for x in p if isinstance(x, NOAAData)]

    def _update_past(self, p):
        """
        Attempt to update the past data, but make sure that this particular
        NOAA data does not already have a time entry that matches.
        """
        if p.station == self._station:
            data = next((x for x in self._past if x.epoch_time == p.epoch_time), None)

            if not data:
                self._past.append(data)

