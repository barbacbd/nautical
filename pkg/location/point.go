package location

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/barbacbd/nautical/pkg/units"

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

// Convenience functions for x,y,z coordinates of the Point
func (p *Point) X() float64 { return p.Latitude }
func (p *Point) Y() float64 { return p.Longitude }
func (p *Point) Z() float64 { return p.Altitude }

// String function returns the String format of the Point struct
func (p *Point) String() string {
	return fmt.Sprintf("%.2f, %.2f, %.2f", p.Latitude, p.Longitude, p.Altitude)
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
		return fmt.Errorf("longitude not in range (-180, 180): %.2f", longitude)
	}
	p.Longitude = longitude
	return nil
}

// Parse will parse the point from the string formatted data containing the
// latitude, longitude, [optional] altitude.
// Strings with spaces are allowed but newlines and tabs should be avoided
func Parse(coordStr string) (Point, error) {
	// TODO: change to all whitespace?
	// replace spaces, or float conversion fails
	coordStr = strings.ReplaceAll(coordStr, " ", "")
	splitStr := strings.Split(coordStr, ",")

	point := Point{}

	switch {
	case len(splitStr) == 3:
		altitude, err := strconv.ParseFloat(splitStr[2], 8)
		if err != nil {
			return point, err
		}
		point.Altitude = altitude

		fallthrough
	case len(splitStr) == 2:
		longitude, err := strconv.ParseFloat(splitStr[0], 10)
		if err != nil {
			return point, err
		} else {
			if err := point.SetLongitude(longitude); err != nil {
				return point, err
			}
		}

		latitude, err := strconv.ParseFloat(splitStr[1], 10)
		if err != nil {
			return point, err
		} else {
			if err := point.SetLatitude(latitude); err != nil {
				return point, err
			}
		}
	default:
		return point, fmt.Errorf("number of arguments to parse should be 2 or 3: %d", len(splitStr))
	}

	return point, nil
}

// GetDistance will get the distance between two points using the Haversine
// function for coordinates on the earth. The returned distance is in meters.
func (p *Point) GetDistance(other *Point) (float64, error) {

	p1Coords := haversine.Coord{Lat: p.Latitude, Lon: p.Longitude}
	p2Coords := haversine.Coord{Lat: other.Latitude, Lon: other.Longitude}
	_, km := haversine.Distance(p1Coords, p2Coords)

	meters, err := units.ConvertDistance(km, units.KILOMETERS, units.METERS)
	if err != nil {
		return 0, err
	}
	return meters, nil
}

// InRange will determine if this point is in range of another point. The range
// is provided as distance, and the units are assumed to be meters.
func (p *Point) InRange(other *Point, distance float64) (bool, error) {
	dist, err := p.GetDistance(other)
	if err != nil {
		return false, err
	}

	return distance >= dist, nil
}
