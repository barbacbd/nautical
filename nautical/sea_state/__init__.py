from nautical.units.units import DistanceUnits
from nautical.units.conversion import convert

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


def sea_state(wvht: float, units: DistanceUnits = DistanceUnits.METERS):
    """
    If the provided wave height is not in meters, convert the wave height to
    meters and determine the minimum seastate that meets the requirements.

    :param wvht: current height of the waves
    :param units: units of the wvht variable (defualt DistanceUnits.METERS)
    :return: the seastate (int) that the wae height falls in.
    """
    ht_m = wvht if units in (DistanceUnits.METERS,) else convert(wvht, units, DistanceUnits.METERS)
    return min([k for k, v in _SeaStates.items() if ht_m <= v])
