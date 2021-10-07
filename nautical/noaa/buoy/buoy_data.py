from nautical.time.conversion import convert_noaa_time
from nautical.time.nautical_time import nTime
from nautical.time.enums import TimeFormat
from time import mktime, strptime
from datetime import datetime


# Not sure why but this is the default value for NOAA data that is not present.
# There may be times where we check against this value for validity/availability
UNAVAILABLE_NOAA_DATA = "-"


class BuoyData(object):

    """
    :param mm: month
    :param dd: day
    :param year: year
    :param time: time
    :param wdir: wind direction
    :param wspd: wind speed, kts
    :param gst: gust, kts
    :param wvht: wave height, feet
    :param dpd: dominant wave period, seconds
    :param apd: average wave period, seconds
    :param mwd: mean wave direction
    :param pres: pressure, inches
    :param ptdy: pressure tendency, inches
    :param atmp: air temp, Degrees F
    :param wtmp: water temp, Degrees F
    :param dewp: dew point, Degrees F
    :param sal: salinity, PSU
    :param vis: visibility, NM
    :param tide: tide, feet
    :param swh: swell height, feet
    :param swp: swell period, seconds
    :param swd: swell direction
    :param wwh: wind wave height, feet
    :param wwp: wind wave period, seconds
    :param wwd: wind wave direction
    :param steepness: steepness
    """

    __slots__ = [
        # time/date data
        'year', 'mm', 'dd', 'time',
        # detailed wave summary data
        'wdir', 'wspd', 'gst', 'wvht', 'dpd', 'apd', 'mwd', 'pres',
        'ptdy', 'atmp', 'wtmp', 'dewp', 'sal', 'vis', 'tide',
        # swell data
        'swh', 'swp', 'swd', 'wwh', 'wwp', 'wwd', 'steepness'
    ]

    def __init__(self):
        """
        Class to contain all information included in a NOAA data point for
        a buoy. A buoy can also include weather stations.
        """
        self.year = int(datetime.now().year)
        self.mm = int(datetime.now().month)
        self.dd = int(datetime.now().day)

        # initialize the time in the case of Present data, we can always correct this later
        self.time = nTime(fmt=TimeFormat.HOUR_24)
        self.time.minutes = 30 if int(datetime.now().minute) > 30 else 0
        self.time.hours = int(datetime.now().hour)

        self.wdir = None       # str
        self.wspd = None       # KTS
        self.gst = None        # KTS
        self.wvht = None       # Feet
        self.dpd = None        # Seconds
        self.apd = None        # Seconds
        self.mwd = None        # str
        self.pres = None       # Inches
        self.ptdy = None       # Inches
        self.atmp = None       # Degrees F
        self.wtmp = None       # Degrees F
        self.dewp = None       # Degrees F
        self.sal = None        # PSU
        self.vis = None        # Nautical Miles
        self.tide = None       # Feet

        self.swh = None        # Feet
        self.swp = None        # Seconds
        self.swd = None        # str
        self.wwh = None        # Feet
        self.wwp = None        # Seconds
        self.wwd = None        # str
        self.steepness = None  # str

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

    @classmethod
    def units(cls, key):
        """
        :param key: internal variable name of this class.
        :return: Units (str) for the variable read from the class docstring. None is returned when units do not exist.
        """
        if cls.__doc__:
            for line in cls.__doc__.split("\n"):
                if line and key in line:

                    sp = line.split(",")
                    if len(sp) > 1:
                        return sp[len(sp) - 1].strip()

                    return None

    def from_dict(self, d: {}):
        """
        :param d: Fill this object from this dictionary
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
