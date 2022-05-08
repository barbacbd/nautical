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
        """String representation of this instance

        :return: string representation of the source
        """
        return str(self._name)

    def __contains__(self, item):
        """
        Determine if the item buoy exists in our dictionary.
        When `item` is a `Buoy`, check if the hash of the item is in the dict. 
        when `item` is an int, assume this is the hash and check for it in the dict.
        When `item` is a str, assume this is the station name check if its in the dict.

        :param item: should be a Buoy, String or int
        :return: True when the item is found in this instance.
        """
        if isinstance(item, Buoy):
            return hash(item) in self._buoys
        elif isinstance(item, int):
            return item in self._buoys
        elif isinstance(item, str):
            return next((True for k, v in self._buoys.items() if item == v.station), False)

        return False

    def __iter__(self):
        """Override iterate to provide the user with the buoys in this instance.
        Yield the `Buoy` objects in this instance.
        """
        for k, v in self._buoys.items():
            yield v

    def __eq__(self, other):
        """Determine if this instance is the same as the other `source`

        :return: True if name and description match
        """
        return type(self) == type(other) and self.name == other.name and self.description == other.description

    def __ne__(self, other):
        """See __eq__ for more information

        :return: True if the name or description do not match
        """
        return not self.__eq__(other)

    @property
    def name(self):
        """Name Property for this instance

        :return: The name of the instance
        """
        return self._name

    @property
    def buoys(self):
        """Buoys Property for this instance

        :return: Copy of the current set of buoys contained in this instance
        """
        return self._buoys.copy()

    @property
    def description(self):
        """Description Property for this instance
    
        :return: The instance description.
        """
        return self._description

    def add_buoy(self, buoy):
        """Add a buoy to this instance

        .. note:: Buoy names are case sensitive to ensure they are unique

        :param buoy: buoy to be added to the list of buoys.
        :return: True if the buoy was added to the list of buoys
        """
        if buoy not in self:
            self._buoys[hash(buoy)] = buoy
            return True
        else:
            return False

    def get_buoy(self, station):
        """Get a buoy where the station matches the `station` of the Buoy

        .. note:: Buoy names are case sensitive to ensure they are unique

        :param station: name of the buoy station
        :return: Buoy with a matching station, None if one was not found.
        """
        return next((v for k, v in self._buoys.items() if v.station == station), None)
