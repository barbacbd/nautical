from . import (
    TimeUnits,
    TemperatureUnits,
    SpeedUnits,
    DistanceUnits,
    PressureUnits
)
from logging import getLogger


log = getLogger()



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
    DistanceUnits.FEET: 30.48,              # cm per feet
    DistanceUnits.YARDS: 91.44,             # cm per yard
    DistanceUnits.METERS: 100.0,            # cm per meter
    DistanceUnits.KILOMETERS: 100000.0,     # cm per km
    DistanceUnits.MILES: 160934.0,          # cm per mile
    DistanceUnits.NAUTICAL_MILES: 185200.0  # cm per nautical mile
}

SpeedLookup = {
    SpeedUnits.MPS: 1.0,
    SpeedUnits.KNOTS: 1.94384,  # MPS to KTS
    SpeedUnits.MPH: 2.23694,    # MPS to Miles Per Hour
    SpeedUnits.KPH: 3.6,        # MPS to Kilometers Per Hour
    SpeedUnits.FPS: 3.28084     # MPS to Feet Per Second
}


PressureLookup = {
    PressureUnits.PA: 1.0,
    PressureUnits.TORR: 7.5*(10**-3),
    PressureUnits.BARR: 10**-5,
    PressureUnits.ATM: 9.869*(10**-6),
    PressureUnits.AT: 1.02*(10**-5),
    PressureUnits.BA: 10,
    PressureUnits.PSI: 1.45*(10**-4),
    PressureUnits.HG: 7.5*(10**-3)
}


def convert_temperature(value, init_units, final_units):
    """
    Convert the temperature value from the initial units to the final units

    :param value: initial value for temperature
    :param init_units: initial units for temperature
    :param final_units: desired temperature units
    :return: value converted from the initial units to the final units
    """
    if not isinstance(init_units, TemperatureUnits) or not isinstance(final_units, TemperatureUnits):
        raise KeyError
    _temp = value if init_units in (TemperatureUnits.DEG_F,) else (9.0/5.0 * value) + 32.0
    return _temp if final_units in (TemperatureUnits.DEG_F,) else (_temp-32) * 5.0/9.0


def convert_time(value, init_units, final_units):
    """
    Convert the time value from the initial units to the final units

    :param value: initial value for time
    :param init_units: initial units for time
    :param final_units: desired time units
    :return: value converted from the initial units to the final units
    :raises KeyError: 
    """
    try:
        return value * TimeLookup[init_units] / TimeLookup[final_units]
    except KeyError as e:
        log.error(e)
        raise


def convert_distance(value, init_units, final_units):
    """
    Convert the distance value from the initial units to the final units

    :param value: initial value for distance
    :param init_units: initial units for distance
    :param final_units: desired distance units
    :return: value converted from the initial units to the final units
    """
    try:
        return value * DistanceLookup[init_units] / DistanceLookup[final_units]
    except KeyError as e:
        log.error(e)
        raise 


def convert_speed(value, init_units, final_units):
    """
    Convert the speed value from the initial units to the final units

    :param value: initial value for speed
    :param init_units: initial units for speed
    :param final_units: desired speed units
    :return: value converted from the initial units to the final units
    """
    try:
        # speed works a bit the opposite we want to divide then multiply
        # instead of the normal multiplication then division
        return value / SpeedLookup[init_units] * SpeedLookup[final_units]
    except KeyError as e:
        log.error(e)
        raise 


def convert_pressure(value, init_units, final_units):
    """
    Convert the pressure value from the initial units to the final units

    :param value: initial value for pressure
    :param init_units: initial units for pressure
    :param final_units: desired pressure units
    :return: value converted from the initial units to the final units
    """
    try:
        # speed works a bit the opposite we want to divide then multiply
        # instead of the normal multiplication then division
        return value / PressureLookup[init_units] * PressureUnits[final_units]
    except KeyError as e:
        log.error(e)
        raise 


# saved for quicker lookup
ConversionLookup = {
    TimeUnits: convert_time,
    TemperatureUnits: convert_temperature,
    DistanceUnits: convert_distance,
    SpeedUnits: convert_speed,
    PressureUnits: convert_pressure
}


def convert(value, init_units, final_units):
    """
    Convert the value given the current units to the new units. If the
    units are not in the same set of units then the value cannot be converted,
    and None will be returned.

    :param value: Value provided in the units (init_units)
    :param init_units: initial units of the value (must match final units type)
    :param final_units: final units of the value (must match initial units type)
    :return: The value converted to the final units. If the units did not match None is returned
    :raises TypeError: when the two types do not match, or when any of the parameters are None
    """

    if None not in (value, init_units, final_units) and type(init_units) == type(final_units):
        func = ConversionLookup.get(type(init_units), None)
        if callable(func):
            return func(value, init_units, final_units)
        
    raise TypeError  # two types did not match 
