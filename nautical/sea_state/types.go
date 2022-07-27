package sea_state

import (
	"math"
)

var (
	// SeaStates is a map/dictionary that maps the sea state (0-9) to the maximum
	// wave height (meters) that is valid for that particular sea state
	SeaStates = map[int]float64{
		0: 0.0,
		1: 0.1,
		2: 0.5,
		3: 1.25,
		4: 2.5,
		5: 4.0,
		6: 6.0,
		7: 9.0,
		8: 14.0,
		9: math.Inf(1),
	}
)

// GetSeaState will return the sea state level based on the provided
// wave height (assumes meters)
func GetSeaState(waveHeight float64) int {
	seaState := 9

	// iteration of maps is not thread safe as the order is not the creation order.
	// We cannot rely on the values returning correctly by returning from inside
	// of the loop.
	for key, value := range SeaStates {
		if waveHeight <= value && key < seaState {
			seaState = key
		}
	}

	return seaState
}
