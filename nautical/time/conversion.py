"""
Author: barbacbd
Date:   4/18/2020
"""
from . import Midday
from .nautical_time import nTime


# constant value from HTML to create a non-breaking space value
NON_BREAKING_SPACE = "&nbsp;"


def convert_noaa_time(orig: str):
    """
    Convert the time value read in from the table that NOAA has hosted.
    The time string is formatted/encoded with HTML data. We need to remove that data
    then split the time up.

    :return: nTime object if it could be created, otherwise None will be returned
    """
    sp = orig.strip().split(NON_BREAKING_SPACE)

    # this is exactly what we were expecting !
    if len(sp) == 2:
        t = nTime()

        # get the am/pm value
        try:
            m = [x for x in Midday if x.name.lower() in sp[1]][0]
        except IndexError as e:
            return None

        m_s = sp[0].split(":")

        # also, exactly what we were expecting !
        if len(m_s) == 2:
            t.minutes = int(m_s[1])
            t.hours = int(m_s[0]), m

            return t
