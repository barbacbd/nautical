# Nautical Python Tutorials

The document contains the tutorials/examples for the python package.

# Table Of Contents

   * [IO](#io)
      * [Buoys](#buoys)
      * [Sources](#sources)
   * [Location](#location)
      * [In Area](#in-area)
      * [In Range](#in-range)
   * [Cache](#cache)
      * [Dump Data To File](#dump-data-to-file)
      * [Load Data From File](#load-data-from-file)
      * [Copying File Contents](#copying-file-contents)

# IO

The following sections are provided as examples in the [IO module](https://github.com/barbacbd/nautical/blob/master/nautical/io/).

## Buoys
If you know the ID of the buoy station you may use `create_buoy` as a shortcut to create a buoy object.

```python
from nautical.io.buoy import create_buoy

buoy = create_buoy(44099)
```

The result will be a buoy filled with all of the data that was pulled online. The user _should_ *always*
check the validity of the buoy after the function call(s) to ensure that the data can be trusted.

```python
if buoy.valid:
````

If the user already has a buoy object and wants to get the most up-to-date information, use te `fill_buoy`
function. It is important to note that this will also keep the buoy's past retrievals. The information that
was previously stored in the buoy object will be moved to the `past` attribute of the buoy.

```python
from nautical.noaa.buoy import Buoy
from nautical.io.buoy import fill_buoy

buoy = Buoy(44099, "This is a test for 44099")
fill_buoy(buoy)
```

If the user wishes to view all data inside of a buoy they can iterate over the object. All
of the available variables can be found [here](https://github.com/barbacbd/nautical/blob/master/nautical/noaa/buoy/buoy_data.py) in the
`buoy_vars` list..

```python
for var_name, value in buoy.data:
    print(var_name, value)
```

The `past` data is considered deprecated, but will remain in the project. Similar to the retrieval
above, the user can access the past data (a list of all past entries) in the buoy and iterate over
the `BuoyData` objects.

## Sources

NOAA provides a KML document containing all sources and the buoys that are grouped together by that
source. The document also provides minimal information about buoys in the event that they cannot
be retrieved online.
<br>
<br>
**Note**: The `TAO` and `Tsunami` sources are not available in any regard.
<br>
<br>
If the user wishes to make a record for `ALL` sources and their buoys use the default settings when
calling the `get_buoy_sources`.

```python
from nautical.io.sources import get_buoy_sources

source_information = get_buoy_sources()
```

Similarly, the user can provide a specific type of source to find. The snippet below will only return
the source information for `International Partners`.

```python
from nautical.io.sources import get_buoy_sources
from nautical.noaa.buoy import SourceType

source_information = get_buoy_sources(SourceType.INTERNATION_PARTNERS)
```

The user is now provided will source information for ALL sources. To view the sources use the following
snippet.

```python
for source, source_obj in sources.items():
    print(f"==== Viewing source {source} ====")

    # the invalid buoys are still in the source, so the number is inflated
    print(f"{source} contains {len(source)} buoys")

    # look at each buoy
    for buoy_hash, buoy_obj in source_obj.buoys.items():
    	print(str(buoy_obj))
```

The buoy objects above are created but not filled (unless they are SHIPS). In order to fill the buoys
use the `validate_sources` function.

```python
from nautical.io.sources import validate_sources

validated_sources = validate_sources(sources)
```

The default configuration (above) will filter out any buoys that were not valid when they were filled
using `fill_buoy`. If the user wishes to keep all buoys, pass `False` as the second argument to the function.
In the event that a source has _no valid buoys_, the source will *not* be returned in the new dictionary. 


# Location

The following sections are provided as examples in the [location module](https://github.com/barbacbd/nautical/blob/master/nautical/location/).

## In area

The user is provided with convenience functions for `location Points`. If the user wants to determine if a
point (possibly the location of a buoy) is contained within a specific area they can use the `in_area_ function.

```python
from nautical.location import Point, in_area

# create points that make up a geometry here
geometry = [ '''Create points here and add to this list''' ]

point_to_check = Point(latitude, longitude)

if in_area(geometry, point_to_check):
   print("Point is in geometry")
```

Similarly, the user can pass the location of a buoy to determine if it is in the area.

```python
from nautical.location import Point, in_area
from nautical.noaa.buoy import Buoy

# create points that make up a geometry here
geometry = [ '''Create points here and add to this list''' ]

buoy = Buoy("test", "this is a test", Point(latitude, longitude))

if in_area(geometry, buoy.location):
   print("Buoy is in geometry")
```

## In Range

The user can determine if two points are within a range of each other using the `in_range`
static function of a `Point`.

```python
from nautical.location import in_range, Point

point_1 = Point(latitude_1, longitude_1)
point_2 = Point(latitude_2, longitude_2)

if in_range(point_1, point_2, 1000.0):
   print("In range")
```

The snippet above will compare two points directly using the base units (`Meters`).

```python
from nautical.location import in_range

if in_range(latitude_1, longitude_1, latitude_2, longitude_2, 1000.0):
   print("In range")
```

The snippet above will compare two sets of latitude/longitude coordinates using the base units (`Meters`).

If the user desires a different unit from `Meters` import `nautical.units.DistanceUnits` and select a new
desired unit (`CENTIMETERS` is not allowed).

Similar to the first snippet above, the user can check if a point is in range of another point directly.

```python
from nautical.location import Point

point_1 = Point(latitude_1, longitude_1)
point_2 = Point(latitude_2, longitude_2)

if point_1.in_range(point_2, 1000.0):
   print("In range")
```


# Cache 

The following sections are provided as examples in the [cache module](https://github.com/barbacbd/nautical/blob/master/nautical/cache/).


## Dump data to file

Start by loading the data. There are several methods of doing so, but here the data is loaded by json dictionaries.

```python
from nautical.cache import dump
from nautical.noaa.buoy import Buoy, Source

buoy1 = Buoy.from_json(
   {   
            "data": {
               'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
               'wspd10m': 10.4, 'wspd20m': 13.4,
               'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
               'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
               'swh': 10.0, 'swp': 1.4, 'swd': "W",
               'pres': 1.8, 'ptdy': 1.8,
               'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
               'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
            },
            "station": "TestStationID",
            "description": "Test Description",
            "valid": True,
            "location": {
               "latitude": 36.0,
               "longitude": -75.34
            }
      }
)
        
source1 = Source.from_json(
   {
      "buoys": [
            {
               "station": "TestBuoy",
               "data": {
                  'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                  'wspd10m': 10.4, 'wspd20m': 13.4,
                  'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                  'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                  'swh': 10.0, 'swp': 1.4, 'swd': "W",
                  'pres': 1.8, 'ptdy': 1.8,
                  'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                  'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
               }            
            }
      ],
      "name": "TestSource",
      "description": "Test Source"
   }
)

```

Add the data to a dictionary that will contain the cached data to be saved. 
The following keys are allowed:
- "BUOYS"
- "SOURCES"
<br>
<br>
**Note**: _See the [CacheData enumeration](https://github.com/barbacbd/nautical/blob/master/nautical/cache/file.py#l25) for more information_.
<br>
<br>
```python    
cache_data = {
   CacheData.BUOYS.name: [buoy1, buoy2],
   CacheData.SOURCES.name: [source1, source2]
}
```

Provide the data to be cached and the filename [optional].

```python
dumps(tmp_data)
```

## Load data from file

Loading the cached data will supply the user/caller with a dictionary where the keys can be fouund in the [CacheData enumeration](https://github.com/barbacbd/nautical/blob/master/nautical/cache/file.py#l25).

```python
from nautical.cache import load

cache_data = load()
```

The [load function](https://github.com/barbacbd/nautical/blob/master/nautical/cache/file.py#l73) accepts a filename and type of data to be returned.
<br>
<br>
**Note**: _Default filename is the `nautical_cache.json`_.
<br>
**Note**: _Default returned data is `CacheData.ALL`_.
<br>
<br>

## Copying file contents

The user/caller has access to `copy_current_cache` and `copy_current_cache_with_timestamp`. These functions will copy
the current contents of the cached file (if exists) to a new filename. The name of the file where the data was copied is returned by both functions.

The `copy_current_cache` function provides a bit more flexibility with the name as any data provided is appended to the name of `nautical_cache.json`.


For instance, the following snippet would return `nautical_cacheEXAMPLE.json`.
```python
filename = copy_current_cache("EXAMPLE")
```
