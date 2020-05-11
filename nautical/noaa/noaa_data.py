"""
Author: barbacbd
"""

from nautical.error import NauticalError
from nautical.time.conversion import convert_noaa_time
from . import UNAVAILABLE_NOAA_DATA
from time import mktime, strptime
from datetime import datetime


class NOAAData(object):

    """
    Lookup table to associate the variable name from NOAA's table on each
    web page to the variable name inside of this class.
    """
    var_table = {
        "mm":        "_month",
        "dd":        "_day",
        "time":      "_time",
        "wdir":      "_wind_direction",
        "wspd":      "_wind_speed",
        "gst":       "_gust",
        "wvht":      "_wave_height",
        "dpd":       "_dominant_wave_period",
        "apd":       "_average_wave_period",
        "mwd":       "_mean_wave_direction",
        "pres":      "_pressure",
        "ptdy":      "_pressure_tendency",
        "atmp":      "_air_temp",
        "wtmp":      "_water_temp",
        "dewp":      "_dew_point",
        "sal":       "_salinity",
        "vis":       "_visibility",
        "tide":      "_tide",
        "swh":       "_swell_height",
        "swp":       "_swell_period",
        "swd":       "_swell_direction",
        "wwh":       "_wind_wave_height",
        "wwp":       "_wind_wave_period",
        "wwd":       "_wind_wave_direction",
        "steepness": "_steepness"
    }

    def __init__(self,
                 station=None
                 ):
        """
        :param station: NOAA Station ID
        """
        try:
            self._station = str(station)
        except TypeError as e:
            raise NauticalError(e)

        self._reverse_lookup = {v: k for k, v in self.var_table.items()}

        # save the year when you initialize the instance
        self._year = int(datetime.now().year)

        self._month = 0
        self._day = 0
        self._time = None

        self._wind_direction = None       # str
        self._wind_speed = 0              # KTS
        self._gust = 0                    # KTS
        self._wave_height = 0             # Feet
        self._dominant_wave_period = 0    # Seconds
        self._average_wave_period = 0     # Seconds
        self._mean_wave_direction = None  # str
        self._pressure = 0                # Inches
        self._pressure_tendency = 0       # Inches
        self._air_temp = 0                # Degrees F
        self._water_temp = 0              # Degrees F
        self._dew_point = 0               # Degrees F
        self._salinity = 0                # PSU
        self._visibility = 0              # Nautical Miles
        self._tide = 0                    # Feet

        self._swell_height = 0            # Feet
        self._swell_period = 0            # Seconds
        self._swell_direction = None      # str
        self._wind_wave_height = 0        # Feet
        self._wind_wave_period = 0        # Seconds
        self._wind_wave_direction = None  # str
        self._steepness = None            # str

    @property
    def epoch_time(self):
        if self._year and self._month and self._day and self._time:
            date = '{}-{}-{} {}'.format(self._year, self._month, self._day, str(self._time))
            pattern = '%Y-%m-%d %H:%M:%S'
            return int(mktime(strptime(date, pattern)))
        else:
            return 0

    def __iter__(self):
        """
        Provide a user friendly mapping of variable names to values stored in this
        NOAA Data Object
        """
        for k, v in self.var_table.items():
            yield ' '.join(list(filter(None, v.split('_')))), getattr(self, k)

    def descriptors(self):
        """
        Return the descriptors for all users to all of the public variable
        representations of this object
        """
        return {
            k: ' '.join(list(filter(None, v.split('_'))))
            for k, v in self.var_table.items()
        }

    def from_dict(self, d: {}):
        """
        Fill this structure from a dictionary
        """
        [self.update(var=k, value=v) for k, v in d.items()]

    def update(self, *args, **kwargs):
        """
        Instead of using the setattr or specific getter and setter combinations,
        the user can use the () function to pass in args to set the values.
        Note: the units will always be assumed as the comments state in the
        init function.

        Args:
            var: name of the variable that you wish to set. The Class
                 prepares for data to be similar to the data coming
                 directly from noaa. If you wish to set values other than
                 those in the lookup table, please use setattr

            value: value of the variable in question. None by default

        """
        var = kwargs.get("var", None)
        if var and var.lower() in self.var_table:

            i_var = self.var_table[var.lower()]
            value = kwargs.get("value", UNAVAILABLE_NOAA_DATA)

            if value != UNAVAILABLE_NOAA_DATA:

                if "time" in i_var:
                    setattr(self, i_var, convert_noaa_time(value))
                else:
                    setattr(self, i_var, value)

    def __getattr__(self, item):
        """
        Provide the user with the ability to find the public names of internal variables

        Ex:
            a = NOAAData()
            ... fill object ...
            time = getattr(a, "time") find the variable _time inside of this object
        """
        item_lower = item.lower()
        if item_lower in self.var_table:
            return getattr(self, self.var_table[item_lower])
        else:
            return super(NOAAData, self).__getattribute__(item)

    @property
    def station(self):
        return self._station

    def __str__(self):
        """
        The long description of the NOAA Data object
        """
        return "Data for NOAA Buoy {}".format(self._station)
