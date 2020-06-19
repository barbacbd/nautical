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


def convert(value, init_units, final_units):
    """
    Convert the value given the current units to the new units. If the
    units are not in the same set of units then the value cannot be converted,
    and None will be returned.

    :param value: Value provided in the units (init_units)
    :param init_units: initial units of the value (must match final units type)
    :param final_units: final units of the value (must match initial units type)
    :return: The value converted to the final units. If the units did not match None is returned
    """
    # value and units need to exist, units should also be the same type
    if value and init_units and final_units and type(init_units) == type(final_units):
        if init_units in TimeUnits:
            return convert_time(value, init_units, final_units)
        elif init_units in TemperatureUnits:
            return convert_temperature(value, init_units, final_units)
        elif init_units in DistanceUnits:
            return convert_distance(value, init_units, final_units)
        elif init_units in SpeedUnits:
            return convert_speed(value, init_units, final_units)


def convert_temperature(value, init_units, final_units):
    """
    Convert the temperature value from the initial units to the final units

    :param value: initial value for temperature
    :param init_units: initial units for temperature
    :param final_units: desired temperature units
    :return: value converted from the initial units to the final units
    """
    try:
        _temp = value if init_units in (TemperatureUnits.DEG_F,) else (9.0/5.0 * value) + 32.0
        return _temp if final_units in (TemperatureUnits.DEG_F,) else (_temp-32) * 5.0/9.0
    except Exception as e:
        pass


def convert_time(value, init_units, final_units):
    """
    Convert the time value from the initial units to the final units

    :param value: initial value for time
    :param init_units: initial units for time
    :param final_units: desired time units
    :return: value converted from the initial units to the final units
    """
    try:
        return value * TimeLookup[init_units] / TimeLookup[final_units]
    except KeyError as e:
        pass


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
        pass


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
        pass
