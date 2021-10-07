from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string
from datetime import datetime


class ZDA(BaseNMEA0183):

    """
    UTC Day, moth, year and local time zone offset
    """

    __slots__ = [
        'utc_time',     # UTC time (hours, minutes, seconds, may have fractional subseconds)
        'day',          # Day, 01 to 31
        'month',        # Month, 01 to 12
        'year',         # Year (4 digits)
        'zone',         # Local zone description, 00 to +- 13 hours
        'zone_minutes'  # Local zone minutes description, 00 to 59, apply same sign as local hours
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 ZDA sentence
        """
        self.utc_time = None
        self.day = None
        self.month = None
        self.year = None
        self.zone = None
        self.zone_minutes = None

        super().__init__(msg)

        self.s_type = "ZDA"

    def __str__(self):
        """
        Returns a string representation of a ZDA nmea message
        """
        _ret = "{}ZDA,{},{},{},{},{},{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            self.utc_time,
            self.day,
            self.month,
            self.year,
            self.zone,
            self.zone_minutes
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 ZDA Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.utc_time = cast(fields[1], StoredType.DATETIME)
            self.day = cast(fields[2], StoredType.INTEGER)
            self.month = cast(fields[3], StoredType.INTEGER)
            self.year = cast(fields[4], StoredType.INTEGER)
            self.zone = cast(fields[5], StoredType.INTEGER)
            self.zone_minutes = cast(fields[6], StoredType.INTEGER)
