from enum import Enum


GGA = "$GP{},{},{},{},{},{},{},{},{},{},{},{},{},,*{}"

class NMEAMessageType(Enum):
    """
    Enumerated values for messages found at:
    https://www.gpsinformation.org/dale/nmea.htm
    """
    NONE = 0
    AAM = 1
    ALM = 2
    APB = 3
    BOD = 4
    BWC = 5
    GGA = 6
    GLL = 7
    GSA = 8
    GSV = 9
    MSK = 10
    MSS = 11
    RMB = 12
    RMC = 13
    RTE = 14
    VTG = 15
    WPL = 16
    XTE = 17
    ZDA = 18


class FixQuality(Enum):
    """

    """
    INVALID = 0
    GPS_FIX_SPS = 1
    DGPS_FIX = 2
    PPS_FIX = 3
    REAL_TIME_KINEMATIC = 4
    FLOAT_RTK = 5
    DEAD_RECKONING = 6
    MANUAL_INPUT = 7
    SIMULATION_MODE = 8


from .helpers import (
    checksum,
    format_latitude,
    format_longitude,
    format_hms_time,
    format_ymd_time
)


def gga(lat_deg: float,
        lon_deg: float,
        fix_quality: FixQuality,
        num_satellites: int,
        horizontal: float,
        altitude_m: float,
        geoid_height: float) -> str:
    """

    """
    pre_cksm = "GP{},{},{},{},{},{},{},{},{},{},M,{},M,,".format(
        NMEAMessageType.GGA.name,
        format_hms_time(),
        format_latitude(lat_deg), 'N' if lat_deg >= 0.0 else 'S',
        format_longitude(lon_deg), 'E' if lon_deg >= 0.0 else 'W',
        fix_quality.value, num_satellites,
        horizontal,
        altitude_m,
        geoid_height
    )
    return "${}*{}".format(pre_cksm, checksum(pre_cksm))


def rmc(lat_deg: float, lon_deg: float, vel_kts: float, hdg_deg: float) -> str:
    """
    @param lat_deg: latitude in degrees
    @param lon_deg: longitude in degrees
    @param vel_kts: velocity in knots
    @param hdg_deg: heading in degrees
    """
    pre_cksm = "GP{},{},A,{},{},{},{},{:05.1f},{:05.1f},{},000.0,W".format(
        NMEAMessageType.RMC.name,
        format_hms_time(),
        format_latitude(lat_deg), 'N' if lat_deg >= 0.0 else 'S',
        format_longitude(lon_deg), 'E' if lon_deg >= 0.0 else 'W',
        vel_kts,
        hdg_deg,
        format_ymd_time()
    )

    return "${}*{}".format(pre_cksm, checksum(pre_cksm))
