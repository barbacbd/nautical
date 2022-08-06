package buoy

import (
	"encoding/json"
	"github.com/barbacbd/nautical/pkg/time"
	"testing"

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

func TestSourceGetBuoyByStationID(t *testing.T) {
	tests := []struct {
		name          string
		source        Source
		searchStation string
		expectedErr   string
	}{{
		name: "Find Station in Source",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys: map[uint64]*Buoy{
				1234: &Buoy{Station: "ExampleBuoy"},
			},
		},
		searchStation: "ExampleBuoy",
	}, {
		name: "Find Station In Empty Source Buoys not init",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
		},
		searchStation: "ExampleBuoy",
		expectedErr:   "failed to find buoy with station: ExampleBuoy",
	}, {
		name: "Find Station In Empty Source",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys:       map[uint64]*Buoy{},
		},
		searchStation: "ExampleBuoy",
		expectedErr:   "failed to find buoy with station: ExampleBuoy",
	}, {
		name: "Find Station in Source No Match",
		source: Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys: map[uint64]*Buoy{
				1234: &Buoy{Station: "ExampleBuoy1"},
				2345: &Buoy{Station: "ExampleBuoy2"},
				3456: &Buoy{Station: "ExampleBuoy3"},
			},
		},
		searchStation: "ExampleBuoy",
		expectedErr:   "failed to find buoy with station: ExampleBuoy",
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {

			buoy, err := tc.source.GetBuoy(tc.searchStation)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.True(t, buoy != nil)
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

			err := tc.source.AddBuoy(tc.newBuoy)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, originalLen+1, len(tc.source.Buoys))
			}
		})
	}
}
