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

- [io](./io) - The module contains the majority of the code where the user can read all buoy data, parse kml, parse beautiful soup 
html output, and grab some of the specific data from the tables that we are looking for.
- [location](./location) - The module contains a 3D Point class that can be used to store locations as well as determine distance
to and from other points.
- [noaa](./noaa) - The module contains classes to store/utilize/manipulate swell and wave data read in from NOAA's website. 
There are also some extra functions such as getting the sea state based on the current wave height.

## How to use this module

1. Start by getting all of the buoy information (unless you already know the buoy id that you wish to lookup).

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

2. Get the beautiful soup object for this buoy, so that we can move on to parsing through some of the data.

```python
from nautical.io import get_noaa_forecast_url, get_url_source
url = get_noaa_forecast_url(name)
soup = get_url_source(url)
```

3. Now that we have the beautiful soup object we can get some of the data from the tables.

```python
from nautical.io import get_current_data
attrs = get_current_data(soup, name)
```
4. Parse through the data at your own discretion and find what you are looking for

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

## Furture Work
1. Further Testing to ensure all tables are readable
2. Unit Tests
3. Parse the current wave data better
4. Parse the current swell data better
5. True Parsers for the tables
6. Ability to save the data on the computer and read last known values in
