from forecaster.noaa_kml import BuoyLookup
from forecaster.location import Point
from forecaster import wave_io
from forecaster.wave_data import SeaState
import math


"""
This is a test program to grab some relatively simple information near Virginia Beach.
Get the data for the nearest buoy to Virginia Beach, but make sure that we only get 
a buoy that is in the water. The nearest buoy is actually at Cape Henry and is not
in the water. Print out the data about this buoy and the current sea state.
"""


bl = BuoyLookup(True)

p = Point()
p.set_latitude(36.8529)
p.set_longitude(-75.9780)

print("Searching for NOAA Data Near {}, {}".format(p.lat, p.lon))

min_distance = float("inf")
name = ""
lat = 0
lon = 0

for buoy in bl.buoys:
    dist = p.get_distance(buoy.location.lat, buoy.location.lon)/1000.0

    #print("{}: {}, {}".format(buoy.name, buoy.location.lat, buoy.location.lon))

    if dist < min_distance:
        name = buoy.name
        min_distance = dist
        lat = buoy.location.lat
        lon = buoy.location.lon

print("Found Buoy {} at {},{}: {} meters from the search location".format(name, lat, lon, min_distance))

url = wave_io.get_noaa_forecast_url(name)

attrs = wave_io.get_current_data(url, name)

wave_height = 0.0

for attr in attrs:
    if 'Wave Height' in attr[0]:
        
        try:
            stuff = attr[1].split()
            wave_height = float(stuff[0])
        except ValueError:
            pass

ss = SeaState()
state = ss.get_state(wave_height / 3.28) # move it to meters

print("Wave Height = {} \nSea State = {}".format(wave_height, state)) 

