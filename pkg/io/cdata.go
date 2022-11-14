package io

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	loc "github.com/barbacbd/nautical/pkg/location"
	buoy "github.com/barbacbd/nautical/pkg/noaa/buoy"
	nt "github.com/barbacbd/nautical/pkg/time"
)

type LocationSign struct {
	LLType string
	Sign   float64
}

type NauticalDate struct {
	Month int
	Day   int
	Year  int
	Time  *nt.NauticalTime
}

var (
	aliasMap = map[string]string{
		"gust":                    "gst",
		"wave height":             "wvht",
		"significant wave height": "wvht",
		"dominant wave period":    "dpd",
		"average wave period":     "apd",
		"atmospheric pressure":    "pres",
		"air temperature":         "atmp",
		"water temperature":       "wtmp",
		"dew point":               "dewp",
		"salinity":                "sal",
		"visibility":              "vis",
		"tide":                    "tide",
		"swell wave height":       "swh",
		"swell wave period":       "swp",
		"wind wave height":        "wwh",
		"wind wave period":        "wwp",
		"wind speed":              "wspd",
	}

	locationMap = map[string]LocationSign{
		"n": {LLType: "latitude", Sign: 1.0},
		"s": {LLType: "latitude", Sign: -1.0},
		"e": {LLType: "longitude", Sign: 1.0},
		"w": {LLType: "longitude", Sign: -1.0},
	}
)

// removeEmpty is a helper function that removes empty string values from
// the original list
func removeEmpty(values []string) []string {
	var validSplitValues []string
	for _, str := range values {
		if str != "" {
			validSplitValues = append(validSplitValues, str)
		}
	}
	return validSplitValues
}

// ParseWinds converts the string wind information that can be retrieved from
// KML into the wind speed and gust information
func ParseWinds(windData string) (float64, float64, error) {
	windSpeed := 0.0
	windSet := false
	gust := 0.0
	gustSet := false

	splitWindData := strings.Split(windData, " ")

	for _, data := range splitWindData {
		value, err := strconv.ParseFloat(data, 64)
		if err == nil {
			if !windSet {
				windSpeed = value
				windSet = true
			} else if !gustSet {
				gust = value
				gustSet = true

				// break out of the loop as this is always last to be set
				break
			}
		}
	}

	if !windSet && !gustSet {
		return windSpeed, gust, fmt.Errorf("no wind speed or gust data parsed")
	}

	return windSpeed, gust, nil
}

// ParseLocation parses the latitude and longitude values out of string that can be retrieved
// from the KML
func ParseLocation(locationData string) (*loc.Point, error) {
	describe := func(data string) (string, float64, string, error) {
		lowerData := strings.ToLower(data)
		for key, value := range locationMap {
			if strings.Contains(lowerData, key) {
				return value.LLType, value.Sign, strings.Replace(lowerData, key, "", -1), nil
			}
		}
		return "", 0.0, "", fmt.Errorf("failed to find a matching lat/lon type")
	}

	var latitude float64
	latitudeSet := false
	var longitude float64
	longitudeSet := false
	splitData := strings.Split(locationData, " ")
	validSplitValues := removeEmpty(splitData)

	for _, value := range validSplitValues {
		llType, sign, strVal, err := describe(value)
		if err != nil {
			return nil, err
		}

		fval, err := strconv.ParseFloat(strVal, 64)
		if err != nil {
			return nil, err
		}

		switch {
		case llType == "latitude":
			latitude = fval * sign
			latitudeSet = true
		case llType == "longitude":
			longitude = fval * sign
			longitudeSet = true
		}
	}

	if !latitudeSet {
		return nil, fmt.Errorf("missing latitude value")
	} else if !longitudeSet {
		return nil, fmt.Errorf("missing longitude value")
	}

	return &loc.Point{Latitude: latitude, Longitude: longitude}, nil
}

// ParseTime parses the time data out of cdata retrieved from KML data.
func ParseTime(timeData string) (*NauticalDate, error) {
	splitTime := strings.Split(timeData, " ")

	dateData := strings.Split(splitTime[0], "/")
	month, err := strconv.Atoi(dateData[0])
	if err != nil {
		return nil, err
	}
	day, err := strconv.Atoi(dateData[1])
	if err != nil {
		return nil, err
	}
	year, err := strconv.Atoi(dateData[2])
	if err != nil {
		return nil, err
	}

	hourMin := splitTime[1]
	hours, err := strconv.Atoi(hourMin[:2])
	if err != nil {
		return nil, err
	}
	minutes, err := strconv.Atoi(hourMin[2:])
	if err != nil {
		return nil, err
	}

	nauticalTime := nt.NauticalTime{Minutes: minutes, Hours: hours, Format: nt.HOUR_24}
	return &NauticalDate{Month: month, Day: day, Year: year, Time: &nauticalTime}, nil
}

// ParseCData will parse the CDATA string that is pulled from the KML.
// On success, the returned Buoy structure should be altered as it will
// indicate that it was auto-filled. The Station and Description will need to be
// set to reflect valid Buoy information.
func ParseCData(cdata string) (*buoy.Buoy, error) {
	buoyData := buoy.BuoyData{}
	station := buoy.Buoy{
		Station:     "AutoFilled",
		Description: "Auto Filled Buoy From Parsed CData",
		Present:     &buoyData,
	}

	xmlData := strings.Split(cdata, "<br />")
	for _, xdVal := range xmlData {

		// Break up the data from the html line breaks
		trimmed := strings.TrimSpace(xdVal)
		trimmed = strings.Replace(trimmed, "<b>", "", -1)
		elements := strings.Split(trimmed, "</b>")

		if len(elements) == 0 {
			continue
		}
		key := strings.ToLower(strings.Replace(elements[0], ":", "", -1))

		switch {
		case key == "winds":
			windSpeed, gust, err := ParseWinds(elements[1])
			if err != nil {
				return nil, err
			}
			station.Present.WindSpeed = windSpeed
			station.Present.Gust = gust
		case key == "location":
			location, err := ParseLocation(elements[1])
			if err != nil {
				return nil, err
			}
			station.Location = loc.Point{Latitude: location.Latitude, Longitude: location.Longitude}
		case strings.Contains(key, "utc"):
			nauticalDate, err := ParseTime(key)
			if err != nil {
				return nil, err
			}
			station.Present.Time = nauticalDate.Time
			station.Present.Day = nauticalDate.Day
			station.Present.Month = nauticalDate.Month
			station.Present.Year = nauticalDate.Year
		default:
			if alias, ok := aliasMap[key]; ok {

				// Split all of the elements and grab the first one as it is the value we need
				validSplitValues := removeEmpty(strings.Split(elements[1], " "))
				val, err := strconv.ParseFloat(validSplitValues[0], 64)
				if err == nil {
					jsonStr := fmt.Sprintf("{\"%s\": %f}", alias, val)
					// nothing to do with the error for now
					json.Unmarshal([]byte(jsonStr), station.Present)
				}
			}
		}
	}

	return &station, nil
}
