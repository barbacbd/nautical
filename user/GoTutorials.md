# Nautical GO Tutorials

The document contains the tutorials/examples for the GO package. 
<br>
<br>
**Note**: _If you are familiar with the python package, please be advised that the go package is structured differently because of the required imports_.
<br>
<br>
# Table Of Contents

   * [Buoys](#buoys)
   * [Sources](#sources)
   * [Location](#location)
      * [In Area](#in-area)
      * [In Range](#in-range)
   * [Cache](#cache)
      * [Dump Data To File](#dump-data-to-file)
      * [Load Data From File](#load-data-from-file)
      * [Copying File Contents](#copying-file-contents)

# Buoys

The following section provides examples in the [buoy package](https://github.com/barbacbd/nautical/blob/master/pkg/noaa/buoy).

If you know the ID of the buoy station you may use `CreateBuoy` as a shortcut to create a buoy struct.

<pre><code class="language-go">
buoy, err := CreateBuoy("44099")
if err != nil {
    // error occurred
} else if buoy.Valid {
    // Buoy contains valid data
}
</code></pre>

The result will be a buoy filled with all of the data that was pulled online. The user _should_ *always*
check the validity of the buoy after the function call(s) to ensure that the data can be trusted.


If the user already has a buoy struct and wants to get the most up-to-date information, use te `FillBuoy`
function.

<pre><code class="language-go">
// Buoy was created previously

err := buoy.FillBuoy()
if err != nil {
    // error occurred
}
</code></pre>

# Sources

The following section provides examples in the [buoy package](https://github.com/barbacbd/nautical/blob/master/pkg/noaa/buoy).

NOAA provides a KML document containing all sources and the buoys that are grouped together by that
source. The document also provides minimal information about buoys in the event that they cannot
be retrieved online.
<br>
<br>
**Note**: The `TAO` and `Tsunami` sources are not available in any regard.
<br>
<br>
If the user wishes to make a record for `ALL` sources and their buoys use the default settings when
calling the `GetBuoySources`.

<pre><code class="language-go">
sources, err := GetBuoySources()
if err != nil {
    // error occurred
} else {
    for _, source := range sources {
        // do something with each source
    }
}
</code></pre>

# Location

The following sections are provided as examples in the [location package](https://github.com/barbacbd/nautical/blob/master/pkg/location/).

## In area

The user is provided with convenience functions for `location Points`. If the user wants to determine if a
point (possibly the location of a buoy) is contained within a specific area they can use the `in_area_ function.

<pre><code class="language-go">
geometry := []Point{
    Point{}, Point{}, Point{}, Point{}
}

pointToCheck := Point{
    Latitude: latitude, 
    Longitude: longitude
}

inArea, err := InArea(geometry, pointToCheck)
if err != nil {
    return err
}

if inArea {
    // do something 
} else {
    // do something else
}
</code></pre>

Similarly, the user can pass the location of a buoy to determine if it is in the area.

<pre><code class="language-go">
geometry := []Point{
    Point{}, Point{}, Point{}, Point{}
}
buoy := Buoy{
    Station: "test", 
    Description: "this is a test", 
    Location: Point{
        Latitude:latitude, 
        Longitude: longitude
    }
}

inArea, err := InArea(geometry, buoy.Location)
if err != nil {
    return err
}

if inArea {
    // do something 
} else {
    // do something else
}
</code></pre>

## In Range

The user can determine if two points are within a range of each other using the `InRange` function of the `Point`.

<pre><code class="language-go">
geometry := []Point{
    Point{}, Point{}, Point{}, Point{}
}

pointOne := Point{
    Latitude: latitude, 
    Longitude: longitude
}

pointTwo := Point{
    Latitude: latitude, 
    Longitude: longitude
}

// Only Meters distance is supported -> 1 km
inRange, err := pointOne.InRange(pointTwo, 1000.0)
if err != nil {
    return nil
}

if inRange {
    // do something
} else {
    // do something else
}
</code></pre>
<br>
<br>
**Note**: _Currently, the Go package only supports meters as a distance for InRange()_.
<br>
<br>

# Cache 

The following sections are provided as examples in the [cache package](https://github.com/barbacbd/nautical/blob/master/pkg/cache/).


## Dump data to file

Start by loading the data. There are several methods of doing so, but this example will manually create data.

<pre><code class="language-go">buoys := []noaa.Buoy{
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

	cacheData := NauticalCacheData{
        Filename: "example.json",
        CacheData: &NauticalCache{
            Buoys: buoys,
            Sources: sources,
            Time: time.Now().UTC().Add(-(time.Minute * time.Duration(minutesOffset))).Format(TimeLayout)
        }
    }

    if err := nauticalCache.Dump(); err != nil {
		// some error occurred
	}

</code></pre>


## Load data from file

Loading the cached data will supply the user/caller with a NauticalCacheData struct when no error exists.

<pre><code class="language-go">myCache := err, cacheData := Load(filename)
if err == nil {
    // Cached Data contains data to view manipulate.
}
</code></pre>


## Copying file contents

The user/caller has access to `CopyCurrentCache` and `CopyCurrentCacheWithTimestamp`. These functions will copy
the current contents of the cached file (if exists) to a new filename. The name of the file where the data was copied is returned by both functions.

The `CopyCurrentCache` function provides a bit more flexibility with the name as any data provided is appended to the name of `nautical_cache.json`.


For instance, the following snippet would set the filename to `nautical_cacheEXAMPLE.json`.
<pre><code class="language-go">myCache := NauticalCacheData{
    Filename: "nautical_cache.json"
}

err := myCache.CopyCurrentCache("EXAMPLE")
</code></pre>