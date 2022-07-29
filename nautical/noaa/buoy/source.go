package buoy

import (
	"fmt"
	"sort"
	"strings"
)

const (
	ALL                       = 0
	INTERNATIONAL_PARTNERS    = 1
	IOOS_PARTNERS             = 2
	MARINE_METAR              = 3
	NDBC_METEOROLOGICAL_OCEAN = 4
	NERRS                     = 5
	NOS_CO_OPS                = 6
	SHIPS                     = 7
	TAO                       = 8
	TSUNAMI                   = 9
)

var (
	SourceTypeMap = map[int]string{
		INTERNATIONAL_PARTNERS:    "International Partners",
		IOOS_PARTNERS:             "IOOS Partners",
		MARINE_METAR:              "Marine METAR",
		NDBC_METEOROLOGICAL_OCEAN: "NDBC Meteorological/Ocean",
		NERRS:                     "NERRS",
		NOS_CO_OPS:                "NOS/CO-OPS",
		SHIPS:                     "Ships",
		TAO:                       "TAO",
		TSUNAMI:                   "Tsunami",
	}
)

// SourceTypeAsString will convert the source type to a readable string.
// In the event that ALL is passed, then all strings are returned as a single
// string with a comma as a delimiter
func SourceTypeAsString(sourceType int) (string, error) {
	if typeStr, ok := SourceTypeMap[sourceType]; ok {
		return typeStr, nil
	} else {

		if sourceType == ALL {
			typeStrs := make([]string, 0, len(SourceTypeMap)-1)
			for key, value := range SourceTypeMap {
				if key == sourceType {
					continue
				} else {
					typeStrs = append(typeStrs, value)
				}
			}

			sort.Strings(typeStrs)

			return strings.Join(typeStrs, ", "), nil
		}

		return "", fmt.Errorf("failed to find SourceType: %d", sourceType)
	}
}

type Source struct {

	// Name of the Source corresponding to Source Type
	Name string `json:"name"`

	// Description for the Source
	Description string `json:"description,omitempty"`

	// Map of Buoys that are contained or associated with[in] this Source
	Buoys map[uint64]*Buoy `json:"buoys,omitempty"`
}

// String returns the string representation of the Source
func (s *Source) String() string {
	return s.Name
}

// Contains determines if the hash of the buoy is contained in this struct.
func (s *Source) Contains(hash uint64) bool {
	_, ok := s.Buoys[hash]
	return ok
}

// GetBuoys will return all Buoy structs. This is not the same as the Map, as it
// returns a list of Buoy Structs without the keys in the map
func (s *Source) GetBuoys() []*Buoy {
	buoys := make([]*Buoy, 0, len(s.Buoys)-1)
	for _, value := range s.Buoys {
		buoys = append(buoys, value)
	}

	return buoys
}

// AddBuoy will add a buoy to the struct
func (s *Source) AddBuoy(buoy Buoy) error {
	hash := buoy.Hash()

	if s.Buoys == nil {
		s.Buoys = make(map[uint64]*Buoy)
	}

	fmt.Println(hash)
	if s.Contains(hash) {
		return fmt.Errorf("buoy already exists: %s", buoy.Station)
	}
	
	s.Buoys[hash] = &buoy
	return nil
}

// GetBuoy will get a buoy from the station Id of the Buoy
func (s *Source) GetBuoy(station string) (*Buoy, error) {

	for _, value := range s.Buoys {
		if value.Station == station {
			return value, nil
		}
	}

	return nil, fmt.Errorf("failed to find buoy with station: %s", station)
}
