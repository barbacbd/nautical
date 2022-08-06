package time

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestConvertNOAATime(t *testing.T) {
	tests := []struct {
		name        string
		timeStr     string
		nt          NauticalTime
		expectedErr string
	}{{
		name:    "Correct Conversion",
		timeStr: "10:30&nbsp;am",
		nt: NauticalTime{
			Minutes: 30,
			Hours:   10,
			Midday:  AM,
			Format:  HOUR_12,
		},
	}, {
		name:    "Correct Conversion Exclude Minutes",
		timeStr: "10:30:123&nbsp;am",
		nt: NauticalTime{
			Minutes: 30,
			Hours:   10,
			Midday:  AM,
			Format:  HOUR_12,
		},
	}, {
		name:    "Correct Conversion Long String No Midday",
		timeStr: "10:30:12",
		nt: NauticalTime{
			Minutes: 30,
			Hours:   10,
			Format:  HOUR_24,
		},
	}, {
		name:    "Correct Conversion Long String No Midday Set To 24 Hour",
		timeStr: "13:45:00",
		nt: NauticalTime{
			Minutes: 45,
			Hours:   13,
			Format:  HOUR_24,
		},
	}, {
		name:    "Correct Conversion Short String No Midday Set To 24 Hour",
		timeStr: "13:45",
		nt: NauticalTime{
			Minutes: 45,
			Hours:   13,
			Format:  HOUR_24,
		},
	}, {
		name:    "Correct Conversion Long String No Midday Set To 12 Hour",
		timeStr: "01:45pm",
		nt: NauticalTime{
			Minutes: 45,
			Hours:   1,
			Format:  HOUR_12,
			Midday:  PM,
		},
	}, {
		name:        "Incorrect Time Format",
		timeStr:     "13:gf45",
		expectedErr: "strconv.Atoi: parsing \"gf45\": invalid syntax",
	}, {
		name:        "Incorrect Time Format Bad Midday",
		timeStr:     "10:30&nbsp;lm",
		expectedErr: "failed to find midday value: lm",
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			nt, err := ConvertNOAATime(tc.timeStr)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.nt.Hours, nt.Hours)
				assert.Equal(t, tc.nt.Minutes, nt.Minutes)
				assert.Equal(t, tc.nt.Midday, nt.Midday)
				assert.Equal(t, tc.nt.Format, nt.Format)
			}
		})
	}
}
