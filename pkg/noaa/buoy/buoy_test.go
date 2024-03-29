package buoy

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"testing"

	"github.com/barbacbd/nautical/pkg/time"

	"github.com/anaskhan96/soup"
	"github.com/stretchr/testify/assert"
)

func TestBuoyDataEpoch(t *testing.T) {
	tests := []struct {
		name        string
		jsonStr     string
		expectedET  int64
		expectedErr string
	}{{
		name:       "Epoch Time test from json",
		jsonStr:    `{"year": 2000, "mm": 5, "dd": 14, "time": {"hours": 8, "minutes": 30}}`,
		expectedET: 958293000,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			var data BuoyData
			err := json.Unmarshal([]byte(tc.jsonStr), &data)

			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {

				epochTime, err := data.EpochTime()
				if err != nil {
					assert.Equal(t, tc.expectedErr, err.Error())
				} else {
					assert.Equal(t, tc.expectedET, epochTime)
				}
			}
		})
	}
}

func TestBuoySetData(t *testing.T) {
	tests := []struct {
		name            string
		startBuoy       Buoy
		newBuoyData     BuoyData
		expectedPastLen int
		expectedErr     string
	}{{
		name:      "Buoy Set Data On Empty",
		startBuoy: Buoy{Station: "FakeStation"},
		newBuoyData: BuoyData{
			Time:  &time.NauticalTime{Minutes: 30, Hours: 8, Format: time.HOUR_24},
			Year:  2000,
			Month: 5,
			Day:   14,
		},
		expectedPastLen: 0,
	}, {
		name: "Buoy Set Data Present Already Set",
		startBuoy: Buoy{
			Station: "FakeStation",
			Present: &BuoyData{
				Time:  &time.NauticalTime{Minutes: 30, Hours: 8, Format: time.HOUR_24},
				Year:  2000,
				Month: 5,
				Day:   14,
			},
		},
		newBuoyData: BuoyData{
			Time:  &time.NauticalTime{Minutes: 30, Hours: 9, Format: time.HOUR_24},
			Year:  2000,
			Month: 5,
			Day:   14,
		},
		expectedPastLen: 1,
	}, {
		name: "Buoy Set Data Fail Present Already Set Same Time",
		startBuoy: Buoy{
			Station: "FakeStation",
			Present: &BuoyData{
				Time:  &time.NauticalTime{Minutes: 30, Hours: 9, Format: time.HOUR_24},
				Year:  2000,
				Month: 5,
				Day:   14,
			},
		},
		newBuoyData: BuoyData{
			Time:  &time.NauticalTime{Minutes: 30, Hours: 9, Format: time.HOUR_24},
			Year:  2000,
			Month: 5,
			Day:   14,
		},
		expectedPastLen: 1,
		expectedErr:     "failed to set data, epoch time is older than present data",
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			err := tc.startBuoy.SetData(&tc.newBuoyData)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, len(tc.startBuoy.Past), tc.expectedPastLen)
			}
		})
	}
}

func TestAddBuoy(t *testing.T) {
	tests := []struct {
		name        string
		source      Source
		newBuoy     Buoy
		expectedErr string
	}{{
		name: "Add Station to Blank Source",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
		},
		newBuoy: Buoy{Station: "ExampleBuoy"},
	}, {
		name: "Add Station to Source With Other Buoys",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys: map[uint64]*Buoy{
				1234: &Buoy{Station: "ExampleBuoy1"},
				2345: &Buoy{Station: "ExampleBuoy2"},
				3456: &Buoy{Station: "ExampleBuoy3"},
			},
		},
		newBuoy: Buoy{Station: "ExampleBuoy"},
	}, {
		name: "Add Station to Source With Other Buoys Same ID",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys: map[uint64]*Buoy{
				13226671306703588120: &Buoy{Station: "ExampleBuoy1"},
				13226671306703588121: &Buoy{Station: "ExampleBuoy2"},
				13226671306703588122: &Buoy{Station: "ExampleBuoy3"},
			},
		},
		newBuoy:     Buoy{Station: "ExampleBuoy"},
		expectedErr: "buoy already exists: ExampleBuoy",
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			originalLen := len(tc.source.Buoys)
			err := tc.source.AddBuoy(&tc.newBuoy)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, originalLen+1, len(tc.source.Buoys))
			}
		})
	}
}

func TestFillBuoy(t *testing.T) {

	tests := []struct {
		name               string
		filename           string
		search             []string
		waveHeight         float64
		airTemp            float64
		waterTemp          float64
		salinity           float64
		windSpeed          float64
		windDirection      string
		gust               float64
		windSpeed10Min     float64
		windSpeed20Min     float64
		errString          string
	}{{
		name:               "Valid Buoy Loading",
		filename:           "../../../tests/ValidBuoy.html",
		search:             []string{"Conditions at 44072", "Detailed Wave Summary"},
		waveHeight:         0.3,
		airTemp:            64.0,
		waterTemp:          67.6,
		salinity:           19.98,
		windSpeed:          9.7, 
		windDirection:      "NNE",
		gust:               11.7,
		windSpeed10Min:     9.7,
		windSpeed20Min:     11.7,
	}, {
		name:      "Invalid Buoy Loading",
		filename:  "../../../tests/InvalidBuoy.html",
		search:    []string{"Conditions at 44099", "Detailed Wave Summary"},
		errString: "no buoy variables set",
	},
	}

	path, err := os.Getwd()
	if err != nil {
		t.Fail()
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			fullFilePath := fmt.Sprintf("%s/%s", path, tc.filename)
			body, err := ioutil.ReadFile(fullFilePath)
			if err != nil {
				t.Fail()
			}
			doc := soup.HTMLParse(string(body))
			station := Buoy{
				Present: &BuoyData{},
			}

			err = station.GetCurrentData(&doc, tc.search)
			if err != nil {
				assert.Equal(t, tc.errString, err.Error())
			} else {
				assert.Equal(t, tc.waveHeight, station.Present.WaveHeight)
				assert.Equal(t, tc.airTemp, station.Present.AirTemperature)
				assert.Equal(t, tc.waterTemp, station.Present.WaterTemperature)
				assert.Equal(t, tc.salinity, station.Present.Salinity)
				assert.Equal(t, tc.windSpeed, station.Present.WindSpeed)
				assert.Equal(t, tc.windDirection, station.Present.WindDirection)
				assert.Equal(t, tc.gust, station.Present.Gust)
				assert.Equal(t, tc.windSpeed10Min, station.Present.WindSpeed10Min)
				assert.Equal(t, tc.windSpeed20Min, station.Present.WindSpeed20Min)
			}
		})
	}

}
