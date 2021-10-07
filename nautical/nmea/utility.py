from enum import IntEnum
from datetime import datetime
from os import environ


class StoredType(IntEnum):
    """
    Data type to use for the stored data types.
    """
    BOOLEAN = 1
    DICT = 2
    FLOAT = 3
    INTEGER = 4
    INTEGER_BASE_16 = 5
    LIST = 6
    STRING = 7
    DATETIME = 8


def cast(original, desired_type: StoredType):
    """
    Attempt to cast the original value to the store value

    :param original: Original data type
    :param desired_type: StoredType that should be used for converting the data
    :return: The converted type, when catching a value error, None is returned
    """
    x = None
    try:
        if desired_type == StoredType.INTEGER:
            x = int(original)
        elif desired_type == StoredType.INTEGER_BASE_16:
            x = int(original, 16)
        elif desired_type == StoredType.FLOAT:
            x = float(original)
        elif desired_type == StoredType.BOOLEAN:
            x = bool(original)
        elif desired_type == StoredType.STRING:
            x = str(original)
        elif desired_type == StoredType.DATETIME:
            use_date = environ.get("USE_DATE_TIME", False)
            if use_date:
                _dt = datetime.combine(datetime.today(), datetime.strptime(original, "%H%M%S.%f").time())
                x = _dt.timestamp()
            else:
                x = str(original)
    except ValueError as e:
        pass
    finally:
        return x

