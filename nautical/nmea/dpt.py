from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class DPT(BaseNMEA0183):

    """
    Depth of Water
    """

    __slots__ = [
        'depth',     # Water depth relative to transducer, meters
        'offset',    # + means distance from transducer to water line, - means distance from transducer to keel
        'max_scale'  # Maximum range scale in use (NMEA 3.0 and above)
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 DPT sentence
        """
        self.depth = None
        self.offset = None
        self.max_scale = None
        
        super().__init__(msg)

        self.s_type = "DPT"

    def __str__(self):
        """

        """
        _ret = "{}DPT,{},{}{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            "{:07.3f}".format(self.depth) if self.depth else "",
            "{:07.3f}".format(self.offset) if self.offset else "",
            ",{}".format(self.max_scale) if self.max_scale else ""
        )
        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 DPT Message
        """

        fields, checksum = BaseNMEA0183.parse_nmea_sentence(self._original)

        if checksum:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.depth = cast(fields[1], StoredType.FLOAT)
            self.offset = cast(fields[2], StoredType.FLOAT)
            if len(fields) == 5:
                self.max_scale = cast(fields[3], StoredType.FLOAT)
