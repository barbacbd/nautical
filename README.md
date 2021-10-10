# Nautical

![build workflow](https://github.com/barbacbd/nautical/actions/workflows/python-app.yml/badge.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/barbacbd/nautical/pulse/commit-activity)
[![GitHub latest commit](https://badgen.net/github/last-commit/Naereen/nautical)](https://github.com/barbacbd/nautical/commit/)


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)


[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)


Author: Brent Barbachem  
Alias: barbacbd  
Date: May 18, 2019

## Description

A python based web scraper to grab the buoy data from [NOAA](https://www.ndbc.noaa.gov/). The scraper utilizes kml parsing
and BeautifulSoup to parse through data found online. NOAA is very kind in the fact that they allow the lookup of Buoy
data very easily using the same url with the id of the buoy at the end of the url. We can grab all of the buoy ids, append
the id to the url, and get several tables of output from the url. All of the data stored in the tables is updated in 30 minute
increments.

## Structure

### [error](./error) 

The module contains the custom exception used in this package.

```python
class NauticalError(Exception):
```

In the event of an error generated by this package, the user should except `NauticalError`.

### [io](./io) 

The module contains the majority of the code where the user can read all buoy data, parse kml, parse beautiful soup 
html output, and grab some of the specific data from the tables that we are looking for.

### [location](./location)
The module contains a 3D Point class that can be used to store locations as well as determine distance
to and from other points.

The module also provides the user with a simple distance function to provide distance between two points and
a function to determine if the point is located within a specified area. 

### [noaa](./noaa/buoy) 
The module contains classes to store/utilize/manipulate swell and wave data read in from NOAA's website. 
There are also some extra functions such as getting the sea state based on the current wave height.

### [sea_state](./sea_state)
Module to allow the user to estimate the current sea state based on wave heights.

|Sea State|Wave Height (meters)|
|---------|----------------|
|0|0 - 0|
|1|0 - 0.1|
|2|0.1 - 0.5|
|3|0.5 - 1.25|
|4|1.25 - 2.5|
|5|2.5 - 4.0|
|6|4.0 - 6.0|
|7|6.0 - 9.0|
|8|9.0 - 14.0|
|9|14.0+|


### [tests](./tests)
The module contains the unit tests for the Nautical package.

The module contains the link to the executable to run all tests for the package with 
 the executable named `NauticalTests`.

### [time](./time) 
Time module to parse and store the time as it is represented from NOAA's webpages.

### [units](./units) 
Utility package to provide the user with the easy ability to alter the units for the data.

The following display the supported unit types for each category:

|Time|
|----|
|Seconds|
|Minutes|
|Hours|
|Days|


|Temperature|
|-----------|
|Fahrenheit|
|Celsius|


|Speed|
|-----|
|Knots|
|Meters per second|
|Miles per hour|
|Kilometers per hour|
|Feet per second|


|Distance|
|--------|
|Centimeters|
|Feet|
|Yards|
|Meters|
|Milometers|
|Miles|
|Nautical Miles|


The user can convert values to a different unit IFF the units are in the same class. 

```python
from nautical.units.conversion import convert

def convert(value, init_units, final_units):
    """
    Convert the value given the current units to the new units. If the
    units are not in the same set of units then the value cannot be converted,
    and None will be returned.
    """
```

## Examples


### Sources

NOAA categorizes all buoys by a source. We can obtain all sources and the buoys the are cateogrized with each
source with one function.

```python
from nautical.io.sources import get_buoy_sources

sources = get_buoy_sources()
```

If this action was successful, sources will be a dictionary mapping the name of the source to the 
[source object](./nautical/noaa/buoy/source.py).  

We can also obtain the information about each buoy contained in the source.

```python
for _, source in sources.items():
    print(source)

    for buoy in source:
        print("\t{}".format(str(buoy)))
```

### Buoy Location

In the [previous example](###Sources) we were able to find all sources and their respective buoys. If we want to
search through this list to find a buoy near or at a location we can.

```python
for _, source in sources.items():
    for buoy in source
        location = buoy.location

        if location:
            # determine if the location meets criteria
```

### Buoy Information

In the [previous examples](###Sources) we were able to find all of the buoys that NOAA provides updated information about. If the
user finds a buoy of interest. If we want to retrieve all of the information for a particular buoy including present and 
past recordings, we can utilize the tools below. 

```python
from nautical.io.buoy import create_buoy

buoy_id = "example_buoy_id"

buoy = create_buoy(buoy_id)
```

This will return a `nautical.noaa.buoy.buoy.Buoy` object. 
