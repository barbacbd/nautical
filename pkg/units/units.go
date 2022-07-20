package units

import "fmt"

const (
	SECONDS int = 1
	MINUTES int = 2
	HOURS   int = 3
	DAYS    int = 4

	DEG_F int = 1
	DEG_C int = 2

	KNOTS int = 1
	MPS   int = 2
	MPH   int = 3
	KPH   int = 4
	FPS   int = 5

	CENTIMETERS    int = 1
	FEET           int = 2
	YARDS          int = 3
	METERS         int = 4
	KILOMETERS     int = 5
	MILES          int = 6
	NAUTICAL_MILES int = 7

	PA   int = 1
	TORR int = 2
	BARR int = 3
	ATM  int = 4
	AT   int = 5
	BA   int = 6
	PSI  int = 7
	HG   int = 8

	PSU int = 1
)

var (
	TimeUnitsName = map[int]string{
		SECONDS: "SECONDS",
		MINUTES: "MINUTES",
		HOURS:   "HOURS",
		DAYS:    "DAYS",
	}
	TimeUnitsLookup = map[int]float64{
		SECONDS: 1.0,
		MINUTES: 60.0,
		HOURS:   3600.0,
		DAYS:    86400.0,
	}

	TemperatureUnitsName = map[int]string{
		DEG_F: "DEG_F",
		DEG_C: "DEG_C",
	}

	SpeedUnitsName = map[int]string{
		KNOTS: "KNOTS",
		MPS:   "MPS",
		MPH:   "MPH",
		KPH:   "KPH",
		FPS:   "FPS",
	}

	SpeedUnitsLookup = map[int]float64{
		MPS:   1.0,
		KNOTS: 1.94384,
		MPH:   2.23694,
		KPH:   3.6,
		FPS:   3.28084,
	}

	DistanceUnitsName = map[int]string{
		CENTIMETERS:    "CENTIMETERS",
		FEET:           "FEET",
		YARDS:          "YARDS",
		METERS:         "METERS",
		KILOMETERS:     "KILOMETERS",
		MILES:          "MILES",
		NAUTICAL_MILES: "NAUTICAL_MILES",
	}

	DistanceUnitsLookup = map[int]float64{
		CENTIMETERS:    1.0,
		FEET:           30.48,
		YARDS:          91.44,
		METERS:         100.0,
		KILOMETERS:     100000.0,
		MILES:          160934.708789,
		NAUTICAL_MILES: 185198.903622,
	}

	PressureUnitsName = map[int]string{
		PA:   "PA",
		TORR: "TORR",
		BARR: "BARR",
		ATM:  "ATM",
		AT:   "AT",
		BA:   "BA",
		PSI:  "PSI",
		HG:   "HG",
	}

	PressureUnitsLookup = map[int]float64{
		PA:   1.0,
		TORR: 0.0075,
		BARR: 0.00010,
		ATM:  0.00009869,
		AT:   0.0000102,
		BA:   10,
		PSI:  0.000145,
		HG:   0.0075,
	}

	SalinityUnitsName = map[int]string{
		PSU: "PSU",
	}
)

type EnumUnits struct {
	value int
	name  string
}

type TimeUnits EnumUnits
type TemperatureUnits EnumUnits
type SpeedUnits EnumUnits
type DistanceUnits EnumUnits
type PressureUnits EnumUnits
type SalinityUnits EnumUnits

// String - Returns the string name for the value store in the TimeUnits struct
func (t *TimeUnits) String() (string, error) {
	if val, ok := TimeUnitsName[t.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("TimeUnits no matching name for value: %d", t.value)
}

// String - Returns the string name for the value store in the TemperatureUnits struct
func (t *TemperatureUnits) String() (string, error) {
	if val, ok := TemperatureUnitsName[t.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("TemperatureUnits no matching name for value: %d", t.value)
}

// String - Returns the string name for the value store in the SpeedUnits struct
func (s *SpeedUnits) String() (string, error) {
	if val, ok := SpeedUnitsName[s.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("SpeedUnits no matching name for value: %d", s.value)
}

// String - Returns the string name for the value store in the DistanceUnits struct
func (d *DistanceUnits) String() (string, error) {
	if val, ok := DistanceUnitsName[d.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("DistanceUnits no matching name for value: %d", d.value)
}

// String - Returns the string name for the value store in the PressureUnits struct
func (p *PressureUnits) String() (string, error) {
	if val, ok := PressureUnitsName[p.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("PressureUnits no matching name for value: %d", p.value)
}

// String - Returns the string name for the value store in the SalinityUnits struct
func (s *SalinityUnits) String() (string, error) {
	if val, ok := SalinityUnitsName[s.value]; ok {
		return val, nil
	}
	return "", fmt.Errorf("SalinityUnits no matching name for value: %d", s.value)
}

// ConvertTime - Convert the value from units initUnits to the value equivalent
// when the units are set to finalUnits
func ConvertTime(value float64, initUnits int, finalUnits int) (float64, error) {
	if origFactor, ok := TimeUnitsLookup[initUnits]; ok {
		if newFactor, ok := TimeUnitsLookup[finalUnits]; ok {
			return value * origFactor / newFactor, nil
		}
		return 0, fmt.Errorf("ConvertTime no matching TimeUnits(finalUnits) for value: %d", finalUnits)
	}
	return 0, fmt.Errorf("ConvertTime no matching TimeUnits(initUnits) for value: %d", initUnits)
}

// ConvertTemperature - Convert the value from units initUnits to the value equivalent
// when the units are set to finalUnits
func ConvertTemperature(value float64, initUnits int, finalUnits int) (float64, error) {
	if _, ok := TemperatureUnitsName[initUnits]; ok {
		if _, ok := TemperatureUnitsName[finalUnits]; ok {
			if initUnits != finalUnits {
				if initUnits == DEG_F {
					return (value - 32) * 5.0 / 9.0, nil
				} else if initUnits == DEG_C {
					return (9.0 / 5.0 * value) + 32.0, nil
				}
			}
			return value, nil
		}
		return 0, fmt.Errorf("ConvertTemperature no matching TemperatureUnits(finalUnits) for value: %d", finalUnits)
	}
	return 0, fmt.Errorf("ConvertTemperature no matching TemperatureUnits(initUnits) for value: %d", initUnits)
}

// ConvertSpeed - Convert the value from units initUnits to the value equivalent
// when the units are set to finalUnits
func ConvertSpeed(value float64, initUnits int, finalUnits int) (float64, error) {
	if origFactor, ok := SpeedUnitsLookup[initUnits]; ok {
		if newFactor, ok := SpeedUnitsLookup[finalUnits]; ok {
			return value / origFactor * newFactor, nil
		}
		return 0, fmt.Errorf("ConvertSpeed no matching SpeedUnits(finalUnits) for value: %d", finalUnits)
	}
	return 0, fmt.Errorf("ConvertSpeed no matching SpeedUnits(initUnits) for value: %d", initUnits)
}

// ConvertDistance - Convert the value from units initUnits to the value equivalent
// when the units are set to finalUnits
func ConvertDistance(value float64, initUnits int, finalUnits int) (float64, error) {
	if origFactor, ok := DistanceUnitsLookup[initUnits]; ok {
		if newFactor, ok := DistanceUnitsLookup[finalUnits]; ok {
			return value * origFactor / newFactor, nil
		}
		return 0, fmt.Errorf("ConvertDistance no matching DistanceUnits(finalUnits) for value: %d", finalUnits)
	}
	return 0, fmt.Errorf("ConvertDistance no matching DistanceUnits(initUnits) for value: %d", initUnits)
}

// ConvertPressure - Convert the value from units initUnits to the value equivalent
// when the units are set to finalUnits
func ConvertPressure(value float64, initUnits int, finalUnits int) (float64, error) {
	if origFactor, ok := PressureUnitsLookup[initUnits]; ok {
		if newFactor, ok := PressureUnitsLookup[finalUnits]; ok {
			return value / origFactor * newFactor, nil
		}
		return 0, fmt.Errorf("ConvertPressure no matching PressureUnits(finalUnits) for value: %d", finalUnits)
	}
	return 0, fmt.Errorf("ConvertPressure no matching PressureUnits(initUnits) for value: %d", initUnits)
}
