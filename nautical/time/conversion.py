from nautical.log import get_logger
from .enums import Midday
from .nautical_time import NauticalTime


log = get_logger()
# constant value from HTML to create a non-breaking space value
NON_BREAKING_SPACE = "&nbsp;"


def convert_noaa_time(orig: str):
    '''Convert the time value read in from the table that NOAA has hosted.
    The time string is formatted/encoded with HTML data. We need to remove that data
    then split the time up.

    :param orig: original string representation of time
    :return: NauticalTime object if it could be created, otherwise None will be returned
    '''
    split_str = orig.strip().split(NON_BREAKING_SPACE)

    mins_secs = None  # minutes and seconds
    nautical_time = None
    midday = None  # Midday value

    if len(split_str) == 2:
        # get the am/pm value
        try:
            midday = [x for x in Midday if x.name.lower() in split_str[1]][0]
        except IndexError as index_error:
            log.error(index_error)
            return None
        mins_secs = split_str[0].split(":")

    elif len(split_str) == 1:

        try:
            midday = [x for x in Midday if x.name.lower() in orig.lower()][0]
        except IndexError as index_error:
            log.error(index_error)
            return None

        time_str_sp = [t for t in orig.lower().split(midday.name.lower()) if t]
        mins_secs = time_str_sp[0].split(":")

    # Minutes and seconds found along with AM/PM
    if mins_secs and midday and len(mins_secs) == 2:
        nautical_time = NauticalTime()  # Time object to be returned on success
        nautical_time.minutes = int(mins_secs[1])
        nautical_time.hours = int(mins_secs[0]), midday

    return nautical_time
