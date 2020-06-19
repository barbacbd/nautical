from .enums import Midday
from .nautical_time import nTime


# constant value from HTML to create a non-breaking space value
NON_BREAKING_SPACE = "&nbsp;"


def convert_noaa_time(orig: str):
    """
    Convert the time value read in from the table that NOAA has hosted.
    The time string is formatted/encoded with HTML data. We need to remove that data
    then split the time up.

    :param orig: original string representation of time
    :return: nTime object if it could be created, otherwise None will be returned
    """
    sp = orig.strip().split(NON_BREAKING_SPACE)

    m_s = None   # minutes and seconds
    t = nTime()  # Time object to be returned on success
    m = None     # Midday value

    if len(sp) == 2:
        # get the am/pm value
        try:
            m = [x for x in Midday if x.name.lower() in sp[1]][0]
        except IndexError as e:
            return None
        m_s = sp[0].split(":")

    elif len(sp) == 1:

        try:
            m = [x for x in Midday if x.name.lower() in orig.lower()][0]
        except IndexError as e:
            return None

        time_str_sp = [t for t in orig.lower().split(m.name.lower()) if t]
        m_s = time_str_sp[0].split(":")

    # Minutes and seconds found along with AM/PM
    if m_s and m and len(m_s) == 2:
        t.minutes = int(m_s[1])
        t.hours = int(m_s[0]), m

        return t
    else:
        return None
