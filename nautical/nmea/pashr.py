from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from datetime import datetime
from .talker import talker_from_string


class PASHR(BaseNMEA0183):

    """
    RT300 proprietary roll and pitch sentence
    """

    __slots__ = [
        'report_time',    # UTC of this report
        'hdg',            # heading, degrees
        'roll',           # Roll Angle in Degrees
        'pitch',          # Pitch Angle in Degrees
        'heave',
        'roll_acc',       # Roll Angle Accuracy Estimate (Stdev) in degrees
        'pitch_acc',      # Pitch Angle Accuracy Estimate (Stdev) in degrees
        'hdg_acc',        # Heading Angle Accuracy Estimate (Stdev) in degrees
        'aiding_status',  # aiding status
        'imu_status'      # imu status
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 PASHR sentence
        """
        self.report_time = None
        self.hdg = None
        self.roll = None
        self.pitch = None
        self.heave = None
        self.roll_acc = None
        self.pitch_acc = None
        self.hdg_acc = None
        self.aiding_status = None
        self.imu_status = None

        super().__init__(msg)

        self.s_type = "PASHR"

    def __str__(self):
        """
        Returns a string representation of a PASHR nmea message
        """

        pashr_str = "PASHR,"
        pashr_str += "{},".format(self.report_time)
        pashr_str += "{:07.3f},T,".format(self.hdg if self.hdg else 0.0)
        pashr_str += "{:07.3f},".format(self.roll if self.roll else 0.0)
        pashr_str += "{:07.3f},".format(self.pitch if self.pitch else 0.0)
        pashr_str += "{:07.3f},".format(self.heave if self.heave else 0.0)
        pashr_str += "{:07.3f},".format(self.roll_acc if self.roll_acc else 0.0)
        pashr_str += "{:07.3f},".format(self.pitch_acc if self.pitch_acc else 0.0)
        pashr_str += "{:07.3f},".format(self.hdg_acc if self.hdg_acc else 0.0)

        pashr_str += "{},".format(int(self.aiding_status))
        pashr_str += "{}".format(int(self.imu_status))
        pashr_str += "*" + "{:02x}".format(BaseNMEA0183.nmea_checksum(pashr_str))

        return "${}".format(pashr_str)

    def _parse_string(self):
        """
        Parse the NMEA 0183 PASHR Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.checksum = cast(fields[len(fields)-1], StoredType.INTEGER_BASE_16)
            self.report_time = cast(fields[1], StoredType.DATETIME)
            self.hdg = cast(fields[2], StoredType.FLOAT)
            self.roll = cast(fields[4], StoredType.FLOAT)
            self.pitch = cast(fields[5], StoredType.FLOAT)
            self.heave = cast(fields[6], StoredType.FLOAT)
            self.roll_acc = cast(fields[7], StoredType.FLOAT)
            self.pitch_acc = cast(fields[8], StoredType.FLOAT)
            self.hdg_acc = cast(fields[9], StoredType.FLOAT)
            self.aiding_status = fields[10] == "1"
            self.imu_status = fields[11] == "1"
