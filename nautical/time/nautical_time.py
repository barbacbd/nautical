"""
Author: barbacbd
Date:   4/18/2020
"""
from . import TimeFormat, Midday


class nTime(object):

    """
    Nautical Time (nTime) is a class to Keep Track of Time read in from
    NOAA data. The time can be converted to 24 or 12 hour time formats.
    """

    def __init__(self,
                 fmt: TimeFormat = TimeFormat.HOUR_12
                 ):

        self._format = fmt
        self._midday = None
        self._minutes = 0
        self._hours = 0

    @property
    def minutes(self):
        return self._minutes

    @property
    def hours(self):
        if self._midday:
            return self._hours % self._format.value, self._midday
        else:
            return self._hours % self._format.value

    @property
    def fmt(self):
        return self._format

    @minutes.setter
    def minutes(self, minutes):
        if 0 <= minutes <= 59:
            self._minutes = minutes

    @hours.setter
    def hours(self, data):
        # make sure that the hours are valid. If the time is afternoon
        # but the hours are less than 12 in a 12-hour format add 12 to
        # convert to the 24 hour format, all other values are considered valid
        try:
            hours, m = data
        except TypeError as e:
            hours = data
            # provide a default value
            m = Midday.AM

        if 0 <= hours <= 24:
            if self._format in (TimeFormat.HOUR_12, ):
                self._midday = m

            if m in (Midday.PM,) and hours < 12:
                self._hours = hours + 12
            else:
                self._hours = hours

    def __str__(self):
        if self._format in (TimeFormat.HOUR_12, ):

            # in 12-hour time we always format midnight and noon as 12 not 0
            h = self.hours if self._hours > 0 else 12

            return "{}:{} {}".format(
                h,
                self.minutes,
                Midday.AM.name if self._hours < 12 else Midday.PM.name
            )
        else:
            return "{}:{}".format(self.hours, self.minutes)


