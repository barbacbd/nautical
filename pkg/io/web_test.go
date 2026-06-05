package io

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetNOAAForecastURL(t *testing.T) {
	tests := []struct {
		name     string
		buoyID   string
		expected string
	}{
		{
			name:     "Valid buoy ID",
			buoyID:   "44099",
			expected: "https://www.ndbc.noaa.gov/station_page.php?station=44099",
		},
		{
			name:     "Another valid buoy ID",
			buoyID:   "44025",
			expected: "https://www.ndbc.noaa.gov/station_page.php?station=44025",
		},
		{
			name:     "Empty buoy ID",
			buoyID:   "",
			expected: "https://www.ndbc.noaa.gov/station_page.php?station=",
		},
		{
			name:     "Buoy ID with numbers and letters",
			buoyID:   "TEST123",
			expected: "https://www.ndbc.noaa.gov/station_page.php?station=TEST123",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := GetNOAAForecastURL(tc.buoyID)
			assert.Equal(t, tc.expected, result)
		})
	}
}
