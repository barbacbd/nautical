from enum import IntEnum


class _BuoyHeaderPositions(IntEnum):
    """
    Enumeration to allow the user to know where the buoy header fields exist
    """
    KEY = 1
    VALUE = 2


class _BuoyDataPositions(IntEnum):
    """
    Enumeration to allow the user to know where the buoy data fields exist
    """
    VALUE = 0
    UNITS = 1
