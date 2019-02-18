# SurfForecastScraper

A python based web scraper to grab the surf data from [NOAA](https://www.ndbc.noaa.gov/).
There scraper will grab all of the surf data from a buoy. There are some statically defined buoy
numbers and names. I added those values, because I thought I would use these the most. Someone 
can extend this functionality by adding their own values.

## Modules

- [analysis](./analysis) - the module is used to analyze small amounts of data from the recent past.
- [io](./io) - the web scraping module. Simple functions utilizing beautiful soup.
- [wave_data](./wave_data) - The module containing objects to hold the wave data.

## Execution

Move to the home directory of this application. 

> python2.7 surf.py

## Software Versions
- Python v2.7
- BeautifulSoup v4
