
from collections import OrderedDict
from .Messages import NMEAMessageType
from logging import getLogger
from os.path import abspath, exists
import yaml

log = getLogger(__name__)


class NMEADescriptors(object):

    """
    Singleton to hold all of the descriptor values for each of the types of
    NMEA messages that can be handled in this package.
    """

    __instance = None

    @staticmethod
    def getInstance():
        if NMEADescriptors.__instance is None:
            NMEADescriptors()

        return NMEADescriptors.__instance

    def __init__(self):
        """
        Make sure that this has not been run before since this is a singleton
        """
        if NMEADescriptors.__instance is not None:
            raise Exception("{} singleton has already been created".format(__name__))
        else:
            NMEADescriptors.__instance = self

            self._descriptors = {}  # store the descriptors from the json file here
            self._load(abspath("NMEADescriptors.yaml"))  # location is relative to this path

    def _load(self, filename):
        """
        Load all of the descriptor information from the file and save it to a dictionary, so
        that it can be used for look up during interpretation
        :param filename:
        """
        if not exists(filename):
            log.error("Failed to load {}".format(filename))

        self._descriptors.clear()  # delete everything in case the user calls this explicitly

        yaml_file = open(filename)
        yaml_data = yaml.load(yaml_file)
        yaml_file.close()

        for nm in NMEAMessageType:
            if yaml_data[str(nm.name)]:
                self._descriptors[str(nm.name)] = OrderedDict()
                for k, v in yaml_data[str(nm.name)].items():
                    self._descriptors[str(nm.name)][k] = v
