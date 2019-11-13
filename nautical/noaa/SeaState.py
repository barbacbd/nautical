"""
The following static dictionary contains all of the sea state upper limits where the
value is in meters

sea state 0 = [0, 0]
sea state 1 = (0, 0.1]
sea state 2 = (0.1, 0.5]
sea state 3 = (0.5, 1.25]
sea state 4 = (1.25, 2.5]
sea state 5 = (2.5, 4.0]
sea state 6 = (4.0, 6.0]
sea state 7 = (6.0, 9.0]
sea state 8 = (9.0, 14.0]
sea state 9 = (14.0, inf]
"""
_SeaStates = {
        0: 0.0,
        1: 0.1,
        2: 0.5,
        3: 1.25,
        4: 2.5,
        5: 4.0,
        6: 6.0,
        7: 9.0,
        8: 14.0,
        9: float('inf')
    }


def get_sea_state(wvht_m: float) -> int:
    """
    The function wil take a wave height in meters and return the sea state
    :param wvht_m: wave height in METERS
    :return: integer value for the sea state
    """
    for key, value in _SeaStates.items():
        if wvht_m <= value:
            return key
