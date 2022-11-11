package cache

import (
	"github.com/stretchr/testify/assert"
	"os"
	"testing"
	"time"

	noaa "github.com/barbacbd/nautical/pkg/noaa/buoy"
	nt "github.com/barbacbd/nautical/pkg/time"
)

const (
	CacheTestDir = "nautical_cache_tests"
)

func Setup(minutesOffset int) (*NauticalCacheData, error) {
	os.Setenv("NAUTICAL_CACHE_DIR", CacheTestDir)

	cacheData := NauticalCacheData{}
	if err := cacheData.New(); err != nil {
		return nil, err
	}

	cacheData.CachedData.Sources = CreateSources()
	cacheData.CachedData.Buoys = CreateBuoys()
	cacheData.CachedData.Time = time.Now().UTC().Add(-(time.Minute * time.Duration(minutesOffset))).Format(TimeLayout)
	return &cacheData, nil
}

func TearDown() {
	os.RemoveAll(CacheTestDir)
}

func CreateBuoys() []noaa.Buoy {
	return []noaa.Buoy{
		noaa.Buoy{
			Station: "FakeStation",
			Present: &noaa.BuoyData{
				Time:  &nt.NauticalTime{Minutes: 30, Hours: 8, Format: nt.HOUR_24},
				Year:  2000,
				Month: 5,
				Day:   14,
			},
		},
		noaa.Buoy{
			Station: "FakeStation2",
			Present: &noaa.BuoyData{
				Time:  &nt.NauticalTime{Minutes: 30, Hours: 9, Format: nt.HOUR_24},
				Year:  2000,
				Month: 5,
				Day:   16,
			},
		},
		noaa.Buoy{
			Station: "FakeStation3",
			Present: &noaa.BuoyData{
				Time:  &nt.NauticalTime{Minutes: 30, Hours: 10, Format: nt.HOUR_24},
				Year:  2000,
				Month: 5,
				Day:   15,
			},
		},
	}
}

func CreateSources() []noaa.Source {
	sources := []noaa.Source{
		noaa.Source{
			Name:        "Sample Source",
			Description: "Sample Source",
			Buoys: map[uint64]*noaa.Buoy{
				1234: &noaa.Buoy{Station: "FakeStation"},
				1235: &noaa.Buoy{Station: "FakeStation2"},
				1236: &noaa.Buoy{Station: "FakeStation3"},
			},
		},
	}

	return sources
}

func TestNauticalCache(t *testing.T) {
	nauticalCache, err := Setup(30)
	if err != nil {
		TearDown()
		t.Fail()
	}

	if err := nauticalCache.Dump(); err != nil {
		TearDown()
		t.Fail()
	}

	newNauticalCache, err := Load(nauticalCache.Filename)
	if err != nil {
		TearDown()
		t.Fail()
	}

	if len(newNauticalCache.CachedData.Sources) != len(nauticalCache.CachedData.Sources) {
		TearDown()
		t.Fail()
	}

	if len(newNauticalCache.CachedData.Buoys) != len(nauticalCache.CachedData.Buoys) {
		TearDown()
		t.Fail()
	}

	if newNauticalCache.CachedData.Time != nauticalCache.CachedData.Time {
		TearDown()
		t.Fail()
	}

	TearDown()
}

func TestNauticalCacheCopy(t *testing.T) {
	nauticalCache, err := Setup(30)
	if err != nil {
		TearDown()
		t.Fail()
	}

	if err := nauticalCache.Dump(); err != nil {
		TearDown()
		t.Fail()
	}

	originalFile := nauticalCache.Filename
	if err := nauticalCache.CopyCurrentCache("test_data"); err != nil {
		TearDown()
		t.Fail()
	}

	if originalFile == nauticalCache.Filename {
		TearDown()
		t.Fail()
	}

	newNauticalCache, err := Load(nauticalCache.Filename)
	if err != nil {
		TearDown()
		t.Fail()
	}

	if len(newNauticalCache.CachedData.Sources) != len(nauticalCache.CachedData.Sources) {
		TearDown()
		t.Fail()
	}

	if len(newNauticalCache.CachedData.Buoys) != len(nauticalCache.CachedData.Buoys) {
		TearDown()
		t.Fail()
	}

	if newNauticalCache.CachedData.Time != nauticalCache.CachedData.Time {
		TearDown()
		t.Fail()
	}

	TearDown()
}

func TestShouldUpdate(t *testing.T) {
	tests := []struct {
		name     string
		timeDiff int
		update   bool
	}{{
		name:     "test should update",
		timeDiff: 45,
		update:   true,
	}, {
		name:     "test should not update",
		timeDiff: 20,
		update:   false,
	},
	}

	// The time here should be noted so that it is valid for the tests above
	nauticalCache, err := Setup(30)
	if err != nil {
		TearDown()
		t.Fail()
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			shouldUpdate := nauticalCache.ShouldUpdate(tc.timeDiff)
			assert.Equal(t, tc.update, shouldUpdate)
		})
	}

	TearDown()
}
