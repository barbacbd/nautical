package buoy

import (
	"fmt"
	"time"

	nt "github.com/barbacbd/nautical/pkg/time"
)

// BuoyData contains the scientific data associated with a Buoy
type BuoyData struct {
	// Year is the year the information was retrieved
	Year int `json:"year"`

	// Month is the month the information was retrieved
	Month int `json:"mm"`

	// Day is the day the information was retrieved
	Day int `json:"dd"`

	// time of day that the information was retrieved
	Time *nt.NauticalTime `json:"time,omitempty"`

	// Wind Direction as a string: example `sse`
	WindDirection string `json:"wdir"`

	// Wind Speed in knots
	WindSpeed float64 `json:"wspd"`

	// Gust speed in knots
	Gust float64 `json:"gst"`

	// Mean Wind Direction is the average wind direction
	MeanWindDirection string `json:"mwd"`

	// Mean wind speed over a 10-minute period
	WindSpeed10Min float64 `json:"wspd10m"`

	// Mean wind speed over a 20-minute period
	WindSpeed20Min float64 `json:"wspd20m"`

	// Wave height in feet
	WaveHeight float64 `json:"wvht"`

	// Dominant Wave Period in seconds
	DominantWavePeriod float64 `json:"dpd"`

	// Average Wave Period in seconds
	AverageWavePeriod float64 `json:"apd"`

	// Wind Wave Height in feet
	WindWaveHeight float64 `json:"wwh"`

	// Wind Wave Period in seconds
	WindWavePeriod float64 `json:"wwp"`

	// Direction of Waves due to wind
	WindWaveDirection string `json:"wwd"`

	// Swell Height in feet
	SwellHeight float64 `json:"swh"`

	// Swell Period in seconds
	SwellPeriod float64 `json:"swp"`

	// Direction of Waves of the Swell
	SwellDirection string `json:"swd"`

	// PSI
	Pressure float64 `json:"pres"`

	// PSI
	PressureTendency float64 `json:"ptdy"`

	// Deg F
	AirTemperature float64 `json:"atmp"`

	// Deg F
	WaterTemperature float64 `json:"wtmp"`

	// Deg F
	DewPoint float64 `json:"dewp"`

	// Deg F
	OceanTemperature float64 `json:"otmp"`

	Chill string `json:"chill"`

	Heat string `json:"heat"`

	// PSU
	Salinity float64 `json:"sal"`

	PH string `json:"ph"`

	// Oxygen percent in water
	OxygenPercent float64 `json:"o2pct"`

	// Oxygen parts per million
	OxygenPPM float64 `json:"o2ppm"`

	// Feet
	Depth float64 `json:"depth"`

	NauticalMiles float64 `json:"nmi"`

	// Nautical Miles
	Visibility float64 `json:"vis"`

	// Feet
	Tide float64 `json:"tide"`

	// Other features that Don't fit in other categories
	Steepness string `json:"steepness"`
	Clcon     string `json:"clcon"`
	Turb      string `json:"turb"`
	Cond      string `json:"cond"`
	SRad1     string `json:"srad1"`
	SWRad     string `json:"swrad"`
	LWRad     string `json:"lwrad"`
}

// EpochTime will convert the current time information in this BuoyData struct to
// the epoch time format
func (bd *BuoyData) EpochTime() (int64, error) {

	bdTimeStr, err := bd.Time.String()
	if err != nil {
		return 0, err
	}

	timeStr := fmt.Sprintf("%04d-%02d-%02dT%s+00:00", bd.Year, bd.Month, bd.Day, bdTimeStr)
	ttime, err := time.Parse(time.RFC3339, timeStr)
	if err != nil {
		return 0, fmt.Errorf("failed to parse time format: %s", timeStr)
	}

	epoch := ttime.Unix()
	return epoch, nil
}
