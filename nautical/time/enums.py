from enum import Enum


class Midday(Enum):
    """
    simple enumeration to provide which side of midday the time is associated with
    """
    AM = 1
    PM = 2


class TimeFormat(Enum):
    """ Time Format Enumeration to indicate 12-24 hour times """
    HOUR_12 = 12
    HOUR_24 = 24
