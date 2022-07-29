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
