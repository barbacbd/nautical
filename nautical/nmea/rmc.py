from .base import BaseNMEA0183
from .enums import FAAModeIndicator
from sis.nmea.utility import cast, StoredType
from datetime import datetime, date
from .talker import talker_from_string


class RMC(BaseNMEA0183):

    """
    Position, Velocity, and Time
    """

    __slots__ = [
        'utc_time',           # UTC Time of position
        'status',             # Status, A = Valid, V = Warning
        'lat',                # latitude
        'lon',                # longitude
        'sog_k',              # speed over ground, knots
        'track_made_good',    # Track made good, degrees true
        'date',               # Date, ddmmyy
        'mag_var',            # Magnetic Variation, degrees
        'faa_mode_indicator'  # FAA mode indicator (NMEA 2.3 and later)
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 RMC sentence
        """
        self.utc_time = None
        self.status = None
        self.lat = None
        self.lon = None
        self.sog_k = None
        self.track_made_good = None
        self.date = None
        self.mag_var = None
        self.faa_mode_indicator = None

        super().__init__(msg)
        self.s_type = "RMC"

    def __str__(self):
        """

        """
        _ret = "{}RMC,{},{},{},{},{},{},{},{},{},{},{},{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            self.utc_time,
            "A" if self.status else "V",
            abs(self.lat) if self.lat else 0.0,
            "N" if self.lat and self.lat >= 0.0 else "S",
            abs(self.lon) if self.lon else 0.0,
            "E" if self.lon and self.lon >= 0.0 else "W",
            self.sog_k if self.sog_k else 0.0,
            self.track_made_good if self.track_made_good else 0.0,
            self.date,
            abs(self.mag_var) if self.mag_var else 0.0,
            "E" if self.mag_var and self.mag_var >= 0.0 else "W",
            str(self.faa_mode_indicator.name)[0] if self.faa_mode_indicator else "N"
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 RMC Message
        """
        fields, checksum = BaseNMEA0183.parse_nmea_sentence(self._original)

        if checksum:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.utc_time = cast(fields[1], StoredType.DATETIME)
            self.status = fields[2] == 'A'
            self.lat = cast(fields[3], StoredType.FLOAT) if fields[4] == "N" else -abs(cast(fields[3], StoredType.FLOAT))
            self.lon = cast(fields[5], StoredType.FLOAT) if fields[6] == "E" else -abs(cast(fields[3], StoredType.FLOAT))
            self.sog_k = cast(fields[7], StoredType.FLOAT)
            self.track_made_good = None if not fields[8] else cast(fields[8], StoredType.FLOAT)
            self.date = fields[9]
            self.mag_var = cast(fields[10], StoredType.FLOAT) if fields[11] == "E" else -abs(cast(fields[10], StoredType.FLOAT))
            self.faa_mode_indicator = next(
                (_ for _ in FAAModeIndicator if fields[12] == _.name[0]),
                FAAModeIndicator.NOT_VALID
            )
