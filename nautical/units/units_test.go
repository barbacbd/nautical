package units

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestTimeConversion(t *testing.T) {
	tests := []struct {
		name          string
		initValue     float64
		initUnits     int
		expectedValue float64
		finalUnits    int
		expectedErr   string
	}{{
		name:          "Valid Seconds to Minutes",
		initValue:     100,
		initUnits:     SECONDS,
		expectedValue: 1.6666666666666667,
		finalUnits:    MINUTES,
	}, {
		name:          "Valid Seconds to Hours",
		initValue:     100,
		initUnits:     SECONDS,
		expectedValue: 0.027777777777777776,
		finalUnits:    HOURS,
	}, {
		name:          "Valid Seconds to Days",
		initValue:     100,
		initUnits:     SECONDS,
		expectedValue: 0.0011574074074074073,
		finalUnits:    DAYS,
	}, {
		name:          "Valid Minutes to Hours",
		initValue:     100,
		initUnits:     MINUTES,
		expectedValue: 1.6666666666666667,
		finalUnits:    HOURS,
	}, {
		name:          "Valid Minutes to Days",
		initValue:     100,
		initUnits:     MINUTES,
		expectedValue: 0.06944444444444445,
		finalUnits:    DAYS,
	}, {
		name:          "Valid Hours to Days",
		initValue:     100,
		initUnits:     HOURS,
		expectedValue: 4.166666666666667,
		finalUnits:    DAYS,
	}, {
		name:          "Invalid initial units",
		initValue:     100,
		initUnits:     100,
		expectedValue: 1.6,
		finalUnits:    MINUTES,
		expectedErr:   fmt.Sprintf("ConvertTime no matching TimeUnits(initUnits) for value: %d", 100),
	}, {
		name:          "Invalid final units",
		initValue:     100,
		initUnits:     SECONDS,
		expectedValue: 1.6,
		finalUnits:    100,
		expectedErr:   fmt.Sprintf("ConvertTime no matching TimeUnits(finalUnits) for value: %d", 100),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			finalValue, err := ConvertTime(tc.initValue, tc.initUnits, tc.finalUnits)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedValue, finalValue)
			}
		})
	}

}

func TestSpeedConversion(t *testing.T) {
	tests := []struct {
		name          string
		initValue     float64
		initUnits     int
		expectedValue float64
		finalUnits    int
		expectedErr   string
	}{{
		name:          "Valid MPS to Knots",
		initValue:     11.2,
		initUnits:     MPS,
		expectedValue: 21.771008,
		finalUnits:    KNOTS,
	}, {
		name:          "Valid MPS to MPH",
		initValue:     11.2,
		initUnits:     MPS,
		expectedValue: 25.053728,
		finalUnits:    MPH,
	}, {
		name:          "Valid MPS to KPH",
		initValue:     11.2,
		initUnits:     MPS,
		expectedValue: 40.32,
		finalUnits:    KPH,
	}, {
		name:          "Valid MPS to FPS",
		initValue:     11.2,
		initUnits:     MPS,
		expectedValue: 36.745408,
		finalUnits:    FPS,
	}, {
		name:          "Valid Knots to MPH",
		initValue:     17.4,
		initUnits:     KNOTS,
		expectedValue: 20.023641863527864,
		finalUnits:    MPH,
	}, {
		name:          "Valid Knots to KPH",
		initValue:     17.4,
		initUnits:     KNOTS,
		expectedValue: 32.22487447526545,
		finalUnits:    KPH,
	}, {
		name:          "Valid Knots to FPS",
		initValue:     17.4,
		initUnits:     KNOTS,
		expectedValue: 29.36796032595275,
		finalUnits:    FPS,
	}, {
		name:          "Valid MPH to KPH",
		initValue:     6.21,
		initUnits:     MPH,
		expectedValue: 9.994009673929563,
		finalUnits:    KPH,
	}, {
		name:          "Valid MPH to FPS",
		initValue:     6.21,
		initUnits:     MPH,
		expectedValue: 9.107985194059742,
		finalUnits:    FPS,
	}, {
		name:          "Valid KPH to FPS",
		initValue:     3.5,
		initUnits:     KPH,
		expectedValue: 3.1897055555555553,
		finalUnits:    FPS,
	}, {
		name:          "Invalid initial units",
		initValue:     100,
		initUnits:     100,
		expectedValue: 1.6,
		finalUnits:    KPH,
		expectedErr:   fmt.Sprintf("ConvertSpeed no matching SpeedUnits(initUnits) for value: %d", 100),
	}, {
		name:          "Invalid final units",
		initValue:     100,
		initUnits:     MPH,
		expectedValue: 1.6,
		finalUnits:    100,
		expectedErr:   fmt.Sprintf("ConvertSpeed no matching SpeedUnits(finalUnits) for value: %d", 100),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			finalValue, err := ConvertSpeed(tc.initValue, tc.initUnits, tc.finalUnits)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedValue, finalValue)
			}
		})
	}

}

func TestDistanceConversion(t *testing.T) {
	tests := []struct {
		name          string
		initValue     float64
		initUnits     int
		expectedValue float64
		finalUnits    int
		expectedErr   string
	}{{
		name:          "Valid CENTIMETERS to FEET",
		initValue:     11.2,
		initUnits:     CENTIMETERS,
		expectedValue: 0.3674540682414698,
		finalUnits:    FEET,
	}, {
		name:          "Valid CENTIMETERS to YARDS",
		initValue:     11.2,
		initUnits:     CENTIMETERS,
		expectedValue: 0.12248468941382326,
		finalUnits:    YARDS,
	}, {
		name:          "Valid CENTIMETERS to METERS",
		initValue:     11.2,
		initUnits:     CENTIMETERS,
		expectedValue: 0.11199999999999999,
		finalUnits:    METERS,
	}, {
		name:          "Valid CENTIMETERS to KILOMETERS",
		initValue:     11.2,
		initUnits:     CENTIMETERS,
		expectedValue: 0.000112,
		finalUnits:    KILOMETERS,
	}, {
		name:          "Valid CENTIMETERS to MILES",
		initValue:     170000,
		initUnits:     CENTIMETERS,
		expectedValue: 1.0563289999976664,
		finalUnits:    MILES,
	}, {
		name:          "Valid CENTIMETERS to NAUTICAL MILES",
		initValue:     170000,
		initUnits:     CENTIMETERS,
		expectedValue: 0.9179320000024314,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Valid FEET to YARDS",
		initValue:     11.2,
		initUnits:     FEET,
		expectedValue: 3.733333333333333,
		finalUnits:    YARDS,
	}, {
		name:          "Valid FEET to METERS",
		initValue:     11.2,
		initUnits:     FEET,
		expectedValue: 3.41376,
		finalUnits:    METERS,
	}, {
		name:          "Valid FEET to KILOMETERS",
		initValue:     11.2,
		initUnits:     FEET,
		expectedValue: 0.0034137599999999996,
		finalUnits:    KILOMETERS,
	}, {
		name:          "Valid FEET to MILES",
		initValue:     17.4,
		initUnits:     FEET,
		expectedValue: 0.003295448222392719,
		finalUnits:    MILES,
	}, {
		name:          "Valid FEET to NAUTICAL MILES",
		initValue:     17.4,
		initUnits:     FEET,
		expectedValue: 0.002863688659207585,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Valid YARDS to METERS",
		initValue:     11.2,
		initUnits:     YARDS,
		expectedValue: 10.24128,
		finalUnits:    METERS,
	}, {
		name:          "Valid YARDS to KILOMETERS",
		initValue:     11.2,
		initUnits:     YARDS,
		expectedValue: 0.010241279999999998,
		finalUnits:    KILOMETERS,
	}, {
		name:          "Valid YARDS to MILES",
		initValue:     17.4,
		initUnits:     YARDS,
		expectedValue: 0.009886344667178157,
		finalUnits:    MILES,
	}, {
		name:          "Valid YARDS to NAUTICAL MILES",
		initValue:     17.4,
		initUnits:     YARDS,
		expectedValue: 0.008591065977622754,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Valid METERS to KILOMETERS",
		initValue:     11.2,
		initUnits:     METERS,
		expectedValue: 0.0112,
		finalUnits:    KILOMETERS,
	}, {
		name:          "Valid METERS to MILES",
		initValue:     17.4,
		initUnits:     METERS,
		expectedValue: 0.010811837999976112,
		finalUnits:    MILES,
	}, {
		name:          "Valid METERS to NAUTICAL MILES",
		initValue:     17.4,
		initUnits:     METERS,
		expectedValue: 0.009395304000024885,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Valid KILOMETERS to MILES",
		initValue:     17.4,
		initUnits:     KILOMETERS,
		expectedValue: 10.811837999976111,
		finalUnits:    MILES,
	}, {
		name:          "Valid KILOMETERS to NAUTICAL MILES",
		initValue:     17.4,
		initUnits:     KILOMETERS,
		expectedValue: 9.395304000024884,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Valid MILES to NAUTICAL MILES",
		initValue:     17.4,
		initUnits:     MILES,
		expectedValue: 15.120305132281318,
		finalUnits:    NAUTICAL_MILES,
	}, {
		name:          "Invalid initial units",
		initValue:     100,
		initUnits:     100,
		expectedValue: 1.6,
		finalUnits:    NAUTICAL_MILES,
		expectedErr:   fmt.Sprintf("ConvertDistance no matching DistanceUnits(initUnits) for value: %d", 100),
	}, {
		name:          "Invalid final units",
		initValue:     100,
		initUnits:     NAUTICAL_MILES,
		expectedValue: 1.6,
		finalUnits:    100,
		expectedErr:   fmt.Sprintf("ConvertDistance no matching DistanceUnits(finalUnits) for value: %d", 100),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			finalValue, err := ConvertDistance(tc.initValue, tc.initUnits, tc.finalUnits)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedValue, finalValue)
			}
		})
	}

}

func TestPressureConversion(t *testing.T) {
	tests := []struct {
		name          string
		initValue     float64
		initUnits     int
		expectedValue float64
		finalUnits    int
		expectedErr   string
	}{{
		name:          "Valid PA to TORR",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.08399999999999999,
		finalUnits:    TORR,
	}, {
		name:          "Valid PA to BARR",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.00112,
		finalUnits:    BARR,
	}, {
		name:          "Valid PA to ATM",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.001105328,
		finalUnits:    ATM,
	}, {
		name:          "Valid PA to AT",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.00011424,
		finalUnits:    AT,
	}, {
		name:          "Valid PA to BA",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 112,
		finalUnits:    BA,
	}, {
		name:          "Valid PA to PSI",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.001624,
		finalUnits:    PSI,
	}, {
		name:          "Valid PA to HG",
		initValue:     11.2,
		initUnits:     PA,
		expectedValue: 0.08399999999999999,
		finalUnits:    HG,
	}, {
		name:          "Valid TORR to BARR",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 0.14933333333333335,
		finalUnits:    BARR,
	}, {
		name:          "Valid TORR to ATM",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 0.14737706666666667,
		finalUnits:    ATM,
	}, {
		name:          "Valid TORR to AT",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 0.015232,
		finalUnits:    AT,
	}, {
		name:          "Valid TORR to BA",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 14933.333333333332,
		finalUnits:    BA,
	}, {
		name:          "Valid TORR to PSI",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 0.21653333333333333,
		finalUnits:    PSI,
	}, {
		name:          "Valid TORR to HG",
		initValue:     11.2,
		initUnits:     TORR,
		expectedValue: 11.2,
		finalUnits:    HG,
	}, {
		name:          "Valid BARR to ATM",
		initValue:     11.2,
		initUnits:     BARR,
		expectedValue: 11.053279999999999,
		finalUnits:    ATM,
	}, {
		name:          "Valid BARR to AT",
		initValue:     11.2,
		initUnits:     BARR,
		expectedValue: 1.1423999999999999,
		finalUnits:    AT,
	}, {
		name:          "Valid BARR to BA",
		initValue:     .112,
		initUnits:     BARR,
		expectedValue: 11200,
		finalUnits:    BA,
	}, {
		name:          "Valid BARR to PSI",
		initValue:     11.2,
		initUnits:     BARR,
		expectedValue: 16.24,
		finalUnits:    PSI,
	}, {
		name:          "Valid BARR to HG",
		initValue:     11.2,
		initUnits:     BARR,
		expectedValue: 839.9999999999999,
		finalUnits:    HG,
	}, {
		name:          "Valid ATM to AT",
		initValue:     11.2,
		initUnits:     ATM,
		expectedValue: 1.1575640895734116,
		finalUnits:    AT,
	}, {
		name:          "Valid ATM to BA",
		initValue:     .112,
		initUnits:     ATM,
		expectedValue: 11348.66754483737,
		finalUnits:    BA,
	}, {
		name:          "Valid ATM to PSI",
		initValue:     11.2,
		initUnits:     ATM,
		expectedValue: 16.455567940014184,
		finalUnits:    PSI,
	}, {
		name:          "Valid ATM to HG",
		initValue:     11.2,
		initUnits:     ATM,
		expectedValue: 851.1500658628026,
		finalUnits:    HG,
	}, {
		name:          "Valid AT to BA",
		initValue:     .112,
		initUnits:     AT,
		expectedValue: 109803.92156862744,
		finalUnits:    BA,
	}, {
		name:          "Valid AT to PSI",
		initValue:     11.2,
		initUnits:     AT,
		expectedValue: 159.2156862745098,
		finalUnits:    PSI,
	}, {
		name:          "Valid AT to HG",
		initValue:     11.2,
		initUnits:     AT,
		expectedValue: 8235.294117647058,
		finalUnits:    HG,
	}, {
		name:          "Valid BA to PSI",
		initValue:     11.2,
		initUnits:     BA,
		expectedValue: 0.0001624,
		finalUnits:    PSI,
	}, {
		name:          "Valid BA to HG",
		initValue:     11.2,
		initUnits:     BA,
		expectedValue: 0.0084,
		finalUnits:    HG,
	}, {
		name:          "Valid PSI to HG",
		initValue:     11.2,
		initUnits:     PSI,
		expectedValue: 579.3103448275862,
		finalUnits:    HG,
	}, {
		name:          "Invalid initial units",
		initValue:     100,
		initUnits:     100,
		expectedValue: 1.6,
		finalUnits:    PA,
		expectedErr:   fmt.Sprintf("ConvertPressure no matching PressureUnits(initUnits) for value: %d", 100),
	}, {
		name:          "Invalid final units",
		initValue:     100,
		initUnits:     PA,
		expectedValue: 1.6,
		finalUnits:    100,
		expectedErr:   fmt.Sprintf("ConvertPressure no matching PressureUnits(finalUnits) for value: %d", 100),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			finalValue, err := ConvertPressure(tc.initValue, tc.initUnits, tc.finalUnits)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedValue, finalValue)
			}
		})
	}
}

func TestTempConversion(t *testing.T) {
	tests := []struct {
		name          string
		initValue     float64
		initUnits     int
		expectedValue float64
		finalUnits    int
		expectedErr   string
	}{{
		name:          "Valid DEG F to DEG C",
		initValue:     89.34,
		initUnits:     DEG_F,
		expectedValue: 31.85555555555556,
		finalUnits:    DEG_C,
	}, {
		name:          "Valid DEG C to DEG F",
		initValue:     35.23,
		initUnits:     DEG_C,
		expectedValue: 95.41399999999999,
		finalUnits:    DEG_F,
	}, {
		name:          "Invalid initial units",
		initValue:     100,
		initUnits:     100,
		expectedValue: 1.6,
		finalUnits:    DEG_F,
		expectedErr:   fmt.Sprintf("ConvertTemperature no matching TemperatureUnits(initUnits) for value: %d", 100),
	}, {
		name:          "Invalid final units",
		initValue:     100,
		initUnits:     DEG_F,
		expectedValue: 1.6,
		finalUnits:    100,
		expectedErr:   fmt.Sprintf("ConvertTemperature no matching TemperatureUnits(finalUnits) for value: %d", 100),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			finalValue, err := ConvertTemperature(tc.initValue, tc.initUnits, tc.finalUnits)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedValue, finalValue)
			}
		})
	}

}
