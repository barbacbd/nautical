from ..units import TimeUnits
from ..time import get_time_diff


def should_update(date_time_stamp: str, units=TimeUnits.MINUTES, max_diff=30):
    '''Determine if an update _should_ occur based on the time provided. The
    date_time_stamp should be provided with the format `__DT_FORMAT` (see
    ../time/ops.py for more information).
    
    :param data_time_stamp: String format for the string following the format in `__DT_FORMAT`
    :param units: Resulting time units
    :param max_diff: if the diff exceeds this value then True is returned
    :return: True when an update _may_ be desired
    '''
    return get_time_diff(date_time_stamp=date_time_stamp, units=units) > max_diff