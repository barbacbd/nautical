package buoy

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

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
			if err != nil {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.True(t, buoy != nil)
			}
		})
	}
}

func TestSourceTypeAsString(t *testing.T) {
	tests := []struct {
		name        string
		sourceType  int
		returnedStr string
		errStr      string
	}{{
		name:        "Good ALL",
		sourceType:  ALL,
		returnedStr: "IOOS Partners, International Partners, Marine METAR, NDBC Meteorological/Ocean, NERRS, NOS/CO-OPS, Ships, TAO, Tsunami",
	}, {
		name:        "Good INTERNATIONAL_PARTNERS",
		sourceType:  INTERNATIONAL_PARTNERS,
		returnedStr: "International Partners",
	}, {
		name:        "Good IOOS_PARTNERS",
		sourceType:  IOOS_PARTNERS,
		returnedStr: "IOOS Partners",
	}, {
		name:        "Good MARINE_METAR",
		sourceType:  MARINE_METAR,
		returnedStr: "Marine METAR",
	}, {
		name:        "Good NDBC_METEOROLOGICAL_OCEAN",
		sourceType:  NDBC_METEOROLOGICAL_OCEAN,
		returnedStr: "NDBC Meteorological/Ocean",
	}, {
		name:        "Good NERRS",
		sourceType:  NERRS,
		returnedStr: "NERRS",
	}, {
		name:        "Good NOS_CO_OPS",
		sourceType:  NOS_CO_OPS,
		returnedStr: "NOS/CO-OPS",
	}, {
		name:        "Good SHIPS",
		sourceType:  SHIPS,
		returnedStr: "Ships",
	}, {
		name:        "Good TAO",
		sourceType:  TAO,
		returnedStr: "TAO",
	}, {
		name:        "Good TSUNAMI",
		sourceType:  TSUNAMI,
		returnedStr: "Tsunami",
	}, {
		name:       "Bad Source Type",
		sourceType: -1,
		errStr:     "failed to find SourceType: -1",
	},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			retStr, err := SourceTypeAsString(tc.sourceType)
			if err != nil {
				assert.Equal(t, tc.errStr, err.Error())
			} else {
				assert.Equal(t, tc.returnedStr, retStr)
			}
		})
	}
}
