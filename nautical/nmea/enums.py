from enum import IntEnum


class FAAModeIndicator(IntEnum):
    AUTONOMOUS_MODE = 0
    DIFFERENTIAL_MODE = 1
    ESTIMATED_MODE = 2
    MANUAL_INPUT_MODE = 3
    SIMULATED_MODE = 4
    NOT_VALID = 5
