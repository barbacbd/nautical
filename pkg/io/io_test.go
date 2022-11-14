package io

import (
	nt "github.com/barbacbd/nautical/pkg/time"
	"github.com/stretchr/testify/assert"
	"testing"
)

const (
	GoodCData = `
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />`

	GoodCDataMissingValues = `
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Random Test Data:</b> 11 nmi<br />`

	BadCDataLocation = `
<b>Location:</b> 9.0 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at 15.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />`

	BadCDataWinds = `
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 0000 UTC</b><br /><b>Winds:</b> E (90&#176;) at a15.6 kts gusting at ad19.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />`

	BadCDataTime = `
<b>Location:</b> 9.0N 120.4E
<br /><b>05/10/2022 UTC</b><br /><b>Winds:</b> E (90&#176;) at a15.6 kts gusting at ad19.6 kts<br />
<b>Significant Wave Height:</b> 1.6 ft<br />
<b>Dominant Wave period:</b> 3 sec<br />
<b>Atmospheric Pressure:</b> 29.75 in  and rising<br />
<b>Air Temperature:</b> 84.2 &#176;F<br />
<b>Dew Point:</b> 80.6 &#176;F<br />
<b>Water Temperature:</b> 83.5 &#176;F<br />
<b>Visibility:</b> 11 nmi<br />`
)

func TestCDataWinds(t *testing.T) {
	tests := []struct {
		name      string
		CData     string
		WindSpeed float64
		Gust      float64
		ErrorStr  string
	}{{
		name:      "Good CData Winds No Gust",
		CData:     "Winds: E (90&#176;) at 15.6 kts",
		WindSpeed: 15.6,
		Gust:      0.0,
	}, {
		name:      "Good CData Winds With Gusts",
		CData:     "Winds: E (90&#176;) at 15.6 kts, 30.4",
		WindSpeed: 15.6,
		Gust:      30.4,
	}, {
		name:      "Bad CData No Data Found",
		CData:     "Winds: E (90&#176;) at kts",
		WindSpeed: 0.0,
		Gust:      0.0,
		ErrorStr:  "no wind speed or gust data parsed",
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			winds, gst, err := ParseWinds(tc.CData)

			if err != nil {
				assert.Equal(t, tc.ErrorStr, err.Error())
			}

			assert.Equal(t, tc.WindSpeed, winds)
			assert.Equal(t, tc.Gust, gst)

		})
	}
}

func TestCDataLocation(t *testing.T) {
	tests := []struct {
		name      string
		CData     string
		Latitude  float64
		Longitude float64
		ErrorStr  string
	}{{
		name:      "Good CData Location",
		CData:     "9.0N 120.4E",
		Latitude:  9.0,
		Longitude: 120.4,
	}, {
		name:      "Bad CData No Latitude",
		CData:     "120.4E",
		Longitude: 120.4,
		ErrorStr:  "missing latitude value",
	}, {
		name:     "Bad CData No Longitude",
		CData:    "9.0N",
		Latitude: 9.0,
		ErrorStr: "missing longitude value",
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			point, err := ParseLocation(tc.CData)

			if err != nil {
				assert.Equal(t, tc.ErrorStr, err.Error())
			} else {
				assert.Equal(t, tc.Latitude, point.Latitude)
				assert.Equal(t, tc.Longitude, point.Longitude)
			}
		})
	}
}

func TestCDataTime(t *testing.T) {
	tests := []struct {
		name     string
		CData    string
		Date     NauticalDate
		ErrorStr string
	}{{
		name:  "Good CData Date",
		CData: "05/10/2022 1034 UTC",
		Date: NauticalDate{
			Month: 5,
			Year:  2022,
			Day:   10,
			Time: &nt.NauticalTime{
				Hours:   10,
				Minutes: 34,
			},
		},
	}, {
		name:     "Bad CData Letters in Day",
		CData:    "05/1F/2022 1034 UTC",
		ErrorStr: "strconv.Atoi: parsing \"1F\": invalid syntax",
	}, {
		name:     "Bad CData Letters in Hours",
		CData:    "05/10/2022 1F34 UTC",
		ErrorStr: "strconv.Atoi: parsing \"1F\": invalid syntax",
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			nauticalDate, err := ParseTime(tc.CData)

			if err != nil {
				assert.Equal(t, tc.ErrorStr, err.Error())
			} else {
				assert.Equal(t, tc.Date.Day, nauticalDate.Day)
				assert.Equal(t, tc.Date.Month, nauticalDate.Month)
				assert.Equal(t, tc.Date.Year, nauticalDate.Year)
				assert.Equal(t, tc.Date.Time.Minutes, nauticalDate.Time.Minutes)
				assert.Equal(t, tc.Date.Time.Hours, nauticalDate.Time.Hours)
			}
		})
	}
}

func TestCData(t *testing.T) {
	tests := []struct {
		name       string
		CData      string
		latitude   float64
		longitude  float64
		day        int
		month      int
		year       int
		hours      int
		minutes    int
		windSpeed  float64
		gust       float64
		waveHeight float64
		wavePeriod float64
		pressure   float64
		airTemp    float64
		dewPoint   float64
		waterTemp  float64
		visibility float64
		ErrorStr   string
	}{{
		name:       "Good CData",
		CData:      GoodCData,
		latitude:   9.0,
		longitude:  120.4,
		day:        10,
		month:      5,
		year:       2022,
		minutes:    0,
		hours:      0,
		waveHeight: 1.6,
		wavePeriod: 3,
		pressure:   29.75,
		airTemp:    84.2,
		dewPoint:   80.6,
		waterTemp:  83.5,
		visibility: 11,
		windSpeed:  15.6,
	}, {
		name:       "Good CData Missing Visibility Value",
		CData:      GoodCDataMissingValues,
		latitude:   9.0,
		longitude:  120.4,
		day:        10,
		month:      5,
		year:       2022,
		minutes:    0,
		hours:      0,
		waveHeight: 1.6,
		wavePeriod: 3,
		pressure:   29.75,
		airTemp:    84.2,
		dewPoint:   80.6,
		waterTemp:  83.5,
		windSpeed:  15.6,
	}, {
		name:     "Bad CData Location",
		CData:    BadCDataLocation,
		ErrorStr: "failed to find a matching lat/lon type",
	}, {
		name:     "Bad CData Winds",
		CData:    BadCDataWinds,
		ErrorStr: "no wind speed or gust data parsed",
	}, {
		name:     "Bad CData Time",
		CData:    BadCDataTime,
		ErrorStr: "strconv.Atoi: parsing \"ut\": invalid syntax",
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			buoy, err := ParseCData(tc.CData)

			if err != nil {
				assert.Equal(t, tc.ErrorStr, err.Error())
			} else {
				assert.Equal(t, tc.latitude, buoy.Location.Latitude)
				assert.Equal(t, tc.longitude, buoy.Location.Longitude)
				assert.Equal(t, tc.day, buoy.Present.Day)
				assert.Equal(t, tc.month, buoy.Present.Month)
				assert.Equal(t, tc.year, buoy.Present.Year)
				assert.Equal(t, tc.minutes, buoy.Present.Time.Minutes)
				assert.Equal(t, tc.hours, buoy.Present.Time.Hours)
				assert.Equal(t, tc.waveHeight, buoy.Present.WaveHeight)
				assert.Equal(t, tc.wavePeriod, buoy.Present.DominantWavePeriod)
				assert.Equal(t, tc.pressure, buoy.Present.Pressure)
				assert.Equal(t, tc.airTemp, buoy.Present.AirTemperature)
				assert.Equal(t, tc.dewPoint, buoy.Present.DewPoint)
				assert.Equal(t, tc.waterTemp, buoy.Present.WaterTemperature)
				assert.Equal(t, tc.visibility, buoy.Present.Visibility)
				assert.Equal(t, tc.windSpeed, buoy.Present.WindSpeed)
				assert.Equal(t, tc.gust, buoy.Present.Gust)
			}
		})
	}
}
