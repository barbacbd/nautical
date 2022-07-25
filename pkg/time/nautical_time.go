package time

import "fmt"

const (
	AM = 1
	PM = 2

	HOUR_12 = 12
	HOUR_24 = 24
)

type NauticalTime struct {
	// Format contains the string representation of the Time Format
	Format int `json:"timeFormat,omitempty" default:"24"`

	// Midday contains the string representation of the AM/PM value
	Midday int `json:"midday,omitempty" default:"0"`

	// Minutes is the number of minutes past the hour. Values are valid 0-59
	Minutes int `json:"minutes" default:"0"`

	// Hours is the hour of the day. times are assumed in 24 hour format unless
	// data from Midday or Format conflict with this information.
	// Values re valid 0-23
	Hours int `json:"hours" default:"0"`
}

// SetMinutes sets the current minutes of the NauticalTime struct
func (nt *NauticalTime) SetMinutes(minutes int) error {
	if minutes >= 60 {
		return fmt.Errorf("minutes is out of range (too large): %d", minutes)
	} else if minutes < 0 {
		return fmt.Errorf("minutes must be positive")
	}
	nt.Minutes = minutes
	return nil
}

// GetHours will get the current value in hours in a 24 hour time format.
func (nt *NauticalTime) GetHours() (int, error) {
	switch {
	case nt.Format == HOUR_24:
		return nt.Hours, nil
	case nt.Format == HOUR_12:
		if nt.Midday == PM {
			return nt.Hours + nt.Format, nil
		} else {
			return nt.Hours, nil
		}
	}
	return 0, fmt.Errorf("failed to find NauticalTime time format")
}

// SetHours sets the hours of the NauticalTime struct
func (nt *NauticalTime) SetHours(hours int) error {
	if hours >= 24 {
		return fmt.Errorf("hours is out of range (too large): %d", hours)
	} else if hours < 0 {
		return fmt.Errorf("hours must be positive")
	}
	nt.Hours = hours
	return nil
}

// SetFormat sets the current time format, 24 vs 12 hour time format. Based on the
// current value of the hours, a value >= 12 will set Midday to PM all other times
// are assumed AM.
func (nt *NauticalTime) SetFormat(format int) error {
	switch {
	case format == HOUR_12:
		if nt.Hours >= HOUR_12 {
			if err := nt.SetHours(nt.Hours - format); err != nil {
				return err
			}

			// Reassign the AM/PM value
			nt.Midday = PM
		} else {
			nt.Midday = AM
		}
	case format == HOUR_24:
		if nt.Midday == PM {
			if err := nt.SetHours(nt.Hours + HOUR_12); err != nil {
				return err
			}
		}
		nt.Midday = 0
	default:
		return fmt.Errorf("invalid time format: %d", format)
	}

	return nil
}

// SetMidday will set the AM/PM value and adjust the hours for the NauticalTime struct. The
// current format MUST be HOUR_12 for this function to complete.
func (nt *NauticalTime) SetMidday(midday int) error {
	if nt.Format != HOUR_12 {
		return fmt.Errorf("failed to set AM/PM while in 24 hour format")
	}

	switch {
	case midday == AM:
		if nt.Hours > 12 {
			return fmt.Errorf("failed to set midday to AM while hours > 12")
		} else {
			nt.Midday = AM
		}
	case midday == PM:
		if nt.Hours > 12 {
			if err := nt.SetHours(nt.Hours - 12); err != nil {
				return err
			}
		}
		nt.Midday = PM
	default:
		return fmt.Errorf("failed to find AM/PM value: %d", midday)
	}

	return nil
}

// String formats a string representation of the NauticalTime struct. The
// following format is returned "00:00:00" where the seconds will always be 0.
func (nt *NauticalTime) String() (string, error) {
	hours, err := nt.GetHours()
	if err != nil {
		return "", err
	}

	return fmt.Sprintf("%02d:%02d:00", hours, nt.Minutes), nil
}
