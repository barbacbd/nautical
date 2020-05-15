"""
Author: barbacbd
Date:   5/12/2020
"""


class Source:

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
        return item in self._buoys

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
        if buoy.station not in self._buoys:
            self._buoys[buoy.station] = buoy
            return True
        else:
            return False

    def get_buoy(self, station):
        """
        If the buoy with the name that matches name exists, then the buoy will
        be returned. Otherwise NONE is returned. All buoy names are considered
        unique meaning that this search is CASE SENSITIVE
        """
        return self._buoys.get(station, None)
