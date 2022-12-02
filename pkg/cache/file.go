package cache

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"os/user"
	"runtime"
	"strings"
	"time"

	noaa "github.com/barbacbd/nautical/v1/pkg/noaa/buoy"
)

const (
	CacheFile  = "nautical_cache.json"
	TimeLayout = "2006-01-02_15-04-05"
)

// NauticalCache contains the Buoys, Sources, and Time data for a cached instance
type NauticalCache struct {
	// Buoys is the list of all buoys that are to be cached
	Buoys []noaa.Buoy `json:"buoys,omitempty"`

	// Sources is the list of all sources that are to be cached
	Sources []noaa.Source `json:"sources,omitempty"`

	// Time that the cache was created
	Time string `json:"time,omitempty"`
}

// NauticalCacheData is a wrapper for the NauticalCache struct that includes the Filename
// where the data is stored
type NauticalCacheData struct {
	// Full Filename (including path) to the cached data
	Filename string

	// CachedData is structure holding all cached data
	CachedData *NauticalCache
}

func (cache *NauticalCacheData) New() error {
	cacheDir, err := FindCacheDir()
	if err != nil {
		return err
	}

	if _, err = os.Stat(cacheDir); err != nil {
		if os.IsNotExist(err) {
			if err = os.Mkdir(cacheDir, os.ModePerm); err != nil {
				return err
			}
		} else {
			return err
		}
	}

	cache.Filename, err = FindCacheFile()
	if err != nil {
		return err
	}
	cache.CachedData = &NauticalCache{}

	return nil
}

// FindCacheDir will find the nautical cache directory. First the environment variable
// NAUTICAL_CACHE_DIR is searched for. If this environment variable is not found, then
// the operating system is searched and directory is returned according to the system.
func FindCacheDir() (string, error) {
	if val, ok := os.LookupEnv("NAUTICAL_CACHE_DIR"); ok {
		return val, nil
	}

	currentUser, err := user.Current()
	if err != nil {
		return "", err
	}

	system := runtime.GOOS
	switch system {
	case "windows":
		return fmt.Sprintf("C:\\Users\\%s\\AppData\\Local\\nautical", currentUser.Username), nil
	case "darwin":
		return fmt.Sprintf("/home/%s/Library/Application Support/nautical", currentUser.Username), nil
	case "linux":
		return fmt.Sprintf("/home/%s/.local/share/nautical", currentUser.Username), nil
	}
	return "", fmt.Errorf("operating system not found")
}

// FindCacheFile find the full path to the cache file.
func FindCacheFile() (string, error) {
	dir, err := FindCacheDir()
	if err != nil {
		return "", err
	}
	return strings.Join([]string{dir, CacheFile}, "/"), nil
}

// CopyCurrentCache copies the current cached data to a new file where the
// extra data is appended to the original cached filename
func (cache *NauticalCacheData) CopyCurrentCache(extra_data string) error {
	if _, err := os.Stat(cache.Filename); err != nil {
		return err
	}

	newFilename := strings.Replace(cache.Filename, ".json", fmt.Sprintf("%s.json", extra_data), -1)

	fin, err := os.Open(cache.Filename)
	if err != nil {
		return err
	}
	defer fin.Close()

	fout, err := os.Create(newFilename)
	if err != nil {
		return err
	}
	defer fout.Close()

	_, err = io.Copy(fout, fin)
	if err != nil {
		return err
	}

	// reset the filename
	cache.Filename = newFilename
	return nil
}

// CopyCurrentCacheWithTimestamp Copies the data of the original file and renames the file
// with a timestamp.
func (cache *NauticalCacheData) CopyCurrentCacheWithTimestamp() error {
	return cache.CopyCurrentCache(fmt.Sprintf(time.Now().UTC().Format(TimeLayout)))
}

// Load will load the data from a file into the NauticalCacheData
func Load(filename string) (*NauticalCacheData, error) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	cache := NauticalCache{}
	if err = json.Unmarshal(content, &cache); err != nil {
		return nil, err
	}

	cacheData := NauticalCacheData{Filename: filename, CachedData: &cache}
	return &cacheData, nil
}

// Dump outputs the nautical cache data to the filename specified in the cache struct
func (cache *NauticalCacheData) Dump() error {
	content, err := json.Marshal(cache.CachedData)
	if err != nil {
		return err
	}
	if err = ioutil.WriteFile(cache.Filename, content, 0666); err != nil {
		return err
	}
	return nil
}

// ShouldUpdate will determine if an update should occur based on the time
// stored in the CacheData
func (cache *NauticalCacheData) ShouldUpdate(minMinutesDifference int) bool {
	timeData, err := time.Parse(TimeLayout, cache.CachedData.Time)
	if err != nil {
		return false
	}

	return ShouldUpdate(timeData, minMinutesDifference)
}
