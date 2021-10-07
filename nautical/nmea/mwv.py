from .base import BaseNMEA0183
from enum import Enum
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class MWV(BaseNMEA0183):

    """
    Wind Speed and Angle
    """

    __slots__ = [
        'angle',       # Wind Angle, 0 to 359 degrees
        'ref',         # Reference, R = Relative, T = True
        'wind_speed',  # Wind Speed
        'units',       # Wind Speed Units, K/M/
        'status'       # Status, A = Data Valid, V = Invalid
    ]

    class Reference(Enum):
        true = 1  # T for true
        relative = 2  # R for relative

    class Unit(Enum):
        mps = 1  # meters per second
        knots = 2  # Knots
        kph = 3  # Kilometers per hour

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 MWV sentence
        """
        self.angle = None
        self.ref = None
        self.wind_speed = None
        self.units = None
        self.status = None

        super().__init__(msg)

        self.s_type = "MWV"

    def __str__(self):
        """
        Returns a string representation of a MWV nmea message
        """
        _ret = "{}MWV,{},{},{},{},{}".format(
            '--' if not self.talker_id else self.talker_id.name,
            "{:07.3f}".format(self.angle) if self.angle else "",
            self.ref.name[0].upper() if self.ref else "T",
            "{:07.3f}".format(self.wind_speed) if self.wind_speed else "",
            {self.Unit.mps: "M", self.Unit.knots: "N", self.Unit.kph: "K"}.get(self.units, "M"),
            "A" if self.status else "V"
        )

        return "${}*{:02x}".format(_ret, BaseNMEA0183.nmea_checksum(_ret))

    def _parse_string(self):
        """
        Parse the NMEA 0183 MWV Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.angle = cast(fields[1], StoredType.FLOAT)
            self.ref = {
                "R": self.Reference.relative,
                "T": self.Reference.true
            }.get(fields[2], self.Reference.relative)
            self.wind_speed = cast(fields[3], StoredType.FLOAT)
            self.units = {
                "M": self.Unit.mps,
                "N": self.Unit.knots,
                "K": self.Unit.kph
            }.get(fields[4], self.Unit.mps)
            self.status = fields[5] == "A"
