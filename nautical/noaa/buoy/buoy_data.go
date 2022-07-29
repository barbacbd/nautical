package buoy

import (
	"fmt"
	"time"

	nt "github.com/barbacbd/nautical/nautical/time"
)

type BuoyData struct {

	// Year is the year the information was retrieved
	Year int `json:"year,omitempty"`

	// Month is the month the information was retrieved
	Month int `json:"mm,omitempty"`

	// Day is the day the information was retrieved
	Day int `json:"dd,omitempty"`

	// time of day that the information was retrieved
	Time *nt.NauticalTime `json:"time,omitempty"`

	// Wind Direction as a string: example `sse`
	WindDirection string `json:"wdir,omitempty"`

	// Wind Speed in knots
	WindSpeed float64 `json:"wspd,omitempty"`

	// Gust speed in knots
	Gust float64 `json:"gst,omitempty"`

	// Mean Wind Direction is the average wind direction
	MeanWindDirection string `json:"mwd,omitempty"`

	// Mean wind speed over a 10-minute period
	WindSpeed10Min float64 `json:"wspd10m,omitempty"`

	// Mean wind speed over a 20-minute period
	WindSpeed20Min float64 `json:"wspd20m,omitempty"`

	// Wave height in feet
	WaveHeight float64 `json:"wvht,omitempty"`

	// Dominant Wave Period in seconds
	DominantWavePeriod float64 `json:"dpd,omitempty"`

	// Average Wave Period in seconds
	AverageWavePeriod float64 `json:"apd,omitempty"`

	// Wind Wave Height in feet
	WindWaveHeight float64 `json:"wwh,omitempty"`

	// Wind Wave Period in seconds
	WindWavePeriod float64 `json:"wwp,omitempty"`

	// Direction of Waves due to wind
	WindWaveDirection string `json:"wwd,omitempty"`

	// Swell Height in feet
	SwellHeight float64 `json:"swh,omitempty"`

	// Swell Period in seconds
	SwellPeriod float64 `json:"swp,omitempty"`

	// Direction of Waves of the Swell
	SwellDirection string `json:"swd,omitempty"`

	// PSI
	Pressure float64 `json:"pres,omitempty"`

	// PSI
	PressureTendency float64 `json:"ptdy,omitempty"`

	// Deg F
	AirTemperature float64 `json:"atmp,omitempty"`

	// Deg F
	WaterTemperature float64 `json:"wtmp,omitempty"`

	// Deg F
	DewPoint float64 `json:"dewp,omitempty"`

	// Deg F
	OceanTemperature float64 `json:"otmp,omitempty"`

	Chill string `json:"chill,omitempty"`

	Heat string `json:"heat,omitempty"`

	// PSU
	Salinity float64 `json:"sal,omitempty"`

	PH string `json:"ph,omitempty"`

	// Oxygen percent in water
	OxygenPercent float64 `json:"o2pct,omitempty"`

	// Oxygen parts per million
	OxygenPPM float64 `json:"o2ppm,omitempty"`

	// Feet
	Depth float64 `json:"depth,omitempty"`

	NauticalMiles float64 `json:"nmi,omitempty"`

	// Nautical Miles
	Visibility float64 `json:"vis,omitempty"`

	// Feet
	Tide float64 `json:"tide,omitempty"`

	// Other features that Don't fit in other categories
	Steepness string `json:"steepness,omitempty"`
	Clcon     string `json:"clcon,omitempty"`
	Turb      string `json:"turb,omitempty"`
	Cond      string `json:"cond,omitempty"`
	SRad1     string `json:"srad1,omitempty"`
	SWRad     string `json:"swrad,omitempty"`
	LWRad     string `json:"lwrad,omitempty"`
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
