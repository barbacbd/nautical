"""
Author: barbacbd
"""

from nautical.error import NauticalError
from nautical.time.conversion import convert_noaa_time

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

    def __call__(self, *args, **kwargs):
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
        if var:
            internal_var = self.var_table.get(var.lower(), None)
            if internal_var:

                value = kwargs.get("value", None)

                if "_time" in internal_var and isinstance(value, str):
                    setattr(self, internal_var, convert_noaa_time(value))
                else:
                    setattr(self, internal_var, value)

    @property
    def station(self):
        return self._station

    def __str__(self):
        """
        Short description of the NOAA Data, the station id provides the
        user with the required information for further lookup.
        """
        return "{}/{} : {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n"\
            .format(
                self._month, self._day, self._time,
                self._wind_direction,
                self._wind_speed,
                self._gust,
                self._wave_height,
                self._dominant_wave_period,
                self._average_wave_period,
                self._mean_wave_direction,
                self._pressure,
                self._pressure_tendency,
                self._air_temp,
                self._water_temp,
                self._dew_point,
                self._salinity,
                self._visibility,
                self._tide,
                self._swell_height,
                self._swell_period,
                self._swell_direction,
                self._wind_wave_height,
                self._wind_wave_period,
                self._wind_wave_direction,
                self._steepness,
            )

    def __repr__(self):
        """
        The long description of the NOAA Data object
        """
        return "Data for NOAA Buoy {}".format(self._station)


class CombinedNOAAData:

    def __init__(self) -> None:
        """
        This class is meant to serve as the combination of past and present NOAA
        data for a particular buoy location. This will will include:

        present wave data
        present swell data
        past data [currently wave data and swell data]
        """
        self.present_wave_data = None
        self.present_swell_data = None
        self.past_data = None




