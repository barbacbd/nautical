from .base import BaseNMEA0183
from sis.nmea.utility import cast, StoredType
from .talker import talker_from_string


class GST(BaseNMEA0183):

    """
    Position Error Statistics
    """

    __slots__ = [
        'tc_time',          # TC time of associated GGA fix
        'total_rms_stdev',  # Total RMS standard deviation of ranges inputs to the navigation solution
        'stdev_m_major',    # Standard deviation (meters) of semi-major axis of error ellipse
        'stdev_m_minor',    # Standard deviation (meters) of semi-minor axis of error ellipse
        'orientation',      # Orientation of semi-major axis of error ellipse (true north degrees)
        'stdev_m_lat',      # Standard deviation (meters) of latitude error
        'stdev_m_lon',      # Standard deviation (meters) of longitude error
        'stdev_m_alt'       # Standard deviation (meters) of altitude error
    ]

    def __init__(self, msg):
        """
        :param msg: original nmea 0183 GST sentence
        """
        self.tc_time = None
        self.total_rms_stdev = None
        self.stdev_m_major = None
        self.stdev_m_minor = None
        self.orientation = None
        self.stdev_m_lat = None
        self.stdev_m_lon = None
        self.stdev_m_alt = None

        super().__init__(msg)

        # GP = GPS ONLY, GL = GLONASS, GN = COMBINED
        self.s_type = "GST"

    def __str__(self):
        """
        Returns a string representation of a GST nmea message
        """
        gst_str = "{}GST,".format('--' if not self.talker_id else self.talker_id.name)
        gst_str += str(self.tc_time) + "," if self.tc_time is not None else ","
        gst_str += str(self.total_rms_stdev) + "," if self.total_rms_stdev is not None else ","
        gst_str += str(self.stdev_m_major) + "," if self.stdev_m_major is not None else ","
        gst_str += str(self.stdev_m_minor) + "," if self.stdev_m_minor is not None else ","
        gst_str += str(self.orientation) + "," if self.orientation is not None else ","
        gst_str += str(self.stdev_m_lat) + "," if self.stdev_m_lon is not None else ","
        gst_str += str(self.stdev_m_lon) + "," if self.stdev_m_lon is not None else ","
        gst_str += str(self.stdev_m_alt) if self.stdev_m_alt is not None else ""
        gst_str += "*" + "{:02x}".format(BaseNMEA0183.nmea_checksum(gst_str))

        return "${}".format(gst_str)

    def _parse_string(self):
        """
        Parse the NMEA 0183 GST Message
        """
        fields, valid = BaseNMEA0183.parse_nmea_sentence(self._original)

        if valid:
            self.talker_id = talker_from_string(fields[0])
            self.tc_time = cast(fields[1], StoredType.DATETIME)
            self.total_rms_stdev = cast(fields[2], StoredType.FLOAT)
            self.stdev_m_major = cast(fields[3], StoredType.FLOAT)
            self.stdev_m_minor = cast(fields[4], StoredType.FLOAT)
            self.orientation = cast(fields[5], StoredType.FLOAT)
            self.stdev_m_lat = cast(fields[6], StoredType.FLOAT)
            self.stdev_m_lon = cast(fields[7], StoredType.FLOAT)
            self.stdev_m_alt = cast(fields[8], StoredType.FLOAT)
            self.checksum = cast(fields[9], StoredType.INTEGER_BASE_16)

