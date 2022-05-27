import unittest
from nautical.units import (
    convert,
    convert_time,
    convert_temperature,
    convert_speed,
    convert_distance,
    convert_pressure,
    TimeUnits,
    SpeedUnits,
    DistanceUnits,
    TemperatureUnits,
    PressureUnits
)
from math import fabs
import pytest


def test_convert_raise_no_value():
    '''Test None Type to convert for time'''
    with pytest.raises(TypeError):
        convert(None, TimeUnits.MINUTES, TimeUnits.MINUTES)


def test_convert_raise_no_init_unit():
    '''Test None type for units in time - arg2'''
    with pytest.raises(TypeError):
        convert(10.45, None, TimeUnits.MINUTES)


def test_convert_raise_no_final_unit():
    '''Test None type for units in time - arg3'''
    with pytest.raises(TypeError):
        convert(10.45, TimeUnits.MINUTES, None)


def test_convert_raise_mismatch():
    '''Test comparing units of different types'''
    with pytest.raises(TypeError):
        convert(10.45, TimeUnits.MINUTES, SpeedUnits.KPH)

        
def test_convert_dist_raises_init():
    '''Test distance with unknown units'''
    with pytest.raises(KeyError):
        convert_distance(10.45, TimeUnits.MINUTES, DistanceUnits.MILES)


def test_convert_dist_raises_final():
    '''test distance with unknown units'''
    with pytest.raises(KeyError):
        convert_distance(10.45, DistanceUnits.MILES, TimeUnits.MINUTES)


def test_convert_speed_raises_init():
    '''test speed with unknown units'''
    with pytest.raises(KeyError):
        convert_speed(10.45, TimeUnits.MINUTES, SpeedUnits.MPH)

        
def test_convert_speed_raises_final():
    '''test speed with unknown units'''
    with pytest.raises(KeyError):
        convert_speed(10.45, SpeedUnits.MPH, TimeUnits.MINUTES)


def test_convert_temp_raises_init():
    '''test temperature with unknown units'''
    with pytest.raises(KeyError):
        convert_temperature(10.45, TimeUnits.MINUTES, TemperatureUnits.DEG_F)


def test_convert_temp_raises_final():
    '''test temperature with unknown units'''
    with pytest.raises(KeyError):
        convert_temperature(10.45,TemperatureUnits.DEG_C, TimeUnits.MINUTES)


def test_convert_time_raises_init():
    '''test time with unknown units'''
    with pytest.raises(KeyError):
        convert_time(10.45, SpeedUnits.MPH, TimeUnits.MINUTES)


def test_convert_time_raises_final():
    '''test time with unknown units'''
    with pytest.raises(KeyError):
        convert_time(10.45, TimeUnits.MINUTES, SpeedUnits.MPH)
    

def test_good_tc_min_to_sec():
    '''
    Start with a minutes value and see if that can be converted to all of the other
    values possible.

    Minutes =  5432.45

    Expect:
        Seconds = 325947.0
        Hours = 90.541
        Days = 3.773
    '''
    init_time = 5432.45  # minutes
    time_test_data  = [
        (TimeUnits.SECONDS, 325947.0),
        (TimeUnits.MINUTES, 5432.45),
        (TimeUnits.HOURS, 90.541),
        (TimeUnits.DAYS, 3.773)
    ]
    errors = []
    for x in time_test_data:
        if fabs(convert(init_time, TimeUnits.MINUTES, x[0])-x[1]) > 0.001:
            errors.append(x[0].name)
    
    assert not errors, "\n".join(errors)


def test_good_speed_conversion():
    '''
    Start with knots value and see if that can be converted to all of the other
    values possible.

    KTS =  5.34

    Expect:
        MPS = 2.747
        MPH = 6.145
        KPH = 9.890
        FPS = 9.013
    '''
    init_speed = 5.34  # KTS

    speed_test_data  = [
        (SpeedUnits.KNOTS, 5.34),
        (SpeedUnits.MPS, 2.747),
        (SpeedUnits.MPH, 6.145),
        (SpeedUnits.KPH, 9.890),
        (SpeedUnits.FPS, 9.013)
    ]
    errors = []
    for x in speed_test_data:
        if fabs(convert(init_speed, SpeedUnits.KNOTS, x[0])-x[1]) > 0.001:
            errors.append(x[0].name)
    
    assert not errors, "\n".join(errors)


def test_good_distance_conversion():
    '''
    Start with MILES value and see if that can be converted to all of the other
    values possible.

    MILES = 2.10

    Expect:
        cm = 337961.4
        ft = 11087.972
        yd = 3695.991
        mt = 3379.614
        km = 3.380
        nm = 1.825
    '''
    init_distance = 2.10  # miles

    dist_test_data  = [
        (DistanceUnits.MILES, 2.10),
        (DistanceUnits.CENTIMETERS, 337961.4),
        (DistanceUnits.FEET, 11087.972),
        (DistanceUnits.YARDS, 3695.991),
        (DistanceUnits.METERS, 3379.614),
        (DistanceUnits.KILOMETERS, 3.380),
        (DistanceUnits.NAUTICAL_MILES, 1.825)
    ]
    errors = []
    for x in dist_test_data:
        if fabs(convert(init_distance, DistanceUnits.MILES, x[0])-x[1]) > 0.001:
            errors.append(x[0].name)
    
    assert not errors, "\n".join(errors)

    
def test_good_temperature_conversion():
    '''
    Test converting from Fahrenheit to Celsius and the opposite
    '''
    deg_f = 54.45
    errors = []
    if fabs(convert(deg_f, TemperatureUnits.DEG_F, TemperatureUnits.DEG_C)-12.472) > 0.001:
        errors.append("DEG_F to DEG_C")
    
    deg_c = 20.56
    if fabs(convert(deg_c, TemperatureUnits.DEG_C, TemperatureUnits.DEG_F)-69.008) > 0.001:
        errors.append("DEG_C to DEG_F")
    
    assert not errors, "\n".join(errors)

