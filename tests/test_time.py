import pytest
from nautical.time import (
    NauticalTime,
    convert_noaa_time,
    TimeFormat,
    Midday,
    get_current_time,
    get_time_diff,
    get_time_str
)
from datetime import timedelta, timezone
from nautical.cache.time import should_update


def test_correct_conversion():
    '''
    Properly convert the normal time string that will be retrieved
    from noaa website.
    '''
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
    '''
    First test:
        Should pass as the minutes do not matter. 

    Second Test:
        The time string has an invalid midday value. The value should
        be am or pm. LM will cause an error to occur and none will be
        returned instead of an nTime object
    '''
    time_str = "10:30:123&nbsp;am"
    t = convert_noaa_time(time_str)
    errors = []
    
    if not t:
        errors.append("t is None")
    
    time_str = "10:30&nbsp;lm"
    t = convert_noaa_time(time_str)
    if t is not None:
        errors.append("t is not None")
        
    assert not errors, "\n".join(errors)
    
    
def test_nTime_12_hr_correct():
    '''
    The Test has both a correct minute and hour value.
    '''
    t = NauticalTime()
    t.minutes = 45
    t.hours = 8, Midday.PM
    assert t.minutes == 45 and t.hours[0] == 8


def test_nTime_24_hr_incorrect_minutes():
    '''
    The minutes value is less than 0 meaning that the value
    wont change. The current value is initialized to 0, so
    that is what we will expect.
    '''
    u = NauticalTime(TimeFormat.HOUR_24)
    u.minutes = -1
    u.hours = 10, Midday.PM
    assert u.minutes == 0 and u.hours == 22


def test_nTime_24_hr_pm_set():
    '''
    Test the ability to set a pm value along with a value greater
    than 12. The value will be ignored and it will be interpreted
    as a 24 hour format.
    '''
    v = NauticalTime(TimeFormat.HOUR_24)
    v.minutes = 59
    v.hours = 13, Midday.PM
    assert v.minutes == 59 and v.hours == 13


def test_nTime_24_hr_high_minutes_high_hours():
    '''
    Test that the minute value is too large. Again
    The value is initialized to 0, so that is the value
    that we expect. The hour value is also incorrect
    as it is greater than 24
    '''
    x = NauticalTime(TimeFormat.HOUR_24)
    x.minutes = 61
    x.hours = 25
    assert x.minutes == 0 and x.hours == 0


def test_nTime_24_hr_low_hours():
    '''
    Test that the hour value is too low.
    '''
    x = NauticalTime(TimeFormat.HOUR_24)
    x.minutes = 45
    x.hours = -1
    assert x.minutes == 45 and x.hours == 0


def test_nTime_from_str_valid():
    '''Test converting time from valid string'''
    n = convert_noaa_time("13:45:00")
    
    assert n.hours == 1
    assert n.minutes == 45


def test_nTime_from_str_short_valid():
    '''Test converting time from valid string'''
    n = convert_noaa_time("13:45")
    
    assert n.hours == 1
    assert n.minutes == 45


def test_nTime_from_str_long_valid():
    '''Test converting time from valid string'''
    n = convert_noaa_time("01:45pm")
    
    assert n.hours[0] == 1
    assert n.hours[1].name == "PM"
    assert n.minutes == 45


def test_nTime_from_str_invalid():
    '''Test converting time from invalid string'''
    n = convert_noaa_time("13:gf45")
    assert n is None


def test_get_time_diff():
    '''Get a time difference of 30 minutes in the past'''
    
    alter = get_current_time().replace(tzinfo=timezone.utc)
    alter = alter - timedelta(minutes=30)
    
    assert get_time_diff(get_time_str(alter)) == 30
    

def test_get_time_diff_invalid():
    '''Get a time difference of 30 minutes in the future'''
    
    alter = get_current_time().replace(tzinfo=timezone.utc)
    alter = alter + timedelta(minutes=30)
    
    with pytest.raises(ValueError):
        assert get_time_diff(get_time_str(alter)) == 30


def test_should_update_yes():
    '''Test that enough time has passed to warrant an update'''
    dt = get_current_time().replace(tzinfo=timezone.utc)
    dt = dt - timedelta(minutes=45)
    
    assert should_update(get_time_str(dt))


def test_should_update_no():
    '''Test that enough time has passed to warrant an update'''
    dt = get_current_time().replace(tzinfo=timezone.utc)
    dt = dt - timedelta(minutes=29)
    
    assert not should_update(get_time_str(dt))
