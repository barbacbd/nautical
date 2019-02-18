

class WaveData:

    """
    month - number
    day - number
    time - (after conversion) hour:minutes am/pm (EST)
    wind direction - degrees
    wind speed - kts
    gust - kts
    wave height - feet
    dominant wave period - sec
    average wave period - sec
    mean wave direction - degrees
    pressure - inches
    pressure tendency - inches
    air temp - Deg F
    water temp - Deg F
    dew point - Deg F
    salinity - PSU
    visibility - nautical miles
    tide - feet
    """

    def __init__(self):
        """
        Member Variables According to the table on NOAA's buoy website
        """
        self.mm = None
        self.dd = None
        self.time = None
        self.wdir = None
        self.wspd = None
        self.gst = None
        self.wvht = None
        self.dpd = None
        self.apd = None
        self.mwd = None
        self.pres = None
        self.ptdy = None
        self.atmp = None
        self.wtmp = None
        self.dewp = None
        self.sal = None
        self.vis = None
        self.tide = None

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


class WaveLocations:

    def __init__(self):
        """
        all locations we are concerned with
        """
        self.vb_id = 44099
        self.kill_devil_hills = 44086
        self.southern_shores_id = 44100
        self.duck_id = 44056
        self.hateras_id = "HCGN7"
        self.wilmington_id = 41110
        self.chincoteague_id = 44089
