

class WaveData:

    def __init__(self) -> None:
        """
        Member Variables According to the table on NOAA's buoy website
        """
        self.mm = None # Month
        self.dd = None # Day
        self.time = None # EST
        self.wdir = None # Wind direction deg
        self.wspd = None # wind speed kts
        self.gst = None # gust kts
        self.wvht = None # wave height ft
        self.dpd = None  # sec
        self.apd = None # sec
        self.mwd = None
        self.pres = None # inches
        self.ptdy = None # inches
        self.atmp = None # degrees F
        self.wtmp = None  # degrees F
        self.dewp = None # degrees F
        self.sal = None # psu
        self.vis = None # nmi
        self.tide = None # ft


class DetailedData:

    def __init__(self) -> None:
        """
        Member Variables for the detailed NOAA data over the last 5 hours
        """
        self.wvht = None # significant wave height
        self.swh = None # swell height
        self.swp = None # swell period
        self.swd = None # swell direction
        self.wwh = None # wind wave height
        self.wwp = None # wind wave period
        self.wwd = None # wind wave direction
        self.steepness = None # wave steepness
        self.apd = None # average wave period