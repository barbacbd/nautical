"""
Author: barbacbd
Date:   5/12/2020
"""
from .buoy import Buoy


class Source:

    __slots__ = ['_name', '_description', '_buoys']

    def __init__(self, name: str, description: str = None):
        """
        The source is a grouping or categorization of buoy sources.

        :param name: Name of the data source or grouping of data
        :param description: Description tag of the data source
        """

        if not name:
            raise NotImplementedError("Invalid source name {}".format(name))
        else:
            self._name = name

        self._description = description

        # Each buoy should have a unique name to use as the key
        self._buoys = {}

    def __str__(self):
        return str(self._name)

    def __contains__(self, item):
        """
        determine if the item buoy exists in our dictionary.

        :param item: should be a Buoy, String or int
            :Buoy: check if the hash of the item is in the dict
            :int: assume this is the hash and check
            :str: assume this is the station name check if its in the list
        """
        if isinstance(item, Buoy):
            return hash(item) in self._buoys
        elif isinstance(item, int):
            return item in self._buoys
        elif isinstance(item, str):
            return next((True for k, v in self._buoys.items() if item == v.station), False)

        return False

    def __iter__(self):
        """
        Override iterate to provide the user with the buoys in this instance
        """
        for k, v in self._buoys.items():
            yield v

    def __eq__(self, other):
        """
        The name and description should match
        """
        return type(self) == type(other) and self.name == other.name and self.description == other.description

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self._name

    @property
    def buoys(self):
        return self._buoys

    @property
    def description(self):
        return self._description

    def add_buoy(self, buoy):
        """
        The buoy will be added to the dictionary of buoys if the buoy does NOT exist.
        If the buoy exists nothing is run and False is returned, otherwise True is returned.
        All buoy names are considered unique meaning the buoy name is CASE SENSITIVE
        """
        if buoy not in self:
            self._buoys[hash(buoy)] = buoy
            return True
        else:
            return False

    def get_buoy(self, station):
        """
        If the buoy with the name that matches name exists, then the buoy will
        be returned. Otherwise NONE is returned. All buoy names are considered
        unique meaning that this search is CASE SENSITIVE
        """
        return next((v for k, v in self._buoys.items() if v.station == station), None)
