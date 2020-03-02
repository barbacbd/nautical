from .Messages import NMEAMessageType
from collections import OrderedDict  # use for a descriptor

class NMEAMessage(object):

    def __init__(self, id=NMEAMessageType.NONE):
        """

        """
        self._id = id

    @property id
    def id(self):
        return self._id

    @id.setter
    def type(self, id):
        self._id = id

    def load(self, msg: str):
        """
        Set a NMEA message by reading in the
        :param msg:
        :return:
        """