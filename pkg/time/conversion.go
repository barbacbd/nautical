package time

import (
	"fmt"
	"strconv"
	"strings"
)

const (
	nonBreakingSpace string = "&nbsp;"
)

// ConvertNOAATime converts a string time into a NauticalTime struct.
// Strings originating on NOAA's website have the `nonBreakingSpace` embedded
// in them. This function will parse these strings as well as strings formatted
// from the String function from the NauticalTime struct in the format: "00:00:00".
// Strings in the format "00:00 AM/PM" will also be parsed here.
func ConvertNOAATime(originalTimeStr string) (*NauticalTime, error) {
	midday := 0
	timeStr := ""

	splitStr := strings.Split(originalTimeStr, nonBreakingSpace)

	if len(splitStr) == 2 {
		switch {
		case strings.EqualFold(splitStr[1], "PM"):
			midday = PM
		case strings.EqualFold(splitStr[1], "AM"):
			midday = AM
		default:
			return nil, fmt.Errorf("failed to find midday value: %s", splitStr[1])
		}

		timeStr = splitStr[0]
	} else if len(splitStr) == 1 {
		timeStr = splitStr[0]
		if strings.HasSuffix(timeStr, "PM") || strings.HasSuffix(timeStr, "pm") {
			timeStr = strings.Replace(timeStr, "PM", "", -1)
			timeStr = strings.Replace(timeStr, "pm", "", -1)
			midday = PM
		} else if strings.HasSuffix(timeStr, "AM") || strings.HasSuffix(timeStr, "am") {
			timeStr = strings.Replace(timeStr, "AM", "", -1)
			timeStr = strings.Replace(timeStr, "am", "", -1)
			midday = AM
		}
	} else {
		timeStr = originalTimeStr
	}

	splitTime := strings.Split(timeStr, ":")
	if len(splitTime) >= 2 {

		hours, err := strconv.Atoi(splitTime[0])
		if err != nil {
			return nil, err
		}

		minutes, err := strconv.Atoi(splitTime[1])
		if err != nil {
			return nil, err
		}

		nauticalTime := NauticalTime{Hours: hours, Minutes: minutes, Format: HOUR_24}
		if midday > 0 {
			nauticalTime.Format = HOUR_12
			nauticalTime.Midday = midday
		}

		return &nauticalTime, nil
	}

	return nil, fmt.Errorf("failed to parse time string: %s", originalTimeStr)
}
