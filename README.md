# Nautical

## Details
Author: Brent Barbachem

Date: May 18, 2019

## Description

Originally this project was developed to attempt to get the current data from NOAA for surfing purposes. The project has 
evolved and taken a step in a different direction, and it now focuses on a broad nautical spectrum.

A python based web scraper to grab the surf data from [NOAA](https://www.ndbc.noaa.gov/). The scraper has utilizes kml parsing
and BeautifulSoup to parse through data found online. NOAA is very kind in the fact that they allow the lookup of Buoy
data very easily using the same url with the id of the buoy at the end of the url. We can grab all of the buoy ids, append
the id to the url, and get several tables of output from the url. All of the data stored in the tables is updated in 30 minute
increments.

Notable data of interest includes:
1. Preset Wave Data
2. Present Swell Data
3. Past Wave Date
4. Past Swell Data

## Structure

- [error](./error) - The module contains the custom exception used in this package.
- [io](./io) - The module contains the majority of the code where the user can read all buoy data, parse kml, parse beautiful soup 
html output, and grab some of the specific data from the tables that we are looking for.
- [location](./location) - The module contains a 3D Point class that can be used to store locations as well as determine distance
to and from other points.
- [noaa](./noaa) - The module contains classes to store/utilize/manipulate swell and wave data read in from NOAA's website. 
There are also some extra functions such as getting the sea state based on the current wave height.
- [tests](./tests) - The module contains the unit tests for the Nautical package.

## How to use this module

Start by getting all of the buoy information (unless you already know the buoy id that you wish to lookup).

```python
from nautical.io import get_buoys_information
# passing True will mean that you only grab data from locations that contain wave data
buoys = get_buoys_information(True)
```

Find the id of the buoy in the list of buoys that you wish to receive data from:

```python
from nautical.location import Point
# this example picks a point and we want to find a point close to this one and use its data.

p = Point()
p.set_latitude(36.8529)
p.set_longitude(-75.9780)

min_distance = float("inf")
name = ""
lat = 0
lon = 0

for key, value in buoys.items():
    dist = p.get_distance(value.lat, value.lon)/1000.0

    if dist < min_distance:
        name = key
        min_distance = dist
        lat = value.lat
        lon = value.lon
```

Get the beautiful soup object for this buoy, so that we can move on to parsing through some of the data.

```python
from nautical.io import get_noaa_forecast_url, get_url_source
url = get_noaa_forecast_url(name)
soup = get_url_source(url)
```

Now that we have the beautiful soup object we can get some of the data from the tables.

```python
from nautical.io import get_current_data
attrs = get_current_data(soup, name)
```
Parse through the data at your own discretion and find what you are looking for

```python
from nautical.noaa import get_sea_state
wave_height = 0.0

for attr in attrs:
    if 'Wave Height' in attr[0]:
        
        try:
            stuff = attr[1].split()
            wave_height = float(stuff[0])
        except ValueError:
            pass

# convert the sea state to meters and get the sea state
state = get_sea_state(wave_height / 3.28)

print("Wave Height = {} meters\nSea State = {}".format(wave_height, state))
```

The output of this sample is:
```text
Searching for NOAA Data Near 36.8529, -75.978
Found Buoy 44064 at 36.998,-76.087: 18.825457352951904 meters from the search location
Wave Height = 1.0 meters
Sea State = 2
```

If you wish to get all past and present informmation (over a 24 hour period) about a buoy, there are several
different ways to go about this:

The simplest way is to get all of the data at once (that is available):

```python
buoy = 44099
data = buoy_workup(buoy)
```

This example will grab all of the current data about the buoy. However, if you wish to grab specific information
about the buoy you can use any of the following:

```python
current_wave_search = "Conditions at {} as of".format(buoy)
data.present_wave_data = get_current_data(soup, current_wave_search)

detailed_search = "Detailed Wave Summary"
data.present_swell_data = get_current_data(soup, detailed_search)

data.past_data = get_past_data(soup)
```



## Unit Tests

To run the unit tests utilize the unit test suite provided by the unit test python package. The following python snippet 
demonstrates a simple way to run all of the unit tests. If the _test_beautiful_soup_ or _test_forecast_url_ tests fail, then
there is a good possibility that you are not connected to the internet OR you cannot reach the noaa website.

```python
from nautical.tests import *

suite = TestNautical.suite()
unittest.TextTestRunner().run(suite)
```

## Troubleshooting

If you are using _python3.5_, _pykml_ will install with references to urllib2. Please edit the files in the 
_pykml_ directory with the following change(s):

```python
import urllib as urllib2
```