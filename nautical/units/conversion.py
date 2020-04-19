"""
Author: barbacbd
Date:   4/18/2020
"""

from .units import (
    TimeUnits,
    TemperatureUnits,
    SpeedUnits,
    DistanceUnits
)

"""
Lookup Tables to convert to a base unit then back to the
final unit
"""

TimeLookup = {
    TimeUnits.SECONDS: 1.0,
    TimeUnits.MINUTES: 60.0,  # seconds per minute
    TimeUnits.HOURS: 3600.0,  # seconds per hour
    TimeUnits.DAYS: 86400.0   # seconds per day
}

DistanceLookup = {
    DistanceUnits.CENTIMETERS: 1.0,
    DistanceUnits.FEET: 30.48,           # cm per feet
    DistanceUnits.YARDS: 91.44,          # cm per yard
    DistanceUnits.METERS: 100.0,         # cm per meter
    DistanceUnits.KILOMETERS: 100000.0,  # cm per km
    DistanceUnits.MILES: 160934.0        # cm per mile
}

SpeedLookup = {
    SpeedUnits.KNOTS: 1.0,
    SpeedUnits.MPS: 0.514444,  # Knots to Meters per Second
    SpeedUnits.MPH: 1.15078,   # Knots to Miles Per Hour
    SpeedUnits.KPH: 1.852,     # Knots to Kilometers Per Hour
    SpeedUnits.FPS: 1.6878     # Knots to Feet Per Second
}


def convert(value, init_units, final_units):
    """
    Convert the value given the current units to the new units. If the
    units are not in the same set of units then the value cannot be converted,
    and None will be returned.
    """

    # value and units need to exist, units should also be the same type
    if value and init_units and final_units and init_units is final_units:
        if init_units in TimeUnits:
            return convert_time(value, init_units, final_units)
        elif init_units in TemperatureUnits:
            return convert_temperature(value, init_units, final_units)
        elif init_units in DistanceUnits:
            return convert_distance(value, init_units, final_units)
        elif init_units in SpeedUnits:
            return convert_speed(value, init_units, final_units)


def convert_temperature(value, init_units, final_units):
    try:
        _temp = value if init_units in (TemperatureUnits.DEG_F,) else (value-32) * 5.0/9.0
        return _temp if final_units in (TemperatureUnits.DEG_F,) else (9.0/5.0 * _temp) + 32.0
    except Exception as e:
        pass


def convert_time(value, init_units, final_units):
    try:
        return value * TimeLookup[init_units] / TimeLookup[final_units]
    except KeyError as e:
        pass


def convert_distance(value, init_units, final_units):
    try:
        return value * DistanceLookup[init_units] / DistanceLookup[final_units]
    except KeyError as e:
        pass


def convert_speed(value, init_units, final_units):
    try:
        return value * SpeedLookup[init_units] / SpeedLookup[final_units]
    except KeyError as e:
        pass