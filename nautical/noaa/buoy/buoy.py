from copy import copy
from typing import List
from warnings import warn
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.location.point import Point


class Buoy:

    # pylint: disable=too-many-instance-attributes

    def __init__(self, station, description: str = None, location=None) -> None:
        '''
        :param station: ID of the station
        :param description: snippet of information to describe this station
        :param location: nautical.location.point.Point [optional]
        '''        
        self.station = station
        self.description = description
        self._location: Point = None
        self._present: BuoyData = None
        self._past: List[BuoyData] = []

        if location is not None:
            self.location = location

        # is the instance data considered valid
        self.valid = False

    @property
    def location(self):
        '''Location Property

        :return: Copy of the location (Point)
        '''
        return copy(self._location)

    @location.setter
    def location(self, loc):
        '''Location setter/validity checker

        :param loc: Location or Point object to be set for the location of this instance
        '''
        if isinstance(loc, Point):
            self._location = loc

    @property
    def data(self):
        '''Copy of `present` Property. This is an expansion function
        for use when the `past` was deprecated.

        :return: Copy of the `present` data stored in this instance
        '''
        return self.present

    @property
    def present(self):
        '''Present Property, the present data stored in this instance. 
        This is the most recent set of buoy data that was retrieved.

        :return: Copy of the `present` data stored in this instance
        '''
        return copy(self._present)

    @data.setter
    def data(self, present_data):
        '''Data Setter/validity checker. See `present` setter for more information.'''
        self.present = present_data

    @present.setter
    def present(self, present_data):
        '''Present Property Setter/validity Checker.
        If this instance of present data is a BuoyData object and the time is
        more recent that the previous present data, then the old present data
        is moved to the past data and the new instance is kept as the present data.

        :param present_data: instance or candidate for present data (BuoyData)
        '''
        if isinstance(present_data, BuoyData):
            if self._present:
                if present_data.epoch_time > self._present.epoch_time:
                    self._update_past(self._present)
                else:
                    raise ValueError("Failed to set present data, time is in the past.")

            self._present = present_data

    @property
    def past(self):
        '''Past Property.

        :return: all past instances of Buoy Data objects stored in this instance.
        '''
        warn(f"{self.__class__.__name__} past is deprecated", DeprecationWarning, stacklevel=2)
        return self._past[:]

    @past.setter
    def past(self, past_data):
        '''The user may pass in a single instance of NOAAData or a list of these
        objects to fill in the past data with.

        :param past_data: list or since instance of BuoyData that is used to fill in the past
        '''
        warn(f"{self.__class__.__name__} past is deprecated", DeprecationWarning, stacklevel=2)
        if isinstance(past_data, BuoyData):
            self._update_past(past_data)
        elif isinstance(past_data, list):
            for data in past_data:
                if isinstance(data, BuoyData):
                    self._update_past(data)

    def _update_past(self, past_data):
        '''Attempt to update the past data, but make sure that this particular
        NOAA data does not already have a time entry that matches.

        :param p: Buoy Data attempting to be added to the past information.
        '''
        data = next((x for x in self._past if x.epoch_time == past_data.epoch_time), None)

        if not data:
            self._past.append(past_data)

    def __str__(self):
        '''If the location of this buoy is known return the location and the name,
        otherwise just return the name

        :return: string representation of this Buoy
        '''
        if not self._location:
            return str(self.station)
        return f"{self.station} at {str(self._location)}"

    def __eq__(self, other):
        '''The stations are considered equal if their station ID is the same as the
        station IDs are meant to be unique. The special case is `SHIP`.

        :param other: Buoy object to compare to this instance.
        :return: True when the two objects are the same
        '''
        return isinstance(other, type(self)) and self.station == other.station

    def __ne__(self, other):
        '''See __eq__ for more information.

        :return: The opposite of __eq__ (==)
        '''
        return not self.__eq__(other)

    def __hash__(self):
        '''The reason behind a private station and description is that they are used for the
        hash function. The hash shouldn't be able to change during execution.

        :return: hash of the station combined with the hash of the description.
        '''
        return hash(str(self.station)) * hash(self.description) \
            if self.description else hash(str(self.station))

    def to_json(self):
        '''Create a json dictionary representation of this instance'''
        json_dict = {
            "station": self.station,
            "description": self.description if self.description else "",
            "valid": self.valid,
            "location": self._location.to_json() if self._location else "",
            "data": self._present.to_json() if self._present else ""
        }
        return json_dict

    @staticmethod
    def from_json(json_dict):
        '''Return a Buoy object created from a json dictionary'''
        buoy = Buoy("nautical_example")
        buoy.from_dict(json_dict)
        
        if buoy.station == "nautical_example":
            raise KeyError("Failed to set station during Buoy::from_json")
        
        return buoy

    def from_dict(self, buoy_dict):
        '''Fill this instance from a dictionary'''
        if "station" in buoy_dict and buoy_dict["station"]:
            self.station = buoy_dict["station"]
        
        if "description" in buoy_dict and buoy_dict["description"]:
            self.description = buoy_dict["description"]
        
        if "valid" in buoy_dict:
            self.valid = bool(buoy_dict["valid"])
        
        if "location" in buoy_dict and buoy_dict["location"]:
            self._location = Point.from_json(buoy_dict["location"])
        
        if "data" in buoy_dict and buoy_dict["data"]:
            self._present = BuoyData.from_json(buoy_dict["data"])
