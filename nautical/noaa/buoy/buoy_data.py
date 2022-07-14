from datetime import datetime, timezone
from typing import Dict, Any
from nautical.log import get_logger
from nautical.time.conversion import convert_noaa_time
from nautical.time.nautical_time import NauticalTime
from nautical.time.enums import TimeFormat, Midday
from nautical.units import (
    SpeedUnits,
    DistanceUnits,
    TimeUnits,
    PressureUnits,
    TemperatureUnits, 
    SalinityUnits
)


log = get_logger()

# Not sure why but this is the default value for NOAA data that is not present.
# There may be times where we check against this value for validity/availability
UNAVAILABLE_NOAA_DATA = "-"

# list of known buoy variable names.
buoy_vars = [
    # date/time
    'year', 'mm', 'dd', 'time',
    # wind data
    'wdir', 'wspd', 'gst', 'mwd', 'wspd10m', 'wspd20m',
    # wave data
    'wvht', 'dpd', 'apd', 'wwh', 'wwp', 'wwd',
    'swh', 'swp', 'swd',
    # pressure
    'pres', 'ptdy',
    # temperature
    'atmp', 'wtmp', 'dewp', 'otmp', 'chill', 'heat',
    # salinity
    'sal', 'ph',
    # oxygen
    'o2pct', 'o2ppm',
    # distance
    'depth', 'nmi', 'vis', 'tide',
    # other
    'steepness', 
    'clcon', 'turb', 'cond',
    'srad1', 'swrad', 'lwrad'
]


def _find_parameter_units(key: str) -> str:
    '''Function that will attempt to find the units associated 
    with the key. If no units are found, None is returned.

    :param key: Name of the parameter
    :return: string of the type of units if there are units associated with the parameter.
    '''
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
        "wwp": TimeUnits.SECONDS,
        "otmp": TemperatureUnits.DEG_F,
        "wspd10m": SpeedUnits.KNOTS,
        "wspd20m": SpeedUnits.KNOTS,
        "depth": DistanceUnits.FEET,
    }.get(key, None)


class BuoyData:

    '''Class to contain all information included in a NOAA data
    point for a buoy. A buoy can also include weather stations.
    '''

    __slots__ = buoy_vars

    def __init__(self):
        # initialize all slots to None
        for slot in self.__slots__:
            setattr(self, slot, None)

        # set the time for this buoy data to NOW
        self.year = int(datetime.now().year)
        # pylint: disable=invalid-name
        self.mm = int(datetime.now().month)
        # pylint: disable=invalid-name
        self.dd = int(datetime.now().day)

        # initialize the time in the case of Present data, we can always correct this later
        self.time = NauticalTime(fmt=TimeFormat.HOUR_24)
        self.time.minutes = 30 if int(datetime.now().minute) > 30 else 0
        self.time.hours = int(datetime.now().hour)

    @property
    def epoch_time(self):
        '''Epoch time property. Converts the nautical time to the epoch time. 
        The function assumes that the data is in UTC time. 

        :return: Seconds since the epoch in UTC, 0 on failure
        '''
        if self.year and self.mm and self.dd and self.time:
            # convert the hours values based on the time format
            hours = self.time.hours
            if isinstance(hours, tuple):
                if hours[1] == Midday.PM and hours[0] < 12:
                    hours = hours[0] + 12
                else:
                    hours = hours[0]
            # convert the time using datetime, set the timezone to UTC
            return int(datetime(
                self.year, self.mm, self.dd, hours, self.time.minutes
            ).replace(tzinfo=timezone.utc).timestamp())
        return 0

    def __contains__(self, item):
        '''Returns True when the value exists and is set'''
        return item in self.__slots__ and \
            getattr(self, item, None) is not None

    def __iter__(self):
        '''Provide a user friendly mapping of variable names to values stored 
        in this Buoy Data Object
        '''
        for slot in self.__slots__:
            val = getattr(self, slot, None)

            if val:
                yield slot, val
    
    def to_json(self):
        '''Return the object as a json dict'''
        output = {k: v for k, v in self if k != "time"}
        if self.time:
            output["time"] = str(self.time)
        return output
    
    @staticmethod
    def from_json(json_data):
        '''Fill an instance from the json_data.'''
        bd = BuoyData()
        bd.from_dict(json_data)
        return bd

    def from_dict(self, buoy_data_dict: Dict[str, Any]):
        '''Fill this object from the data stored in a dictionary where 
        the key should match a slot or object variable

        :param buoy_data_dict: Dictionary containing the data about this buoy
        '''
        for key, value in buoy_data_dict.items():
            self.set(key, value)

    def set(self, key, value):
        '''Set a key, value pair. This function is intended to replace
        `__setattr__` for simplcity. The function will also attempt to convert
        the noaa time to a formatted time that is readable.

        :param key: the internal variable name
        :param value: the value we wish to set the variable to
        '''
        if isinstance(value, str) and UNAVAILABLE_NOAA_DATA == value.strip():
            return

        if "time" == key:
            if isinstance(value, str):
                setattr(self, key, convert_noaa_time(value))
            elif isinstance(value, NauticalTime):
                setattr(self, key, value)
        else:
            try:
                setattr(self, key, value)
            except AttributeError as error:
                log.warning(error)
