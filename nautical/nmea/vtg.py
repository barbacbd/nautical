from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string
from .enums import FAAModeIndicator


class VTG(BaseNMEA0183):

    """
    Actual Track Made Good and Speed Over Ground
    """

    __slots__ = [
        'cog_dt',   # Course over ground, degrees North
        'cog_dm',   # Course over ground, degrees magnetic
        'sog_k',    # speed over ground, knots
        'sog_kmh',  # speed over ground, kilometers per hour
        'faa_mode_indicator'  # FAA Mode, nmea 2.3 or later
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 VTG sentence
        """
        self.cog_dt = None
        self.cog_dm = None
        self.sog_k = None
        self.sog_kmh = None
        self.faa_mode_indicator = None
        super().__init__(msg)
        self.s_type = "VTG"

    def __str__(self):
        """

        """
        _ret = "{}VTG,{},T,{},M,{},N,{},K,{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            "{:05.2f}".format(self.cog_dt) if self.cog_dt else "",
            "{:05.2f}".format(self.cog_dm) if self.cog_dm else "",
            "{:04.2f}".format(self.sog_k) if self.sog_k else "",
            "{:04.2f}".format(self.sog_kmh) if self.sog_kmh else "",
            self.faa_mode_indicator.name[0]
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """

        """
        fields, checksum = BaseNMEA0183.parse_nmea_sentence(self._original)

        if checksum:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.cog_dt = cast(fields[1], StoredType.FLOAT)
            self.cog_dm = cast(fields[3], StoredType.FLOAT)
            self.sog_k = cast(fields[5], StoredType.FLOAT)
            self.sog_kmh = cast(fields[7], StoredType.FLOAT)
            if len(fields) > 9:
                self.faa_mode_indicator = next(
                    (_ for _ in FAAModeIndicator if fields[9] == _.name[0]),
                    FAAModeIndicator.NOT_VALID
                )
