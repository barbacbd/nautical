# Github Documentation

This document will provide instructions for generating the formal documentation for the `Nautical` package.
The documentation can be found [here](https://barbacbd.github.io/nautical/build/html/index.html). 

# Location

The `pages` branch will always contain all of the [documentation](https://barbacbd.github.io/nautical/build/html/index.html).
As new code is added to the repository (on `master`), the `pages` branch must be rebased off of `master` and the
documents should be regenerated based on the new source.

# Process

The following should be executed from the base of the project:

```bash
wget https://raw.githubusercontent.com/barbacbd/auto_doc/master/auto_doc.sh;
chmod 777 auto_doc.sh;
./auto_doc.sh
```

# Examples

The following are examples that can be copied and modified for a user's specific needs.

## IO - Buoys

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
of the available variables can be found [here](../../nautical/noaa/buoy/buoy_data.py) in the
`buoy_vars` list..

```python
for var_name, value in buoy.data:
    print(var_name, value)
```

The `past` data is considered deprecated, but will remain in the project. Similar to the retrieval
above, the user can access the past data (a list of all past entries) in the buoy and iterate over
the `BuoyData` objects.

## IO - Sources

NOAA provides a KML document containing all sources and the buoys that are grouped together by that
source. The document also provides minimal information about buoys in the event that they cannot
be retrieved online.

**Note**: The `TAO` and `Tsunami` sources are not available in any regard.

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


## Location - In Area

The user is provided with convenience functions for `location Points`. If the use wants to determine if a
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

## Location - In Range

The user can determine if two points are within a range of each other using the `in_range`
static function of the `in_range` function of a `Point`.

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


