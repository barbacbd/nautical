
class NOAAData(object):

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

        We will not keep values that are empty

        We will also not keep blank values that NOAA stores as - on their website

        :param key: dictionary key the attirbute is stored as
        :param value: value of the attribute
        :return: None
        """

        if value is None or value == '-':
            return

        # print("WaveData {} = {}".format(key, value))
        super().__setattr__(key, value)


class CombinedNOAAData:

    def  __init__(self) -> None:
        """
        This class is meant to serve as the combination of past and present NOAA
        data for a particular buoy location. This will will include:

        present wave data
        present swell data
        past wave data
        past swell data
        """
        self.present_wave_data = None
        self.present_swell_data = None
        self.past_wave_data = None
        self.past_swell_data = None


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