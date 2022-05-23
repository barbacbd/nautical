import pytest
from nautical.time import (
    NauticalTime,
    convert_noaa_time,
    TimeFormat,
    Midday
)


def test_correct_conversion():
    """
    Properly convert the normal time string that will be retrieved
    from noaa website.
    """
    time_str = "10:30&nbsp;am"
    t = convert_noaa_time(time_str)
    
    errors = []
    
    if not t:
        errors.append("t is None")
        
    if t.minutes != 30:
        errors.append("Minutes are wrong")

    if isinstance(t.hours, tuple):
        hours, units = t.hours
    else:
        hours = t.hours
        
    if hours != 10:
        errors.append("Hours are wrong")
    
    assert not errors, "\n".join(errors)


def test_incorrect_conversion():
    """
    First test:
        The time string below has extra fields after that will cause
        an error which means that no nTime object is created.

    Second Test:
        The time string has an invalid midday value. The value should
        be am or pm. LM will cause an error to occur and none will be
        returned instead of an nTime object
    """
    time_str = "10:30:123&nbsp;am"
    t = convert_noaa_time(time_str)
    errors = []
    
    if t:
        errors.append("t is None")
    
    time_str = "10:30&nbsp;lm"
    t = convert_noaa_time(time_str)
    if t:
        errors.append("t is not None")
        
    assert not errors, "\n".join(errors)
    
    
def test_nTime_12_hr_correct():
    """
    The Test has both a correct minute and hour value.
    """
    t = NauticalTime()
    t.minutes = 45
    t.hours = 8, Midday.PM
    assert t.minutes == 45 and t.hours[0] == 8


def test_nTime_24_hr_incorrect_minutes():
    """
    The minutes value is less than 0 meaning that the value
    wont change. The current value is initialized to 0, so
    that is what we will expect.
    """
    u = NauticalTime(TimeFormat.HOUR_24)
    u.minutes = -1
    u.hours = 10, Midday.PM
    assert u.minutes == 0 and u.hours == 22


def test_nTime_24_hr_pm_set():
    """
    Test the ability to set a pm value along with a value greater
    than 12. The value will be ignored and it will be interpreted
    as a 24 hour format.
    """
    v = NauticalTime(TimeFormat.HOUR_24)
    v.minutes = 59
    v.hours = 13, Midday.PM
    assert v.minutes == 59 and v.hours == 13


def test_nTime_24_hr_high_minutes_high_hours():
    """
    Test that the minute value is too large. Again
    The value is initialized to 0, so that is the value
    that we expect. The hour value is also incorrect
    as it is greater than 24
    """
    x = NauticalTime(TimeFormat.HOUR_24)
    x.minutes = 61
    x.hours = 25
    assert x.minutes == 0 and x.hours == 0


def test_nTime_24_hr_low_hours():
    """
    Test that the hour value is too low.
    """
    x = NauticalTime(TimeFormat.HOUR_24)
    x.minutes = 45
    x.hours = -1
    assert x.minutes == 45 and x.hours == 0

