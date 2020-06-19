from .buoy import Buoy


class Source:

    """
    The source is a grouping or categorization of buoy sources.
    """

    __slots__ = ['_name', '_description', '_buoys']

    def __init__(self, name: str, description: str = None):
        """
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
        """
        :return: string representation of the source
        """
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
        :return: True if name and description match
        """
        return type(self) == type(other) and self.name == other.name and self.description == other.description

    def __ne__(self, other):
        """
        :return: True if the name or description do not match
        """
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
        :param buoy: buoy to be added to the list of buoys.

        .. note::
            All buoy names are considered unique meaning the buoy name is CASE SENSITIVE

        :return: True if the buoy was added to the list of buoys
        """
        if buoy not in self:
            self._buoys[hash(buoy)] = buoy
            return True
        else:
            return False

    def get_buoy(self, station):
        """
        :param station: name of the buoy station
        :return: Buoy with a matching station, None if one was not found.

        .. note::
            All buoy names are considered unique meaning the search is CASE SENSITIVE
        """
        return next((v for k, v in self._buoys.items() if v.station == station), None)
