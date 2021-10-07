from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class HDT(BaseNMEA0183):

    """
    Rate of Turn
    """

    __slots__ = [
        'hdg'      # Heading, degrees True
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 HDT sentence
        """
        self.hdg = None

        super().__init__(msg)

        self.s_type = "HDT"

    def __str__(self):
        """
        Returns a string representation of a HDG nmea message
        """
        hdt_str = "{}HDT,".format('--' if not self.talker_id else self.talker_id.name)
        hdt_str += str(self.hdg) + ",T" if self.hdg is not None else ",T"
        hdt_str += "*" + "{:02x}".format(BaseNMEA0183.nmea_checksum(hdt_str))

        return "${}".format(hdt_str)

    def _parse_string(self):
        """
        Parse the NMEA 0183 HDT Message
        """

        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.hdg = cast(fields[1], StoredType.FLOAT)
