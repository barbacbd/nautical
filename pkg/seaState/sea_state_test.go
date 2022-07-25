package seaState

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestTimeConversion(t *testing.T) {
	tests := []struct {
		name          string
		waveHeightMts float64
		expectedState int
	}{{
		name:          "Sea State 0",
		waveHeightMts: 0.0,
		expectedState: 0,
	}, {
		name:          "Sea State 0 Negative",
		waveHeightMts: -121312.0,
		expectedState: 0,
	}, {
		name:          "Sea State 1",
		waveHeightMts: 0.005,
		expectedState: 1,
	}, {
		name:          "Sea State 2",
		waveHeightMts: 0.49,
		expectedState: 2,
	}, {
		name:          "Sea State 3",
		waveHeightMts: 0.51,
		expectedState: 3,
	}, {
		name:          "Sea State 4",
		waveHeightMts: 2.0,
		expectedState: 4,
	}, {
		name:          "Sea State 5",
		waveHeightMts: 3.99,
		expectedState: 5,
	}, {
		name:          "Sea State 6",
		waveHeightMts: 4.001,
		expectedState: 6,
	}, {
		name:          "Sea State 7",
		waveHeightMts: 7.5,
		expectedState: 7,
	}, {
		name:          "Sea State 8",
		waveHeightMts: 12.0,
		expectedState: 8,
	}, {
		name:          "Sea State 9",
		waveHeightMts: 123123123.0,
		expectedState: 9,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			state := GetSeaState(tc.waveHeightMts)
			assert.Equal(t, tc.expectedState, state)
		})
	}

}
