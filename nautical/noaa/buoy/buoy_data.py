"""
Author: barbacbd
"""
from nautical.time.conversion import convert_noaa_time
from nautical.time.nautical_time import nTime
from time import mktime, strptime
from datetime import datetime
from . import UNAVAILABLE_NOAA_DATA


class BuoyData(object):

    """
    mm        : month
    dd        : day
    year      : year
    time      : time
    wdir      : wind direction
    wspd      : wind speed           : kts
    gst       : gust                 : kts
    wvht      : wave height          : feet
    dpd       : dominant wave period : seconds
    apd       : average wave period  : seconds
    mwd       : mean wave direction
    pres      : pressure             : inches
    ptdy      : pressure tendency    : inches
    atmp      : air temp             : Degrees F
    wtmp      : water temp           : Degrees F
    dewp      : dew point            : Degrees F
    sal       : salinity             : PSU
    vis       : visibility           : NM
    tide      : tide                 : feet
    swh       : swell height         : feet
    swp       : swell period         : seconds
    swd       : swell direction
    wwh       : wind wave height     : feet
    wwp       : wind wave period     : seconds
    wwd       : wind wave direction
    steepness : steepness
    """

    __slots__ = [
        '_lookup',
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
        # split the docstring into something a bit more readable for later
        # (variable name, description, units)
        self._lookup = []
        if self.__doc__:
            for line in self.__doc__.split("\n"):
                if line:
                    self._lookup.append([str(x.strip()) for x in line.split(":")])

        self.year = int(datetime.now().year)
        self.mm = int(datetime.now().month)
        self.dd = int(datetime.now().day)
        self.time = None

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
        for entry in self._lookup:
            if not getattr(self, entry[0], None):
                continue

            if len(entry) == 2:
                yield "{}: {}".format(entry[1], getattr(self, entry[0]))
            elif len(entry) == 3:
                yield "{}: {} {}".format(entry[1], getattr(self, entry[0]), entry[2])

    def from_dict(self, d: {}):
        """
        Fill this structure from a dictionary
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
