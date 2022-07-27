package location

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/barbacbd/nautical/nautical/units"

	"github.com/umahmood/haversine"
)

type Point struct {

	// Latitude degrees for the world coordinates
	Latitude float64 `json:"latitude,omitempty"`

	// Longitude degrees for the world coordinates
	Longitude float64 `json:"longitude,omitempty"`

	// Altitude in meters above sea level. Negative values
	// are considered to be depth.
	Altitude float64 `json:"altitude,omitempty"`
}

// SetLatitude adds some protection to the ability to set the latitude degrees for
// the global coordinates
func (p *Point) SetLatitude(latitude float64) error {
	if latitude > 90 || latitude < -90 {
		return fmt.Errorf("latitude not in range (-90, 90): %.2f", latitude)
	}
	p.Latitude = latitude
	return nil
}

// SetLongitude adds some protection to the ability to set the longitude degrees for
// the global coordinates
func (p *Point) SetLongitude(longitude float64) error {
	if longitude > 180 || longitude < -180 {
		return fmt.Errorf("latitude not in range (-180, 180): %.2f", longitude)
	}
	p.Longitude = longitude
	return nil
}

// Parse will parse the point from the string formatted data containing the
// latitude, longitude, [optional] altitude
func Parse(coordStr string) (*Point, error) {
	splitStr := strings.Split(coordStr, ",")

	point := Point{}

	switch {
	case len(splitStr) == 3:
		altitude, err := strconv.ParseFloat(splitStr[2], 8)
		if err != nil {
			return nil, err
		}
		point.Altitude = altitude

		fallthrough
	case len(splitStr) == 2:
		longitude, err := strconv.ParseFloat(splitStr[0], 10)
		if err != nil {
			return nil, err
		} else {
			if err := point.SetLongitude(longitude); err != nil {
				return nil, err
			}
		}

		latitude, err := strconv.ParseFloat(splitStr[1], 10)
		if err != nil {
			return nil, err
		} else {
			if err := point.SetLatitude(latitude); err != nil {
				return nil, err
			}
		}
	default:
		return nil, fmt.Errorf("number of arguments to parse should be 2 or 3: %d", len(splitStr))
	}

	return &point, nil
}

func (p *Point) GetDistance(other *Point) float64 {

	p1Coords := haversine.Coord{Lat: p.Latitude, Lon: p.Longitude}
	p2Coords := haversine.Coord{Lat: other.Latitude, Lon: other.Longitude}
	_, km := haversine.Distance(p1Coords, p2Coords)

	return units.ConvertDistance(km, units.KILOMETERS, units.METERS)
}
