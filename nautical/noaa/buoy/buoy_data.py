from nautical.time.conversion import convert_noaa_time
from nautical.time.nautical_time import nTime
from nautical.time.enums import TimeFormat
from time import mktime, strptime
from datetime import datetime
from nautical.units import *
from typing import Dict, Any


# Not sure why but this is the default value for NOAA data that is not present.
# There may be times where we check against this value for validity/availability
UNAVAILABLE_NOAA_DATA = "-"


def _find_parameter_units(key: str) -> str:
    """
    Function that will attempt to find the units associated with the key. If 
    no units are found, None is returned.

    :param key: Name of the parameter

    :return: string of the type of units if there are units associated with the 
    parameter.
    """
    return {
        "wspd": SpeedUnits.KNOTS,
        "gst": SpeedUnits.KNOTS,
        "wvht": DistanceUnits.FEET,
        "dpd": TimeUnits.SECONDS,
        "apd": TimeUnits.SECONDS,
        "pres": PressureUnits.PSI,
        "ptdy": PressureUnits.PSI,
        "atmp": TemperatureUnits.DEG_F,
        "wtmp": TemperatureUnits.DEG_F,
        "dewp": TemperatureUnits.DEG_F,
        "sal": SalinityUnits.PSU,
        "vis": DistanceUnits.NAUTICAL_MILES,
        "tide": DistanceUnits.FEET,
        "swh": DistanceUnits.FEET,
        "swp": TimeUnits.SECONDS,
        "wwh": DistanceUnits.FEET,
        "wwp": TimeUnits.SECONDS
    }.get(key, None)


class BuoyData(object):

    __slots__ = [
        # time/date data
        'year', 'mm', 'dd', 'time',
        # detailed wave summary data
        'wdir', 'wspd', 'gst', 'wvht', 'dpd', 'apd', 'mwd', 'pres',
        'ptdy', 'atmp', 'wtmp', 'dewp', 'sal', 'vis', 'tide',
        # swell data
        'swh', 'swp', 'swd', 'wwh', 'wwp', 'wwd', 'steepness', 
        # new support
        'chill'
    ]

    def __init__(self):
        """
        Class to contain all information included in a NOAA data point for
        a buoy. A buoy can also include weather stations.
        """
        # initialize all slots to None
        for x in self.__slots__:
            setattr(self, x, None)

        # set the time for this buoy data to NOW
        self.year = int(datetime.now().year)
        self.mm = int(datetime.now().month)
        self.dd = int(datetime.now().day)

        # initialize the time in the case of Present data, we can always correct this later
        self.time = nTime(fmt=TimeFormat.HOUR_24)
        self.time.minutes = 30 if int(datetime.now().minute) > 30 else 0
        self.time.hours = int(datetime.now().hour)

    @property
    def epoch_time(self):
        """
        :return: epoch time if all pieces of the time object exist, otherwise None
        """
        if self.year and self.mm and self.dd and self.time:
            date = '{}-{}-{} {}'.format(self.year, self.mm, self.dd, str(self.time))
            pattern = '%Y-%m-%d %H:%M:%S'
            return int(mktime(strptime(date, pattern)))
        else:
            return 0

    def __iter__(self):
        """
        Provide a user friendly mapping of variable names to values stored in this
        Buoy Data Object
        """
        for entry in self.__slots__:
            val = getattr(self, entry, None)

            if val:
                yield entry, val

    def from_dict(self, d: Dict[str, Any]):
        """
        Fill this object from the data stored in a dictionary where 
        the key should match a slot or object variable

        :param d: Dictionary containing the data about this buoy
        """
        for k, v in d.items():
            self.set(k, v)

    def set(self, key, value):
        """
        :param key: the internal variable name
        :param value: the value we wish to set the variable to
        """
        if isinstance(value, str) and UNAVAILABLE_NOAA_DATA == value.strip():
            return

        if "time" == key:
            if isinstance(value, str):
                setattr(self, key, convert_noaa_time(value))
            elif isinstance(value, nTime):
                setattr(self, key, value)
        else:
            setattr(self, key, value)
