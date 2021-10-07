import operator
from time import time
from functools import reduce
from re import split as r_split


class BaseNMEA0183:
    """
    Base class for NMEA 0183 Messages
    """

    __slots__ = ['timestamp', 'checksum', 's_type', '_original', 'talker_id']

    def __init__(self, msg):
        """
        :param msg: Entire message received as a single nmea sentence
        """
        self.timestamp = time()
        self.checksum = None
        self._original = msg
        self.s_type = None  # sentence Type
        self.talker_id = None

        self.parse()

    def __str__(self):
        """
        :return: String representation of the message
        :raises NotImplementedError: Base Class Only, all children will/should implement
        """
        raise NotImplementedError("{} does not have a string form.".format(__name__))

    def parse(self):
        """
        Generic parse function that will allow the user to provide several different
        types of values for the messages to be created.

        :raises AttributeError: Raised when the type is not a string, list, or dict
        """
        if isinstance(self._original, str):
            self._parse_string()
        elif isinstance(self._original, list):
            self._parse_list()
        elif isinstance(self._original, dict):
            self._parse_dict()
        else:
            raise AttributeError("Cannot parse unexpected type {}".format(type(self._original)))

    def _parse_string(self):
        """
        Parse the sentence that arrived in the init function. Validate the message.
        If the message cannot be validated, raise an error. The instance should then be
        disposed of.

        :raises NotImplementedError: Base class only
        """
        raise NotImplementedError()

    def _parse_list(self):
        """
        The list provided MUST be 1 greater than the size of the __slots__ for
        the child class, where the each element is in the same order as the slots.
        The final item in the list is the checksum.

        :raises NotImplementedError: When the provided list is incompatible with the
        number of slots, or when the message cannot be validated
        """
        if len(self._original) != (len(self.__slots__) + 1):
            raise NotImplementedError("Expected {} args, received {}".format(len(self.__slots__) + 1, len(self._original)))

        for _i, _n in enumerate(self.__slots__):
            setattr(self, _n, self._original[_i])

        self.checksum = self._original[len(self._original) - 1]

        _, valid = BaseNMEA0183.parse_nmea_sentence(str(self))
        if not valid:
            raise NotImplementedError("failed to validate {}".format(self._original))

    def _parse_dict(self):
        """
        The dictionary provided MUST contain the names in __slots__. If not all values are
        filled out in the message, or if any values are left as NONE in the child, an error
        will be raised. Do NOT forget to set the checksum!

        :raises NotImplementedError: When the provided dictionary is incompatible with the
        number of slots, or when the message cannot be validated
        """
        for _k, _v in self._original.items():
            if _k in self.__slots__:
                setattr(self, _k, _v)
            elif _k == 'checksum':
                self.checksum = _v

        if not self.checksum or None in [getattr(self, _) for _ in self.__slots__]:
            raise NotImplementedError("Failed to set all values for the NMEA Message.")

        _, valid = BaseNMEA0183.parse_nmea_sentence(str(self))
        if not valid:
            raise NotImplementedError("Failed to validate {}".format(self._original))

    @staticmethod
    def nmea_checksum(sentence):
        """
        :param sentence: Create a checksum from the sentence
        """
        return reduce(operator.xor, (ord(s) for s in sentence), 0)

    @staticmethod
    def parse_nmea_sentence(sentence):
        """
        Static method to parse the nmea message and put it into a list.

        :param sentence:  NMEA 0183 sentence to validate
        :return:  A list of the message given
        """
        nmeadata = r_split('[,|*]', sentence)
        return nmeadata, BaseNMEA0183.validate(sentence)

    @staticmethod
    def validate(sentence):
        """
        Validate the NMEA 0183 sentence using the data and the checksum that are all contained
        with in the sentence.

        :param sentence:  NMEA 0183 sentence to validate
        :return: True if validate, False otherwise
        """
        _s = sentence[1:] if sentence.startswith("$") else sentence

        try:
            nmeadata, cksum = _s.split('*', 1)
        except ValueError:
            return False

        calc_cksum = BaseNMEA0183.nmea_checksum(nmeadata)

        return hex(calc_cksum) == hex(int(cksum, 16))
