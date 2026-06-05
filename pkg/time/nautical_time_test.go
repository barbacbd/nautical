package time

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetMinutes(t *testing.T) {
	nt := &NauticalTime{}

	// Valid minutes
	err := nt.SetMinutes(30)
	assert.NoError(t, err)
	assert.Equal(t, 30, nt.Minutes)

	// Zero minutes
	err = nt.SetMinutes(0)
	assert.NoError(t, err)
	assert.Equal(t, 0, nt.Minutes)

	// Max valid minutes
	err = nt.SetMinutes(59)
	assert.NoError(t, err)
	assert.Equal(t, 59, nt.Minutes)

	// Too large
	err = nt.SetMinutes(60)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "out of range")

	// Negative
	err = nt.SetMinutes(-1)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "must be positive")
}

func TestGetHours(t *testing.T) {
	tests := []struct {
		name     string
		nt       NauticalTime
		expected int
		wantErr  bool
	}{
		{
			name:     "24-hour format",
			nt:       NauticalTime{Hours: 14, Format: HOUR_24},
			expected: 14,
			wantErr:  false,
		},
		{
			name:     "12-hour AM",
			nt:       NauticalTime{Hours: 9, Format: HOUR_12, Midday: AM},
			expected: 9,
			wantErr:  false,
		},
		{
			name:     "12-hour PM",
			nt:       NauticalTime{Hours: 2, Format: HOUR_12, Midday: PM},
			expected: 14,
			wantErr:  false,
		},
		{
			name:     "Zero format defaults to 24-hour",
			nt:       NauticalTime{Hours: 10, Format: 0},
			expected: 10,
			wantErr:  false,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			hours, err := tc.nt.GetHours()
			if tc.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tc.expected, hours)
			}
		})
	}
}

func TestSetHours(t *testing.T) {
	nt := &NauticalTime{}

	// Valid hours
	err := nt.SetHours(14)
	assert.NoError(t, err)
	assert.Equal(t, 14, nt.Hours)

	// Zero hours
	err = nt.SetHours(0)
	assert.NoError(t, err)
	assert.Equal(t, 0, nt.Hours)

	// Max valid hours
	err = nt.SetHours(23)
	assert.NoError(t, err)
	assert.Equal(t, 23, nt.Hours)

	// Too large
	err = nt.SetHours(24)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "out of range")

	// Negative
	err = nt.SetHours(-1)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "must be positive")
}

func TestSetFormat(t *testing.T) {
	tests := []struct {
		name          string
		initial       NauticalTime
		format        int
		expectedHours int
		expectedMidday int
		wantErr       bool
	}{
		{
			name:          "24-hour to 12-hour AM",
			initial:       NauticalTime{Hours: 9, Format: HOUR_24},
			format:        HOUR_12,
			expectedHours: 9,
			expectedMidday: AM,
			wantErr:       false,
		},
		{
			name:          "24-hour to 12-hour PM",
			initial:       NauticalTime{Hours: 14, Format: HOUR_24},
			format:        HOUR_12,
			expectedHours: 2,
			expectedMidday: PM,
			wantErr:       false,
		},
		{
			name:          "12-hour PM to 24-hour",
			initial:       NauticalTime{Hours: 2, Format: HOUR_12, Midday: PM},
			format:        HOUR_24,
			expectedHours: 14,
			expectedMidday: 0,
			wantErr:       false,
		},
		{
			name:          "12-hour AM to 24-hour",
			initial:       NauticalTime{Hours: 9, Format: HOUR_12, Midday: AM},
			format:        HOUR_24,
			expectedHours: 9,
			expectedMidday: 0,
			wantErr:       false,
		},
		{
			name:    "Invalid format",
			initial: NauticalTime{Hours: 10, Format: HOUR_24},
			format:  99,
			wantErr: true,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			nt := tc.initial
			err := nt.SetFormat(tc.format)
			if tc.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tc.expectedHours, nt.Hours)
				assert.Equal(t, tc.expectedMidday, nt.Midday)
			}
		})
	}
}

func TestSetMidday(t *testing.T) {
	tests := []struct {
		name    string
		initial NauticalTime
		midday  int
		wantErr bool
		errMsg  string
	}{
		{
			name:    "Set to AM",
			initial: NauticalTime{Hours: 9, Format: HOUR_12, Midday: PM},
			midday:  AM,
			wantErr: false,
		},
		{
			name:    "Set to PM",
			initial: NauticalTime{Hours: 9, Format: HOUR_12, Midday: AM},
			midday:  PM,
			wantErr: false,
		},
		{
			name:    "Fail when 24-hour format",
			initial: NauticalTime{Hours: 14, Format: HOUR_24},
			midday:  PM,
			wantErr: true,
			errMsg:  "24 hour format",
		},
		{
			name:    "Fail with hours > 12 for AM",
			initial: NauticalTime{Hours: 13, Format: HOUR_12},
			midday:  AM,
			wantErr: true,
			errMsg:  "hours > 12",
		},
		{
			name:    "Invalid midday value",
			initial: NauticalTime{Hours: 9, Format: HOUR_12},
			midday:  99,
			wantErr: true,
			errMsg:  "failed to find AM/PM",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			nt := tc.initial
			err := nt.SetMidday(tc.midday)
			if tc.wantErr {
				assert.Error(t, err)
				if tc.errMsg != "" {
					assert.Contains(t, err.Error(), tc.errMsg)
				}
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tc.midday, nt.Midday)
			}
		})
	}
}

func TestString(t *testing.T) {
	tests := []struct {
		name     string
		nt       NauticalTime
		expected string
		wantErr  bool
	}{
		{
			name:     "24-hour format",
			nt:       NauticalTime{Hours: 14, Minutes: 30, Format: HOUR_24},
			expected: "14:30:00",
			wantErr:  false,
		},
		{
			name:     "12-hour AM",
			nt:       NauticalTime{Hours: 9, Minutes: 15, Format: HOUR_12, Midday: AM},
			expected: "09:15:00",
			wantErr:  false,
		},
		{
			name:     "12-hour PM",
			nt:       NauticalTime{Hours: 2, Minutes: 45, Format: HOUR_12, Midday: PM},
			expected: "14:45:00",
			wantErr:  false,
		},
		{
			name:     "Zero padding",
			nt:       NauticalTime{Hours: 5, Minutes: 5, Format: HOUR_24},
			expected: "05:05:00",
			wantErr:  false,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result, err := tc.nt.String()
			if tc.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tc.expected, result)
			}
		})
	}
}
