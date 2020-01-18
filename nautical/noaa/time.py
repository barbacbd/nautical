from ..error import NauticalError


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
                        human_readable_time = "{}:{} {}".format(hour, minute, am_pm)
                    except ValueError:
                        raise NauticalError("invalid time.")
            else:
                raise NauticalError("invalid am/pm value.")

    return human_readable_time
