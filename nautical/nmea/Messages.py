from enum import Enum


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
    :param lat_deg: latitude in degrees
    :param lon_deg: Longitude in degrees
    :param fix_quality: Fix qulaity Enumeration
    :param num_satellites: number of satellites in the fix
    :param horizontal: Horizontal dilution of position
    :param altitude_m: meters above sea level
    :param geoid_height: Height of geoid (mean sea level) above WGS84 ellipsoid
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
    :param lat_deg: latitude in degrees
    :param lon_deg: longitude in degrees
    :param vel_kts: velocity in knots
    :param hdg_deg: heading in degrees
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


class FixSelection(Enum):
    AUTO = 0
    MANUAL = 1


class FixValues(Enum):
    FIX_NONE = 1
    FIX_2D = 2
    FIX_3D = 3


def gsa(fix: FixSelection, fix_value: FixValues, prns: [], pdop: float, horizontal: float, vertical: float) -> str:
    """
    :param fix:
    :param fix_value:
    :param prns:
    :param pdop:
    :param horizontal:
    :param vertical:
    """
    if isinstance(prns, list) and len(prns) <= 12:
        [prns.append("") for _ in range(len(prns), 12)]
        prn_str = ",".join(prns)

        pre_cksm = "GP{},{},{},{},{:05.1f},{:05.1f},{:05.1f}".format(
            NMEAMessageType.GSA.name, str(fix.name)[0], fix_value.value, prn_str, pdop, horizontal, vertical
        )

        return "${}*{}".format(pre_cksm, checksum(pre_cksm))

class GSVSatelliteInfo(object):

    def __init__(self):
        self._prn = 0
        self._elevation_deg = 0.0
        self._azimuth_deg = 0.0

        # Signal to Noise Ratio (higher the better)
        # 0 - 99, units = dB
        self._snr = 0

    @property
    def snr(self):
        return self._snr

    @property
    def prn(self):
        return self._prn

    @property
    def elevation(self):
        return self._elevation_deg

    @property
    def azimuth(self):
        return self._azimuth_deg

    @snr.setter
    def snr(self, snr):
        if 0 <= snr <= 99:
            self._snr = snr

    @prn.setter
    def snr(self, prn):
        if 0 <= prn <= 99:
            self._prn = prn

    @elevation.setter
    def elevation(self, elevation):
        self._elevation_deg = elevation

    @azimuth.setter
    def azimuth(self, azimuth):
        self._azimuth_deg = azimuth

    def __str__(self):
        return "{:02d},{},{},{}".format(self._prn, self._elevation_deg, self._azimuth_deg, self._snr)


def gsv(satellites_for_full_data: int, sentence: int, num_satellites_in_view: int, sinfo_s: [GSVSatelliteInfo]) -> str:
    """
    :param satellites_for_full_data:
    :param sentence:
    :param num_satellites_in_view:
    :param sinfo_s:
    """
    if isinstance(sinfo_s, list) and len(sinfo_s) <= 4:
        sinfo_total = ",".join(sinfo_s)

        pre_cksm = "GP{},{},{},{},{}".format(
            NMEAMessageType.GSV.name, satellites_for_full_data, sentence, num_satellites_in_view, ",".join(sinfo_s)
        )

        return "${}*{}".format(pre_cksm, checksum(pre_cksm))