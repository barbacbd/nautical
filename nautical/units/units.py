from enum import Enum


class TimeUnits(Enum):
    """
    Various units of time to provide to the user in the event
    that they do not wish to use the base units from NOAA
    """
    SECONDS = 1
    MINUTES = 2
    HOURS = 3
    DAYS = 4


class TemperatureUnits(Enum):
    """
    Various units of temperature to provide to the user in the event
    that they do not wish to use the base units from NOAA
    """
    DEG_F = 1  # Degrees Fahrenheit
    DEG_C = 2  # Degrees Celsius


class SpeedUnits(Enum):
    """
    Various units of speed to provide to the user in the event
    that they do not wish to use the base units from NOAA
    """
    KNOTS = 1  # Nautical Miles Per Hour
    MPS = 2    # Meters Per Second
    MPH = 3    # Miles Per Hour
    KPH = 4    # Kilometers Per Hour
    FPS = 5    # Feet Per Second


class DistanceUnits(Enum):
    """
    Various units of distance to provide to the user in the event
    that they do not wish to use the base units from NOAA
    """
    CENTIMETERS = 1
    FEET = 2
    YARDS = 3
    METERS = 4
    KILOMETERS = 5
    MILES = 6
    NAUTICAL_MILES = 7
