"""
Author: barbacbd
"""
from nautical.time.conversion import convert_noaa_time
from nautical.time.nautical_time import nTime
from time import mktime, strptime
from datetime import datetime


class BuoyData(object):

    """
    mm        : month                : int
    dd        : day                  : int
    time      : time                 : nautical.time.nautical_time.nTime
    wdir      : wind direction       : string
    wspd      : wind speed           : kts
    gst       : gust                 : kts
    wvht      : wave height          : feet
    dpd       : dominant wave period : seconds
    apd       : average wave period  : seconds
    mwd       : mean wave direction  : string
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
    swd       : swell direction      : string
    wwh       : wind wave height     : feet
    wwp       : wind wave period     : seconds
    wwd       : wind wave direction  : string
    steepness : steepness            : string
    """

    def __init__(self):
        """

        """
        # split the docstring into something a bit more readable for later
        # (variable name, description, units)
        self._lookup = []
        if self.__doc__:
            for line in self.__doc__.split("\n"):
                if line:
                    _split = [str(x.strip()) for x in line.split(":")]

                    if len(_split) == 3:
                        self._lookup.append(_split)

        # save the year when you initialize the instance
        self.year = int(datetime.now().year)

        self.mm = 0
        self.dd = 0
        self.time = None

        self.wdir = None       # str
        self.wspd = 0          # KTS
        self.gst = 0           # KTS
        self.wvht = 0          # Feet
        self.dpd = 0           # Seconds
        self.apd = 0           # Seconds
        self.mwd = None        # str
        self.pres = 0          # Inches
        self.ptdy = 0          # Inches
        self.atmp = 0          # Degrees F
        self.wtmp = 0          # Degrees F
        self.dewp = 0          # Degrees F
        self.sal = 0           # PSU
        self.vis = 0           # Nautical Miles
        self.tide = 0          # Feet

        self.swh = 0           # Feet
        self.swp = 0           # Seconds
        self.swd = None        # str
        self.wwh = 0           # Feet
        self.wwp = 0           # Seconds
        self.wwd = None        # str
        self.steepness = None  # str

    @property
    def epoch_time(self):
        if self.year and self.mm and self.dd and self.time:
            date = '{}-{}-{} {}'.format(self.year, self.mm, self.dd, str(self.time))
            pattern = '%Y-%m-%d %H:%M:%S'
            return int(mktime(strptime(date, pattern)))
        else:
            return 0

    def __iter__(self):
        """
        Provide a user friendly mapping of variable names to values stored in this
        NOAA Data Object
        """
        for entry in self._lookup:
            yield "{} ({})".format(entry[1], entry[2]), getattr(self, entry[0])

    def from_dict(self, d: {}):
        """
        Fill this structure from a dictionary
        """
        [self.set(k, v) for k, v in d.items()]

    def set(self, key, value):
        """
        :param key: the internal variable name
        :param value: the value we wish to set the variable to
        """
        if hasattr(self, key):
            if "time" == key:
                if isinstance(value, str):
                    setattr(self, key, convert_noaa_time(value))
                elif isinstance(value, nTime):
                    setattr(self, key, value)
            else:
                setattr(self, key, value)

    def __getattr__(self, item):
        """
        Not currently overriding
        """
        return super(BuoyData, self).__getattribute__(item)
