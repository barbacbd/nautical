package io

import (
	"net/http"
	"net/http/httptest"
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

func TestGetURLSource(t *testing.T) {
	t.Run("Valid HTML page", func(t *testing.T) {
		ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Content-Type", "text/html")
			w.Write([]byte("<html><body><h1>Test Page</h1></body></html>"))
		}))
		defer ts.Close()

		root, err := GetURLSource(ts.URL)
		assert.NoError(t, err)
		assert.NotNil(t, root)

		h1 := root.Find("h1")
		assert.Equal(t, "Test Page", h1.Text())
	})

	t.Run("Invalid URL", func(t *testing.T) {
		_, err := GetURLSource("http://127.0.0.1:1")
		assert.Error(t, err)
	})
}
