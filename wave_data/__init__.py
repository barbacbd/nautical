

class WaveData:

    def __init__(self):
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

    def convert_time(self):
        """
        Convert the time value to a more readable time
        :return: none
        """
        if self.time:
            sp = self.time.split(";")
            am_pm = sp[1]
            time = sp[0].split("&")[0]

            self.time = "{} {}".format(time, am_pm)

    def to_string(self):
        """
        Convert all wave date to one long string
        :return: String representation of the wave data
        """
        header = "{}-{} {}\n".format(self.mm, self.dd, self.time)
        wind = "Wind DIR = {} SPD = {} GUST = {}\n".format(self.wdir, self.wspd, self.gst)
        waves = "Wave HT = {} Dominant Wave Period = {} Avg Wave Period = {} Mean Wave Direction\n".format(
            self.wvht, self.dpd, self.apd, self.mwd)
        other = "Pressure = {} Pressure Tendency = {} Air Temp = {} Water Temp = {} Dew Point = {}\n".format(
            self.pres, self.ptdy, self.atmp, self.wtmp, self.dewp)
        water = "Salinity = {} Visibility = {} Tide = {}\n".format(self.sal, self.vis, self.tide)

        return "{}{}{}{}{}".format(header, wind, waves, other, water)


class DetailedData:

    def __init__(self):
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
