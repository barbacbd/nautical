package buoy

import (
	"fmt"
	"github.com/barbacbd/nautical/nautical/location"
	"hash/fnv"
)

type Buoy struct {

	// Station is the station ID or ID of the buoy
	Station string `json:"station"`

	// Description is the string description for the Buoy
	// +optional
	Description string `json:"description,omitempty"`

	// Location is the geographical location of the buoy
	// +optional
	Location location.Point `json:"location,omitempty"`

	// Present is the current BuoyData associated with this Buoy
	// +optional
	Present *BuoyData `json:"data,omitempty"`

	// Past is a list of BuoyData structs that are from the Past
	// Deprecated: the past variable is still provided for user assistance, but
	// the value is considered deprecated and abandoned
	// +optional
	Past []*BuoyData `json:"past,omitempty"`

	// Determines whether the data stored in this stuct is considered valid
	// +optional
	Valid bool `json:"valid,omitempty"`
}

// Hash returns the hashed string as an integer from Buoy
func (b *Buoy) Hash() uint64 {
	hash := fnv.New64a()

	var hashString string

	if b.Description != "" {
		hashString = fmt.Sprintf("%s %s", b.Station, b.Description)
	} else {
		hashString = b.Station
	}

	hash.Write([]byte(hashString))

	return hash.Sum64()
}

// SetData sets the current data and moves the current data to the past
func (b *Buoy) SetData(data *BuoyData) error {
	if b.Present != nil {

		dataEpoch, err := data.EpochTime()
		if err != nil {
			return nil
		}

		presentEpoch, err := b.Present.EpochTime()
		if err != nil {
			return nil
		}

		if dataEpoch <= presentEpoch {
			return fmt.Errorf("failed to set data, epoch time is older than present data")
		}

		b.Past = append(b.Past, b.Present)
	}

	b.Present = data
	return nil
}