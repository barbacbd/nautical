
class WaveData(object):

    def __str__(self) -> str:
        """
        It appears that all of the attributes that we added through setattr are stored in
        a dictionary called self.__dict__ ... let's loop over that to print out the
        attrivutes that we have stored.

        NOTE: just in case, we can filter out some of our values here if we wanted to
        by making sure that no private variables are displayed ... filter for the __
        inside of the key (leaving this out for now though)

        :return: string representation of this object
        """
        ret = ""
        for k, v in self.__dict__.items():
            ret = ret + "{} = {}\n".format(k, v)

        return ret

    def __setattr__(self, key, value):
        """
        Probably don't neeed to override this function, but for debugging purposes I will leave
        this hear in case the user wishes to print out the data as it is set.
        :param key: dictionary key the attirubte is stored as
        :param value: value of the attribute
        :return: None
        """
        # print("WaveData {} = {}".format(key, value))
        super().__setattr__(key, value)


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