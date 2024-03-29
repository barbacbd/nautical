package buoy

import (
	"encoding/json"
	"fmt"
	"hash/fnv"
	"regexp"
	"strconv"
	"strings"

	"github.com/anaskhan96/soup"

	"github.com/barbacbd/nautical/pkg/io"
	"github.com/barbacbd/nautical/pkg/location"
	"github.com/barbacbd/nautical/pkg/util"
)

var (
	// NauticalRegex is a regular expression to find values between the parentheses
	NauticalRegex = regexp.MustCompile(`\((.*?)\)`)

	// aliases is a set of all alias names for variables of a buoy
	aliases = util.GetAliases(BuoyData{})
)


// Buoy represents a NOAA buoy.
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

// Placemark is the xml structure for a Buoy. It is a very different
// format than the normal Buoy
type Placemark struct {
	// Name is the name tag in the Placemark that should match the
	// name of a Buoy
	Name string `xml:"name"`
	// Description is the description tag of the Placemark that should
	// match the description of the Buoy
	Description string `xml:"description"`
	// Placement is the location of the buoy
	Placement location.Point `xml:"LookAt"`
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

// CreateBuoy will provide a full workup for a specific buoy. When the
// buoy with matching station is not found, an error is returned.
func CreateBuoy(stationID string) (*Buoy, error) {
	station := &Buoy{Station: stationID}

	err := station.FillBuoy()
	if err != nil {
		return nil, err
	}

	if !station.Valid {
		return nil, fmt.Errorf("buoy %s is not valid", stationID)
	}

	return station, nil
}

// FillBuoy will fill a Buoy struct with the data parsed from the web
func (b *Buoy) FillBuoy() error {
	url := io.GetNOAAForecastURL(b.Station)
	root, err := io.GetURLSource(url)
	if err != nil {
		return err
	}

	search := []string{fmt.Sprintf("Conditions at %s", b.Station), "Detailed Wave Summary"}
	if err := b.GetCurrentData(root, search); err != nil {
		return err
	}
	return nil
}

// GetCurrentData parses the current data for a buoy from the NOAA website
func (b *Buoy) GetCurrentData(root *soup.Root, search []string) error {
	buoyVariablesSet := false

	tables := map[string]soup.Root{}

	// Find all tables that have a caption that matches any of
	// the search criteria
	suspectTables := root.FindAll("table")
	for _, suspect := range suspectTables {
		captions := suspect.FindAll("caption")
		captionText := []string{}
		for _, caption := range captions {
			captionText = append(captionText, caption.Text())
		}
		for _, searchText := range search {
			for _, ct := range captionText {
				if strings.Contains(ct, searchText) {
					if _, ok := tables[ct]; !ok {
						tables[ct] = suspect
					}

				}
			}
		}
	}

	for _, table := range tables {
		allTR := table.FindAll("tr")
		for i, row := range allTR {
			if i >= 1 {
				cells := row.FindAll("td")
				if len(cells) >= 2 {
					// for idx, cell := range cells {
					submatchall := NauticalRegex.FindAllString(cells[0].Text(), -1)
					if len(submatchall) > 0 {
						// Trim the () off of the value so that we can use the variable name
						alias := strings.Trim(strings.Trim(strings.ToLower(submatchall[0]), "("), ")")

						// Make sure that this is data that we are expecting
						if aliases.Has(alias) {
							splitCell := RemoveEmpty(strings.Split(cells[1].Text(), " "))
							val, err := strconv.ParseFloat(splitCell[0], 64)
							if err != nil {
								json.Unmarshal([]byte(fmt.Sprintf("{\"%s\": \"%s\"}", alias, splitCell[0])), b.Present)
							} else {
								json.Unmarshal([]byte(fmt.Sprintf("{\"%s\": %f}", alias, val)), b.Present)
							}
							buoyVariablesSet = true
						}
					}
				}
			}
		}
	}

	b.Valid = buoyVariablesSet
	if !buoyVariablesSet {
		return fmt.Errorf("no buoy variables set")
	}
	return nil
}
