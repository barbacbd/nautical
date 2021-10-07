from .base import BaseNMEA0183
from enum import IntEnum
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class QoGPS(IntEnum):
    """
    Enumeration describing the Quality of GPS
    """
    FIX_NOT_AVAILABLE = 0
    GPS_FIX = 1
    DIFFERENTIAL_GPS_FIX = 2
    PPS_FIX = 3
    REAL_TIME_KINEMATIC = 4
    FLOAT_RTK = 5
    ESTIMATED_DR = 6
    MANUAL_INPUT_MODE = 7
    SIMULATION_MODE = 8


class GGA(BaseNMEA0183):

    """
    Time, Position, and Fix Related Data
    """

    __slots__ = [
        'report_time',         # UTC of this position report
        'lat',                 # latitude
        'lon',                 # longitude
        'gps_quality',         # GPS Quality Indicator (non null)
        'num_satellites',      # Number of satellites in use, 00 - 12
        'dillution_horiz',     # Horizontal Dilution of precision (meters)
        'antenna_alt_m',       # Antenna Altitude above/below mean-sea-level (geoid) (in meters)
        'geodial_separation',  # difference between the WGS-84 earth ellipsoid and mean-sea-level
        'gps_data_age',        # time in seconds since last SC104 type 1 or 9 update
        'diff_ref_stat_id'     # Differential reference station ID, 0000-1023
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 GGA sentence
        """
        self.report_time = 0.0
        self.lat = None
        self.lon = None
        self.gps_quality = None
        self.num_satellites = None
        self.dillution_horiz = None
        self.antenna_alt_m = None
        self.geodial_separation = None
        self.gps_data_age = None
        self.diff_ref_stat_id = None

        super().__init__(msg)

        self.s_type = "GGA"

    def __str__(self):
        """

        """
        _ret = "{}GGA,{},{},{},{},{},{},{},{},{},M,{},M".format(
            '--' if not self.talker_id else self.talker_id.name,
            self.report_time,
            abs(self.lat) if self.lat else 0.0,
            "N" if self.lat and self.lat >= 0.0 else "S",
            abs(self.lon) if self.lon else 0.0,
            "E" if self.lon and self.lon >= 0.0 else "W",
            self.gps_quality.value,
            self.num_satellites,
            "{:06.2f}".format(self.dillution_horiz) if self.dillution_horiz else 0.0,
            "{:07.3f}".format(self.antenna_alt_m) if self.antenna_alt_m else 0.0,
            "{:06.2f}".format(self.geodial_separation) if self.geodial_separation else 0.0
        )
        if self.gps_data_age:
            _ret = "{},{}".format(_ret, self.gps_data_age)

        if self.diff_ref_stat_id:
            _ret = "{},{}".format(_ret, self.diff_ref_stat_id)

        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 GGA Message
        """
        fields, checksum = BaseNMEA0183.parse_nmea_sentence(self._original)

        if checksum:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.report_time = cast(fields[1], StoredType.DATETIME)
            self.lat = cast(fields[2], StoredType.FLOAT)
            self.lon = cast(fields[4], StoredType.FLOAT)

            _i = cast(fields[6], StoredType.INTEGER)
            if _i:
                self.gps_quality = next((_ for _ in QoGPS if _i == _.value), None)

            self.num_satellites = cast(fields[7], StoredType.INTEGER)
            self.dillution_horiz = cast(fields[8], StoredType.FLOAT)
            self.antenna_alt_m = cast(fields[9], StoredType.FLOAT)
            self.geodial_separation = cast(fields[11], StoredType.FLOAT)
            self.gps_data_age = cast(fields[13], StoredType.FLOAT)
            self.diff_ref_stat_id = cast(fields[14], StoredType.INTEGER)
