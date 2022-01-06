from .enums import TimeFormat, Midday


class nTime(object):

    """
     Nautical Time (nTime) is a class to Keep Track of Time read in from
     NOAA data. The time can be converted to 24 or 12 hour time formats.
    """

    __slots__ = ['_format', '_midday', '_minutes', '_hours']

    def __init__(self, fmt: TimeFormat = TimeFormat.HOUR_12):
        """
        :param fmt: format for the time 12 vs 24 hour (default is TimeFormat.HOUR_12)
        """
        self._format = fmt
        self._midday = None
        self._minutes = 0
        self._hours = 0

    @property
    def minutes(self):
        """
        :return: current minutes
        """
        return self._minutes

    @property
    def hours(self):
        """
        :return: current hour (am/pm if exists)
        """
        if self._midday:
            return self._hours % self._format.value, self._midday
        else:
            return self._hours % self._format.value

    @property
    def fmt(self):
        """
        :return: current format (12 vs 24 hour)
        """
        return self._format

    @fmt.setter
    def fmt(self, val):
        """
        Adjust the hours and the midday (meridian) value accordingly

        :param val: TimeFormat that should be different that the current format.
        """
        if isinstance(val, TimeFormat) and val != self._format:
            if val == TimeFormat.HOUR_12:
                if self._hours >= 12:
                    self._hours -= 12
                    self._midday = Midday.PM
                else:
                    self._midday = Midday.AM

            elif val == TimeFormat.HOUR_24:
                self._hours = self._hours + 12 if self._midday == Midday.PM else self._hours
                self._midday = None

    @minutes.setter
    def minutes(self, minutes):
        """
        :param minutes: minutes provided should be no less than 0 and no greater than 59
        """
        if 0 <= minutes <= 59:
            self._minutes = minutes

    @hours.setter
    def hours(self, data):
        """
        Make sure that the hours are valid. If the time is afternoon
        but the hours are less than 12 in a 12-hour format add 12 to
        convert to the 24 hour format, all other values are considered valid

        :param data: tuple or single value containing (hours, midday enumeration)
        """
        hours = None
        m = None
        if isinstance(data, (tuple, list)):
            if len(data) == 2:
                hours, m = data

        if None in (hours, m):
            hours = data
            # provide a default value
            m = Midday.AM if hours < 12 else Midday.PM

        if 0 <= hours < 24:
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

        :return: string representation of the time
        """
        if self._format in (TimeFormat.HOUR_12, ):
            hours, midday = self.hours
            h = hours + 12 if midday in (Midday.PM, ) else hours
            return "{:02d}:{:02d}:00".format(h, self.minutes)
        else:
            return "{:02d}:{:02d}:00".format(self.hours, self.minutes)


