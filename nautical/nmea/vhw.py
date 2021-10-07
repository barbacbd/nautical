from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class VHW(BaseNMEA0183):

    """
    Water Speed and Heading
    """

    __slots__ = [
        'hdg_t',   # heading degrees, true
        'hdg_m',   # heading deg, magnetic
        'stw_k',   # speed through water knots
        'stw_km'   # speed through water km/h
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 VHW sentence
        """
        self.hdg_m = None
        self.hdg_t = None
        self.stw_k = None
        self.stw_km = None

        super().__init__(msg)

        # TODO: need to figure out if there is a prefix to this message

        self.s_type = "VHW"

    def __str__(self):
        """
        Returns a string representation of a VHW nmea message
        """
        _ret = "{}VHW,{},T,{},M,{},N,{},K".format(
            '--' if not self.talker_id else self.talker_id.name,
            "{:07.3f}".format(self.hdg_t) if self.hdg_t else "",
            "{:07.3f}".format(self.hdg_m) if self.hdg_m else "",
            "{:07.3f}".format(self.stw_k) if self.stw_k else "",
            "{:07.3f}".format(self.stw_km) if self.stw_km else ""
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 VHW Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.hdg_t = cast(fields[1], StoredType.FLOAT)
            self.hdg_m = cast(fields[3], StoredType.FLOAT)
            self.stw_k = cast(fields[5], StoredType.FLOAT)
            self.stw_km = cast(fields[7], StoredType.FLOAT)
