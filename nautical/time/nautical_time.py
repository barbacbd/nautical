"""
Author: barbacbd
Date:   4/18/2020
"""
from .enums import TimeFormat, Midday


class nTime(object):

    __slots__ = ['_format', '_midday', '_minutes', '_hours']

    def __init__(self, fmt: TimeFormat = TimeFormat.HOUR_12):
        """
        Nautical Time (nTime) is a class to Keep Track of Time read in from
        NOAA data. The time can be converted to 24 or 12 hour time formats.
        """
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
        """
        Make sure that the hours are valid. If the time is afternoon
        but the hours are less than 12 in a 12-hour format add 12 to
        convert to the 24 hour format, all other values are considered valid
        """
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
        """
        Return the 24 hour version of the hour and minutes. This class does not
        deal in seconds as the seconds are not provided by NOAA.
        """
        if self._format in (TimeFormat.HOUR_12, ):
            hours, midday = self.hours
            h = hours + 12 if midday in (Midday.PM, ) else hours
            return "{:02d}:{:02d}:00".format(h, self.minutes)
        else:
            return "{:02d}:{:02d}:00".format(self.hours, self.minutes)


