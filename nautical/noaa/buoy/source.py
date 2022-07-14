from copy import deepcopy
from enum import Enum
from nautical.log import get_logger
from nautical.noaa.buoy.buoy_data import BuoyData
from .buoy import Buoy


log = get_logger()


class SourceType(Enum):

    ALL = 0
    INTERNATIONAL_PARTNERS = 1
    IOOS_PARTNERS = 2
    MARINE_METAR = 3
    NDBC_METEOROLOGICAL_OCEAN = 4
    NERRS = 5
    NOS_CO_OPS = 6
    SHIPS = 7
    # unsupported types below
    TAO = 8
    TSUNAMI = 9

    @classmethod
    def as_strings(cls, source_type):
        '''Get the string value based on the type of source

        :param source_type: Type of source from the enumeration
        :return: List of strings that match the source type
        '''
        if source_type in (cls.TAO, cls.TSUNAMI):
            log.warning("Unsupported type: %s", source_type.name)
        
        source_as_string = {
            cls.INTERNATIONAL_PARTNERS: "International Partners",
            cls.IOOS_PARTNERS: "IOOS Partners",
            cls.MARINE_METAR: "Marine METAR",
            cls.NDBC_METEOROLOGICAL_OCEAN: "NDBC Meteorological/Ocean",
            cls.NERRS: "NERRS",
            cls.NOS_CO_OPS: "NOS/CO-OPS",
            cls.SHIPS: "Ships",
            cls.TAO: "TAO",
            cls.TSUNAMI: "Tsunami"
        }

        if source_type == cls.ALL:
            return list(source_as_string.values())
        return source_as_string.get(source_type, None)


class Source:
    '''The source is a grouping or categorization of buoy sources.'''

    def __init__(self, name: str, description: str = None):
        '''
        :param name: Name of the data source or grouping of data
        :param description: Description tag of the data source
        '''
        if not name:
            raise NotImplementedError(f"Invalid name provided to {self.__class__.__name__}")
        self.name = name
        self.description = description

        # Each buoy should have a unique name to use as the key
        self._buoys = {}

    def __len__(self):
        '''Return the number of buoys in this source'''
        return len(self._buoys)
        
    def __copy__(self):
        '''Override the copy function to only keep specific 
        values. Notice that the buoys are not kept
        '''
        cls = self.__class__
        result = cls.__new__(cls)
        
        source_dict = {
            key: value
            for key, value in self.__dict__.items() if not key.startswith("_")
        }
        source_dict["_buoys"] = {}
        log.info("Making copy of %s with dict %s", str(self.__class__.__name__), source_dict)
        result.__dict__.update(source_dict)
        return result

    def __deepcopy__(self, memo):
        '''Override the deepcopy for this instance to include
        all private variables
        '''
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        log.info("Making deepcopy of %s (%s) with dict %s",
                 str(self.__class__.__name__), id(self), self.__dict__)
        # Keep the references to the buoy and all private variables
        for key, value in self.__dict__.items():
            setattr(result, key, deepcopy(value, memo))
        return result
    
    def __str__(self):
        '''String representation of this instance

        :return: string representation of the source
        '''
        return self.name

    def __contains__(self, item):
        '''Determine if the item buoy exists in our dictionary.
        When `item` is a `Buoy`, check if the hash of the item is in the dict. 
        when `item` is an int, assume this is the hash and check for it in the dict.
        When `item` is a str, assume this is the station name check if its in the dict.

        :param item: should be a Buoy, String or int
        :return: True when the item is found in this instance.
        '''
        if isinstance(item, Buoy):
            return hash(item) in self._buoys
        if isinstance(item, int):
            return item in self._buoys
        if isinstance(item, str):
            return next((True for k, v in self._buoys.items() if item == v.station), False)
        return False

    def __iter__(self):
        '''Override iterate to provide the user with the buoys in this instance.
        Yield the `Buoy` objects in this instance.
        '''
        for _key, value in self._buoys.items():
            yield value

    def __eq__(self, other):
        '''Determine if this instance is the same as the other `source`

        :return: True if name and description match
        '''
        return isinstance(other, type(self)) and \
            self.name == other.name and self.description == other.description

    def __ne__(self, other):
        '''See __eq__ for more information

        :return: True if the name or description do not match
        '''
        return not self.__eq__(other)

    @property
    def buoys(self):
        '''Buoys Property for this instance

        :return: Copy of the current set of buoys contained in this instance
        '''
        return self._buoys.copy()

    def add_buoy(self, buoy):
        '''Add a buoy to this instance

        .. note:: Buoy names are case sensitive to ensure they are unique

        :param buoy: buoy to be added to the list of buoys.
        :return: True if the buoy was added to the list of buoys
        '''
        if buoy not in self:
            self._buoys[hash(buoy)] = buoy
            return True
        return False

    def get_buoy(self, station):
        '''Get a buoy where the station matches the `station` of the Buoy

        .. note:: Buoy names are case sensitive to ensure they are unique

        :param station: name of the buoy station
        :return: Buoy with a matching station, None if one was not found.
        '''
        return next((v for k, v in self._buoys.items() if v.station == station), None)

    def to_json(self):
        '''Convert this instance to a json dictionary'''
        return {
            "name": self.name,
            "description": self.description if self.description else "",
            "buoys": [value.to_json() for _, value in self.buoys.items()]
        }

    @staticmethod
    def from_json(json_dict):
        '''Create/Fill/Return an instance from a json dictionary'''
        src = Source("nautical_source")
        src.from_dict(json_dict)
        
        if src.name == "nautical_source":
            raise KeyError("Failed to set name during Source::from_json")
    
        return src
        
    def from_dict(self, source_dict):
        '''Fill in instance from a dictionary'''
        if "name" in source_dict and source_dict["name"]:
            self.name = source_dict["name"]
        
        if "description" in source_dict and source_dict["description"]:
            self.description = source_dict["description"]

        if "buoys" in source_dict:
            for buoy_json in source_dict["buoys"]:
                buoy = Buoy.from_json(buoy_json)
                self._buoys[buoy.station] = buoy
