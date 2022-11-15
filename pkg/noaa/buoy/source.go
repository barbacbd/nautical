package buoy

import (
	"encoding/xml"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
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

	// NOAASourcesURL is the URL where all of the source data is supplied as KML
	NOAASourcesURL = "https://www.ndbc.noaa.gov/kml/marineobs_as_kml.php?sort=pgm"

	expectedFile = "marineobs_as_kml.php"
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

// XMLDoc assists in the xml/kml parsing. The struct represents the entry point of the document.
type XMLDoc struct {
	Sources []Source `xml:"Document>Folder>Folder"`
}

// Source represents a group of buoys. The Source also contains details about
// the grouping such as a description of why/how the buoys are grouped.
type Source struct {
	// Name of the Source corresponding to Source Type
	Name string `json:"name" xml:"name"`

	// Description for the Source
	Description string `json:"description,omitempty" xml:"description"`

	// Map of Buoys that are contained or associated with[in] this Source
	Buoys map[uint64]*Buoy `json:"buoys,omitempty"`

	// Placemarks are the xml version of the Buoy information. These
	// require additional parsing, so they are NOT interchangeable with
	// the Buoy Structs
	Placemarks []Placemark `xml:"Placemark"`
}

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
	}
	return "", fmt.Errorf("failed to find SourceType: %d", sourceType)
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
func (s *Source) AddBuoy(buoy *Buoy) error {
	hash := buoy.Hash()

	if s.Buoys == nil {
		s.Buoys = make(map[uint64]*Buoy)
	}

	if s.Contains(hash) {
		return fmt.Errorf("buoy already exists: %s", buoy.Station)
	}

	s.Buoys[hash] = buoy
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

// GetBuoySources will parse and create sources from the NOAA link:
// https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml
func GetBuoySources() ([]*Source, error) {
	filename, err := downloadSourcesFile()
	if err != nil {
		return nil, err
	}

	xmlFile, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer xmlFile.Close()
	byteValue, _ := ioutil.ReadAll(xmlFile)
	var myXMLDoc XMLDoc
	xml.Unmarshal(byteValue, &myXMLDoc)

	sources := []*Source{}
	for _, source := range myXMLDoc.Sources {
		s := &source
		for _, pm := range s.Placemarks {
			buoy, err := ParseCData(pm.Description)
			if err != nil {
				continue
			}
			buoy.Station = pm.Name
			buoy.Description = fmt.Sprintf("KML Parsed Buoy information for %s", pm.Description)
			if err := s.AddBuoy(buoy); err != nil {
				continue
			}
		}
	}

	if err := removeSourcesFile(filename); err != nil {
		return sources, err
	}
	return sources, nil
}

// downloadSourcesFile downloads the KML file from the url source. The file contains
// all NOAA Source information as KML.
func downloadSourcesFile() (string, error) {
	// Build filename from the path
	fileURL, err := url.Parse(NOAASourcesURL)
	if err != nil {
		return "", err
	}
	path := fileURL.Path
	segments := strings.Split(path, "/")
	filename := segments[len(segments)-1]

	// Create a blank file where the data will be stored
	file, err := os.Create(filename)
	if err != nil {
		return "", err
	}
	client := http.Client{
		CheckRedirect: func(r *http.Request, via []*http.Request) error {
			r.URL.Opaque = r.URL.Path
			return nil
		},
	}

	// Grab the data from the URL
	resp, err := client.Get(NOAASourcesURL)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	// Copy the contents from the website to the file
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		return "", err
	}
	defer file.Close()

	return filename, nil
}

// removeSourcesFile removes the file if it exists
func removeSourcesFile(filename string) error {
	if _, err := os.Stat(filename); err == nil {
		if err := os.Remove(filename); err != nil {
			return err
		}
	}
	return nil
}
