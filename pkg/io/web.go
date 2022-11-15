package io

import (
	"fmt"
	
	"github.com/anaskhan96/soup"
)

const (
	forecastURL = "https://www.ndbc.noaa.gov/station_page.php?station="
)

// GetNOAAForecastURL will return webpage for a NOAA Buoy when supplied with
// a Buoy ID
func GetNOAAForecastURL(buoyID string) string {
	return fmt.Sprintf("%s%s", forecastURL, buoyID)
}

// GetURLSource will get the Soup Root struct associated with the provided url
func GetURLSource(url string) (*soup.Root, error) {
	resp, err := soup.Get(url)
	if err != nil {
		return nil, err
	}

	doc := soup.HTMLParse(resp)
	return &doc, nil
}
