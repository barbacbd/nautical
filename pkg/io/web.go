package io

import "fmt"

const (
	forecastURL = "https://www.ndbc.noaa.gov/station_page.php?station="
)

// GetNOAAForecastURL will return webpage for a NOAA Buoy when supplied with
// a Buoy ID
func GetNOAAForecastURL(buoyID string) string {
	return fmt.Sprintf("%s%s", forecastURL, buoyID)
}
