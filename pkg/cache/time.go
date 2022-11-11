package cache

import "time"

// ShouldUpdate will determine if the cache should be updated based on the
// time difference (provided) that is the min difference allowed before an
// update will occur.
func ShouldUpdate(originalTime time.Time, minMinutesDifference int) bool {
	currentTime := time.Now().UTC()
	diff := currentTime.Sub(originalTime)
	return diff.Minutes() < float64(minMinutesDifference)
}
