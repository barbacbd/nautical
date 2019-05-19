
class WaveData:

    def __init__(self, **config):
        """
        The following data in this class is stored in an html data table for each buoy on NOAA's website.
        The data should be parsed in any way possible and stored here so that it can be accessed later.

        All of the variables are considered public, so the user can edit them at any point without feeling
        as though the data changes will have effects on the overall execution of their program.

        The dictionary lookup was chosen because the data that NOAA provides could change at any point. Also
        the fields that NOAA has chosen to provide in the table can be null or invalid.

        :param month: number
        :param day: number
        :param time: (after conversion) hour:minutes am/pm (EST)
        :param wdir: wind direction - degrees
        :param wspd: wind speed - kts
        :param  gst: gust - kts
        :param wvht: wave height - feet
        :param dpd: dominant wave period - sec
        :param apd: average wave period - sec
        :param mwd: mean wave direction - degrees
        :param pres: pressure - inches
        :param ptdy: pressure tendency - inches
        :param atmp: air temp - Deg F
        :param wtmp: water temp - Deg F
        :param dewp: dew point - Deg F
        :param sal: salinity - PSU
        :param vis: visibility - nautical miles
        :param tide: feet
        """
        mm = config.get("month", None)
        dd = config.get("day", None)
        time = config.get("time", None)
        wdir = config.get("wdir", None)
        wspd = config.get("wspd", None)
        gst = config.get("gst", None)
        wvht = config.get("wvht", None)
        dpd = config.get("dpd", None)
        apd = config.get("apd", None)
        mwd = config.get("mwd", None)
        pres = config.get("pres", None)
        ptdy = config.get("ptdy", None)
        atmp = config.get("atmp", None)
        wtmp = config.get("wtmp", None)
        dewp = config.get("dewp", None)
        sal = config.get("sal", None)
        vis = config.get("vis", None)
        tide = config.get("tide", None)

        self.mm = mm if isinstance(mm, int) else None
        self.dd = dd if isinstance(dd, int) else None
        self.time = convert_noaa_time(time)

        self.wdir = wdir if isinstance(wdir, float) else None
        self.wspd = wspd if isinstance(wspd, float) else None
        self.gst = gst if isinstance(gst, float) else None

        self.wvht = wvht if isinstance(wvht, float) else None
        self.dpd = dpd if isinstance(dpd, float) else None
        self.apd = apd if isinstance(apd, float) else None
        self.mwd = mwd if isinstance(mwd, float) else None

        self.pres = pres if isinstance(pres, float) else None
        self.ptdy = ptdy if isinstance(ptdy, float) else None
        self.atmp = atmp if isinstance(atmp, float) else None
        self.wtmp = wtmp if isinstance(wtmp, float) else None

        self.dewp = dewp if isinstance(dewp, float) else None
        self.sal = sal if isinstance(sal, float) else None
        self.vis = vis if isinstance(vis, float) else None
        self.tide = tide if isinstance(tide, float) else None

    def __str__(self) -> str:
        """
        Create the python version of to-string, so that all of our can be displayed well
        :return: string representation of this object
        """
        header = ""
        if self.mm and self.dd and self.time:
            header = "{}-{} {}\n".format(self.mm, self.dd, self.time)

        wind = ""
        if self.wdir and self.wspd and self.gst:
            wind = "Wind DIR({}) SPD({}) GST({})\n".format(self.wdir, self.wspd, self.gst)

        waves = ""
        if self.wvht and self.dpd and self.apd and self.mwd:
            waves = "Wave HT({}) DP({}) AP({}) MWD({})\n".format(self.wvht, self.dpd, self.apd, self.mwd)

        other = ""
        if self.pres and self.ptdy and self.atmp and self.wtmp and self.dewp:
            other = "PRES({}) PTDY({}) ATMP({}) WTMP({}) DEWP({})\n".format(
                self.pres, self.ptdy, self.atmp, self.wtmp, self.dewp)

        water = ""
        if self.sal and self.vis and self.tide:
            water = "SAL({}) VIS({}) Tide({})\n".format(self.sal, self.vis, self.tide)

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


class SwellData:

    def __init__(self, **config):
        """
        The following data in this class is stored in an html data table for each buoy on NOAA's website.
        The data should be parsed in any way possible and stored here so that it can be accessed later.

        All of the variables are considered public, so the user can edit them at any point without feeling
        as though the data changes will have effects on the overall execution of their program.

        The dictionary lookup was chosen because the data that NOAA provides could change at any point. Also
        the fields that NOAA has chosen to provide in the table can be null or invalid.

        :param month: number
        :param day: number
        :param time - (after conversion) hour:minutes am/pm (EST)
        :param wdir: wind direction - deg
        :param wvht: wave height - ft
        :param swh: swell height - ft
        :param swp: swell period - sec
        :param swd: swell direction - deg
        :param wwh: wind wave height - ft
        :param wwp: wind wave period - sec
        :param wwd: wind wave direction - deg
        :param steepness: text
        :param apd: average wave period - sec
        """
        mm = config.get("month", None)
        dd = config.get("day", None)
        time = config.get("time", None)
        wvht = config.get("wvht", None)
        swh = config.get("swh", None)
        swp = config.get("swp", None)
        swd = config.get("swd", None)
        wwh = config.get("wwh", None)
        wwp = config.get("wwp", None)
        wwd = config.get("wwd", None)
        steepness = config.get("steepness", None)
        apd = config.get("apd", None)

        self.mm = mm if isinstance(mm, int) else None
        self.dd = dd if isinstance(dd, int) else None
        self.time = convert_noaa_time(time)

        self.wvht = wvht if isinstance(wvht, float) else None
        self.swh = swh if isinstance(swh, float) else None
        self.swp = swp if isinstance(swp, float) else None
        self.swd = swd if isinstance(swd, float) else None

        self.wwh = wwh if isinstance(wwh, float) else None
        self.wwp = wwp if isinstance(wwp, float) else None
        self.wwd = wwd if isinstance(wwd, float) else None

        self.steepness = steepness if isinstance(steepness, str) else ""
        self.apd = apd if isinstance(apd, float) else None

    def __str__(self) -> str:
        """
        Convert all swell data to one long string
        :return: String representation of the wave data
        """
        header = ""
        if self.mm and self.dd and self.time:
            header = "{}-{} {}\n".format(self.mm, self.dd, self.time)

        waves = ""
        if self.wvht and self._wh and self.swp and self.swd:
            waves = "Wave HT({}) SWH({}) SWP({}) SWD({})\n".format(self.wvht, self.swh, self.swp, self.swd)

        wind_wave = ""
        if self.wwh and self.wwp and self.wwd and self.apd:
            wind_wave = "WWH({}) WWP({}) WWD({}) APD({})\n".format(self.wwh, self.wwp, self.wwd, self.apd)

        other = ""
        if self.steepness:
            other = "Steepness({})\n".format(self.steepness)

        return "{}{}{}{}".format(header, waves, wind_wave, other)


def convert_noaa_time(ugly_time: str) -> str:
    """
    Convert the time value read in from the table that NOAA has hosted. The time string is formatted
    oddly, so we will reformat the string to a more human readable representation.
    :param ugly_time: time string from the table on NOAA's website for each buoy data
    :return: human readable formatted time string, return an empty string we were unable to format the string
    """
    human_readable_time = ""

    if ugly_time and isinstance(ugly_time, str):
        sp = ugly_time.split(";")

        # the string should now contain am/pm and the actual time
        if len(sp) > 1:
            am_pm = sp[1]

            if am_pm == "am" or am_pm == "pm":

                # We don't care about anything after the &
                time = sp[0].split("&")[0]

                sp_time = time.split(":")

                if len(sp_time) == 2:
                    try:
                        hour = int(sp_time[0])
                        minute = int(sp_time[1])
                    except ValueError:
                        print("Nautical.noaa Package Error: convert_noaa_time() -> invalid time.")

                    human_readable_time = "{}:{} {}".format(hour, minute, am_pm)
            else:
                print("Nautical.noaa Package Error: convert_noaa_time() -> invalid am/pm value.")

    return human_readable_time


def get_sea_state(wvht_m: float) -> int:
    """
    The function wil take a wave height in meters and return the sea state

    The following static dictionary contains all of the sea state upper limits where the
    value is in meters

    sea state 0 = [0, 0]
    sea state 1 = (0, 0.1]
    sea state 2 = (0.1, 0.5]
    sea state 3 = (0.5, 1.25]
    sea state 4 = (1.25, 2.5]
    sea state 5 = (2.5, 4.0]
    sea state 6 = (4.0, 6.0]
    sea state 7 = (6.0, 9.0]
    sea state 8 = (9.0, 14.0]
    sea state 9 = (14.0, inf]

    :param wvht_m: wave height in METERS
    :return: integer value for the sea state
    """
    states = {
        0: 0.0,
        1: 0.1,
        2: 0.5,
        3: 1.25,
        4: 2.5,
        5: 4.0,
        6: 6.0,
        7: 9.0,
        8: 14.0,
        9: float('inf')
    }

    for key, value in states.items():
        if wvht_m <= value:
            return key