"""
Author: barbacbd

Description: This file contains constants that will be used through
out the IO module.
"""

# The known public link to all NOAA Buoys
KML_LINK = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"

# Default text to use as a search parameter for obtaining buoy
# information from a table
DEFAULT_BUOY_WAVE_TEXT_SEARCH = "Conditions at {} as of"

# Default text to use as a search parameter for obtaining swell
# information from a table
SWELL_DATA_TEXT_SEARCH = "Detailed Wave Summary"

# Text to search for previous observations. These values
# may occur in multiple tables. Unfortunately we have to
# provide exact text matches
PREVIOUS_OBSERVATION_SEARCH = "Previous observations"
