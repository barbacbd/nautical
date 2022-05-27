from nautical.time import NauticalTime, TimeFormat
from nautical.log import get_logger
from nautical.location import Point
from nautical.noaa.buoy import BuoyData


log = get_logger()


def parse_winds(wind_data):
    '''Parse the wind information. The wind data includes
    a direction, speed in knots, as well as the gust speed
    
    :param wind_data: String containing the wind string
    :return: Dictionary containing the windspeed and gust information
    '''
    split_wind_data = wind_data.split()

    wind_speed = None
    gusts = None

    for data_point in split_wind_data:

        try:
            float_value = float(data_point)

            if wind_speed is None:
                wind_speed = float_value
            else:
                if gusts is None:
                    gusts = float_value
        except ValueError as error:
            log.debug(error)

    return {"wspd": wind_speed, "gst": gusts}


def parse_location(location_data):
    '''Parse the latitude and longitude values out of the
    the string that was passed in. The latitude and longitude
    should contain the NSEW strings describing their sign.

    :param location_data: String data contain latitude and longitude values
    :return: dictionary containing the location point (when valid)
    '''
    def _describe(data):
        '''Describe or determine lat vs lon, positivity, and
        the value that needs to be calculated. 
        '''
        _lookup = {
            "n": ("latitude", 1.0),
            "s": ("latitude", -1.0),
            "e": ("longitude", 1.0),
            "w": ("longitude", -1.0),
        }
        _data = data.lower()

        for key, value in _lookup.items():
            if key in _data:
                return value[0], value[1], _data.replace(key, '')
        return None, 0.0, None

    location_dict = {}  # base/default return
    split_location = [x for x in location_data.split() if x]

    latitude = None
    longitude = None

    for loc_data in split_location:
        ll_val, sign, val = _describe(loc_data)

        try:
            fval = float(val)

            if ll_val == "latitude":
                latitude = sign * fval
            elif ll_val == "longitude":
                longitude = sign * fval

        except (ValueError, TypeError) as error:
            log.debug(error)

    if None not in (latitude, longitude):
        location_dict["location"] = Point(latitude, longitude)

    return location_dict


def parse_time(time_data):
    '''Parse the month/day/year time out of the time
    data string from CDATA.

    :param time_data: String containing all time and date information
    :return: dictionary mm, dd, year, time where time is NauticalTime
    '''
    nautical_time = None
    month = None
    day = None
    year = None

    try:
        split_time_data = time_data.split()

        # date should be the first in the list
        date_data = split_time_data[0].split("/")
        month = int(date_data[0])
        day = int(date_data[1])
        year = int(date_data[2])

        # Get the minutes and hours out of the time in the list
        hour_min = split_time_data[1]
        hours = int(hour_min[:2])
        mins = int(hour_min[2:])
        nautical_time = NauticalTime(fmt=TimeFormat.HOUR_24)
        nautical_time.hours = hours
        nautical_time.minutes = mins
    except (IndexError, ValueError, TypeError) as error:
        log.debug(error)

    # output a dictionary containing the keys and values that are expected
    # during a normal web scrape of buoy information
    return {"time": nautical_time, "dd": day, "mm": month, "year": year}


# The alias is linked to the name contained in the BuoyData
aliases = {
    "gust": "gst",
    "wave height": "wvht",
    "significant wave height": "wvht",
    "dominant wave period": "dpd",
    "average wave period": "apd",
    "atmospheric pressure": "pres",
    # ptdy
    "air temperature": "atmp",
    "water temperature": "wtmp",
    "dew point": "dewp",        
    "salinity": "sal",
    "visibility": "vis",
    "tide": "tide",
    "swell wave heigh": "swh",
    "swell wave period": "swp",
    "wind wave height": "wwh",
    "wind wave period": "wwp",
    "wind speed": "wspd"
}

# The alias is actually multiple values, so let's use a function to parse
alias_func = {
    "winds": parse_winds,
    "location": parse_location
}


def parse_cdata(cdata):
    '''Parse the CDATA string that contains information about this 
    presumed buoy. The data here will be used as supplemental information
    as some buoys cannot be scraped online (no valid or useable data).

    :param cdata: String containing the CDATA or description element from kml
    :return: Dictionary containing all parsed fields.
    '''
    parsed_cdata_dict = {}

    # data is separated by line breaks, cut there
    xml_data = cdata.split("<br />")

    for xd_val in xml_data:

        # remove the tags
        elements = [x for x in xd_val.strip().replace("<b>", "").split("</b>") if x]
        # no elements found, don't bother searching
        if not elements:
            continue

        # format the string to remove colons and lowercase for searching
        key = elements[0].replace(":", "").lower()

        if key in alias_func:
            # all functions need to return a dictionary
            parsed_cdata_dict.update(alias_func[key](elements[1]))
        elif key in aliases:
            # The first element in the string will be the value
            # assumes default units
            try:
                parsed_cdata_dict[aliases[key]] = float(elements[1].split()[0])
            except ValueError as error:
                # skip the value if the value was not a float
                log.error(error)
        elif "utc" in key:
            parsed_cdata_dict.update(parse_time(key))

    # filter out the results that returned None
    return {k: v for k, v in parsed_cdata_dict.items() if v is not None}


def fill_buoy_with_cdata(buoy, cdata):
    '''Parse the CDATA string that contains information about this 
    presumed buoy. The data here will be used as supplemental information
    as some buoys cannot be scraped online (no valid or useable data).

    :param buoy: nautical.noaa.buoy.Buoy
    :param cdata: String containing the CDATA or description element from kml
    :return: Buoy object
    '''
    buoy_data = BuoyData()

    parsed_cdata = parse_cdata(cdata)

    # set the location for this station if found
    if "location" in parsed_cdata:
        loc = parsed_cdata.pop("location")
        buoy.location = loc

    # fill the buoy_data with the parsed data
    buoy_data.from_dict(parsed_cdata)
    buoy.present = buoy_data
