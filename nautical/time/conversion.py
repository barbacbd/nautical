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

    nautical_time = None
    midday = None  # Midday value

    if len(split_str) == 2:
        # get the am/pm value
        try:
            midday = [x for x in Midday if x.name.lower() in split_str[1]][0]
        except IndexError as index_error:
            log.error(index_error)
            return None
        # time portion of the split string is element 0
        # time_str = split_str[0].split(":")
        time_str = split_str[0]

    elif len(split_str) == 1:
        midday = [x for x in Midday if x.name.lower() in orig.lower()]
        if midday:
            midday = midday[0]
            time_str_sp = [t for t in orig.lower().split(midday.name.lower()) if t]
            # time portion of the string is the first element
            time_str = time_str_sp[0]
        else:
            log.warning("No AM/PM found in time string, assuming 24 hour format")
            # in this case NO AM/PM provided - String assumed to be complete in original state
            time_str = orig

    split_time = time_str.split(":")
    
    # Time is assumed in the format HH:MM:[SS] Where seconds is optional and not used
    if len(split_time) >= 2:
        nautical_time = NauticalTime()
        try:
            nautical_time.minutes = int(split_time[1])
            # See nautical.time.nautical_time.NauticalTime.hours for parsing information
            nautical_time.hours = int(split_time[0]), midday
        except ValueError as error:
            log.error(error)
            return None
    
    return nautical_time
