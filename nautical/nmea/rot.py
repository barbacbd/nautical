from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class ROT(BaseNMEA0183):

    """
    Rate of Turn
    """

    __slots__ = [
        'rot',     # Rate Of Turn, degrees per minute, "-" means bow turns to port
        'status'   # Status, A means data is valid
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 ROT sentence
        """
        self.rot = None
        self.status = None

        super().__init__(msg)

        self.s_type = "ROT"

    def __str__(self):
        """
        Returns a string representation of a ROT nmea message
        """
        _ret = "{}ROT,{},{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            "{:07.3f}".format(self.rot) if self.rot else "",
            "A" if self.status else "V"
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 ROT Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.rot = cast(fields[1], StoredType.FLOAT)
            self.status = fields[2] == "A"
