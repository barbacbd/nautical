from datetime import datetime, timezone
from ..units import TimeUnits, convert_time


# Datetime string format for all date time values
__DT_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_current_time():
    '''Get current time in UTC timezone format'''
    return datetime.now().replace(tzinfo=timezone.utc)


def get_time_str(dt_obj=get_current_time()):
    '''Get the current time as a string'''
    return datetime.strftime(dt_obj, __DT_FORMAT)


def get_time_diff(date_time_stamp: str, units=TimeUnits.MINUTES):
    '''Pass in a string that contains the date and timestamp formatted in the same manner
    as `__DT_FORMAT` (see above for more information). The resulting time difference
    from now is returned with the units provided. All values _should_ use utc time. 
    
    :param data_time_stamp: String format for the string following the format in `__DT_FORMAT`
    :param units: Resulting time units
    :return: Time units difference from now to the date_time_stamp in the units provided.
    '''
    assumed_past_time = datetime.strptime(date_time_stamp, __DT_FORMAT).replace(tzinfo=timezone.utc)
    now = get_current_time()
    
    time_diff_seconds = (now - assumed_past_time).total_seconds()
    
    if time_diff_seconds < 0: 
        raise ValueError("Time provided to get_wait_time_diff is in the future")

    return int(convert_time(time_diff_seconds, TimeUnits.SECONDS, units))
