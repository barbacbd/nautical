from math import degrees
from time import gmtime, strftime


def checksum(nmea_str_pre_checksum: str) -> str:
    """
    Create a checksum for the NMEA 0183 string (excluding the $ and * characters). Convert each
    character of the string to an ascii integer value and XOR the values. The resulting base-16
    integer. Append this checksum to the NMEA  0183 message.
    :param nmea_str_pre_checksum: string before the checksum is calculated
    :return: 2 digit hexadecimal checksum
    """
    cksum = 0
    for c in nmea_str_pre_checksum:
        cksum = cksum ^ ord(c)

    return "{:02x}".format(cksum)


def format_latitude(lat_deg: float) -> (str, str):
    """
    :param lat_deg: Degrees of latitude [-90, 90]
    :return: Tuple of the formatted string for latitude and the N, S value
    """

    abs_lat_deg = int(abs(lat_deg))
    lat_min = (abs(lat_deg) - abs_lat_deg) * 60.0
    lat_str = "{:02d}{:06.3f}".format(abs_lat_deg, lat_min)

    return lat_str, "N" if lat_deg >= 0 else "S"


def format_longitude(lon_deg: float) -> (str, str):
    """
    :param lon_deg: Degrees of Longitude [-180, 180]
    :return: Tuple of the formatted string for longitude and the E, W value
    """
    abs_lon_deg = int(abs(lon_deg))
    lon_min = (abs(lon_deg) - abs_lon_deg) * 60.0
    lon_str = "{:03d}{:06.3f}".format(abs_lon_deg, lon_min)

    return lon_str, "E" if lon_deg >= 0 else "W"


format_latitude_rad = lambda lat_rad: format_latitude(degrees(lat_rad))


format_longitude_rad = lambda lon_rad: format_longitude(degrees(lon_rad))


def format_time() -> (str, str):
    return format_hms_time(), format_ymd_time()


def format_hms_time():
    """
    :return: Formatted Hours Minutes and Seconds from the current time
    """
    return strftime("%H%M%S", gmtime())


def format_ymd_time():
    """
    :return: Formmatted Year Month and Days from current time
    """
    return strftime("%d%m%y", gmtime())
