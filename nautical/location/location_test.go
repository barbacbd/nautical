package location

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestConvertPoint(t *testing.T) {
	tests := []struct {
		name        string
		locationStr string
		latitude    float64
		longitude   float64
		altitude    float64
		expectedErr string
	}{{
		name:        "Correct Parse Point No Altitude",
		locationStr: "-110.123, 76.45",
		latitude:    76.45,
		longitude:   -110.123,
		altitude:    0.0,
	}, {
		name:        "Correct Parse Point With Altitude",
		locationStr: "-110.123, 76.45, 123.67",
		latitude:    76.45,
		longitude:   -110.123,
		altitude:    123.67,
	}, {
		name:        "Parse Failure Missing Last Value",
		locationStr: "-110.123, 76.45,",
		expectedErr: "strconv.ParseFloat: parsing \"\": invalid syntax",
	}, {
		name:        "Parse Failure Bad Latitude",
		locationStr: "-110.123, sdffgsdfg, 123.67",
		expectedErr: "strconv.ParseFloat: parsing \"sdffgsdfg\": invalid syntax",
	}, {
		name:        "Parse Failure Bad Longitude",
		locationStr: "sdffgsdfg, 45.123 123.67",
		expectedErr: "strconv.ParseFloat: parsing \"sdffgsdfg\": invalid syntax",
	}, {
		name:        "Parse Failure Too Many Args",
		locationStr: "sdffgsdfg, 45.123, 123.67, 3423, 34123",
		expectedErr: "number of arguments to parse should be 2 or 3: 5",
	}, {
		name:        "Parse Failure Too Few Args",
		locationStr: "100.213",
		expectedErr: "number of arguments to parse should be 2 or 3: 1",
	}, {
		name:        "Parse Failure Longitude Out of Bounds",
		locationStr: "181.213, 74.123",
		expectedErr: "longitude not in range (-180, 180): 181.21",
	}, {
		name:        "Parse Failure Latitude Out of Bounds",
		locationStr: "100.213, -100.123",
		expectedErr: "latitude not in range (-90, 90): -100.12",
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			point, err := Parse(tc.locationStr)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.latitude, point.Latitude)
				assert.Equal(t, tc.longitude, point.Longitude)
				assert.Equal(t, tc.altitude, point.Altitude)
			}
		})
	}
}

func TestInRange(t *testing.T) {
	tests := []struct {
		name        string
		pointOne    Point
		pointTwo    Point
		distance    float64
		inRange     bool
		expectedErr string
	}{{
		name:     "Test Valid In Range",
		pointOne: Point{Latitude: 36.0, Longitude: -75.0},
		pointTwo: Point{Latitude: 37.0, Longitude: -76.0},
		distance: 150000.0,
		inRange:  true,
	}, {
		name:     "Test Valid Not In Range",
		pointOne: Point{Latitude: 36.0, Longitude: -75.0},
		pointTwo: Point{Latitude: 37.0, Longitude: -76.0},
		distance: 100.0,
		inRange:  false,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			inrange, err := tc.pointOne.InRange(&tc.pointTwo, tc.distance)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.inRange, inrange)
			}
		})
	}
}

func TestDistance(t *testing.T) {
	tests := []struct {
		name        string
		pointOne    Point
		pointTwo    Point
		expDistance float64
		expectedErr string
	}{{
		name:        "Test Valid Distance Meters",
		pointOne:    Point{Latitude: 36.0, Longitude: -75.0},
		pointTwo:    Point{Latitude: 37.0, Longitude: -76.0},
		expDistance: 142665.16,
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			distance, err := tc.pointOne.GetDistance(&tc.pointTwo)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.InDelta(t, tc.expDistance, distance, 0.01)
			}
		})
	}
}

func TestInRangeLL(t *testing.T) {
	tests := []struct {
		name        string
		latOne      float64
		lonOne      float64
		latTwo      float64
		lonTwo      float64
		distance    float64
		inRange     bool
		expectedErr string
	}{{
		name:     "Test Valid In Range",
		latOne:   36.0,
		lonOne:   -75.0,
		latTwo:   37.0,
		lonTwo:   -76.0,
		distance: 150000.0,
		inRange:  true,
	}, {
		name:     "Test Valid Not In Range",
		latOne:   36.0,
		lonOne:   -75.0,
		latTwo:   37.0,
		lonTwo:   -76.0,
		distance: 100.0,
		inRange:  false,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			inrange, err := InRangeLL(tc.latOne, tc.lonOne, tc.latTwo, tc.lonTwo, tc.distance)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.inRange, inrange)
			}
		})
	}
}

func TestInArea(t *testing.T) {
	tests := []struct {
		name        string
		geometry    []Point
		point       Point
		inside      bool
		expectedErr string
	}{{
		name: "In Area Simple",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
		},
		point:       Point{Latitude: 36.854422, Longitude: -75.854998},
		expectedErr: "geometry must be a set of at least 2 points",
	}, {
		name: "In Area Simple",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.867840, Longitude: -75.813113},
		},
		point:  Point{Latitude: 36.854422, Longitude: -75.854998},
		inside: true,
	}, {
		name: "Not In Area Simple",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.867840, Longitude: -75.813113},
		},
		point:  Point{Latitude: 36.876079, Longitude: -75.736208},
		inside: false,
	}, {
		name: "Test In Square",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.849403, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.9408287},
		},
		point:  Point{Latitude: 36.854422, Longitude: -75.854998},
		inside: true,
	}, {
		name: "Test Square Edge Out",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.849403, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.9408287},
		},
		point:  Point{Latitude: 36.854422, Longitude: -75.9408287},
		inside: false,
	}, {
		name: "Test Square Corner Out",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.849403, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.9408287},
		},
		point:  Point{Latitude: 36.867840, Longitude: -75.9408287},
		inside: false,
	}, {
		name: "Test Square Out",
		geometry: []Point{
			Point{Latitude: 36.849403, Longitude: -75.9408287},
			Point{Latitude: 36.849403, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.813113},
			Point{Latitude: 36.867840, Longitude: -75.9408287},
		},
		point:  Point{Latitude: 36.876079, Longitude: -75.736208},
		inside: false,
	}, {
		name: "Test Complex Geometry Point In",
		geometry: []Point{
			Point{Latitude: 36.932651, Longitude: -75.852713},
			Point{Latitude: 36.824144, Longitude: -75.800303},
			Point{Latitude: 36.862386, Longitude: -75.784889},
			Point{Latitude: 36.808101, Longitude: -75.700108},
			Point{Latitude: 36.916631, Longitude: -75.650781},
		},
		point:  Point{Latitude: 36.84, Longitude: -75.742},
		inside: true,
	}, {
		name: "Test Complex Geometry Point Out",
		geometry: []Point{
			Point{Latitude: 36.932651, Longitude: -75.852713},
			Point{Latitude: 36.824144, Longitude: -75.800303},
			Point{Latitude: 36.862386, Longitude: -75.784889},
			Point{Latitude: 36.808101, Longitude: -75.700108},
			Point{Latitude: 36.916631, Longitude: -75.650781},
		},
		point:  Point{Latitude: 36.916631, Longitude: -75.650781},
		inside: false,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			inside, err := InArea(tc.geometry, tc.point)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.inside, inside)
			}
		})
	}
}
