# Exception Refactoring Examples

This document shows concrete before/after examples of refactoring code to use custom exceptions.

## Example 1: `nautical/units/conversion.py`

### Before (lines 50-63)
```python
def convert_temperature(value, init_units, final_units):
    '''Convert the temperature value from the initial units to the
    final units

    :param value: initial value for temperature
    :param init_units: initial units for temperature
    :param final_units: desired temperature units
    :return: value converted from the initial units to the final units
    '''
    if not isinstance(init_units, TemperatureUnits) or \
       not isinstance(final_units, TemperatureUnits):
        raise KeyError
    _temp = value if init_units in (TemperatureUnits.DEG_F,) else (9.0 / 5.0 * value) + 32.0
    return _temp if final_units in (TemperatureUnits.DEG_F,) else (_temp - 32) * 5.0 / 9.0
```

### After
```python
from nautical.exceptions import InvalidUnitsError

def convert_temperature(value, init_units, final_units):
    '''Convert the temperature value from the initial units to the
    final units

    :param value: initial value for temperature
    :param init_units: initial units for temperature
    :param final_units: desired temperature units
    :return: value converted from the initial units to the final units
    :raises InvalidUnitsError: If init_units or final_units are not TemperatureUnits
    '''
    if not isinstance(init_units, TemperatureUnits):
        raise InvalidUnitsError(
            f"Invalid initial temperature unit: {init_units!r}. "
            f"Expected TemperatureUnits enum value.",
            unit=init_units,
            valid_units=list(TemperatureUnits)
        )
    
    if not isinstance(final_units, TemperatureUnits):
        raise InvalidUnitsError(
            f"Invalid final temperature unit: {final_units!r}. "
            f"Expected TemperatureUnits enum value.",
            unit=final_units,
            valid_units=list(TemperatureUnits)
        )
    
    _temp = value if init_units in (TemperatureUnits.DEG_F,) else (9.0 / 5.0 * value) + 32.0
    return _temp if final_units in (TemperatureUnits.DEG_F,) else (_temp - 32) * 5.0 / 9.0
```

### Before (lines 66-79)
```python
def convert_time(value, init_units, final_units):
    '''Convert the time value from the initial units to the final units

    :param value: initial value for time
    :param init_units: initial units for time
    :param final_units: desired time units
    :return: value converted from the initial units to the final units
    :raises KeyError: 
    '''
    try:
        return value * TimeLookup[init_units] / TimeLookup[final_units]
    except KeyError as key_error:
        log.error(key_error)
        raise
```

### After
```python
from nautical.exceptions import InvalidUnitsError

def convert_time(value, init_units, final_units):
    '''Convert the time value from the initial units to the final units

    :param value: initial value for time
    :param init_units: initial units for time
    :param final_units: desired time units
    :return: value converted from the initial units to the final units
    :raises InvalidUnitsError: If init_units or final_units are not recognized
    '''
    try:
        return value * TimeLookup[init_units] / TimeLookup[final_units]
    except KeyError as e:
        # Determine which unit was invalid
        if init_units not in TimeLookup:
            raise InvalidUnitsError(
                f"Unknown time unit: {init_units!r}. "
                f"Valid units: {list(TimeLookup.keys())}",
                unit=init_units,
                valid_units=list(TimeLookup.keys())
            ) from e
        else:
            raise InvalidUnitsError(
                f"Unknown time unit: {final_units!r}. "
                f"Valid units: {list(TimeLookup.keys())}",
                unit=final_units,
                valid_units=list(TimeLookup.keys())
            ) from e
```

### Before (lines 141-159)
```python
def convert(value, init_units, final_units):
    '''Convert the value given the current units to the new units. If the
    units are not in the same set of units then the value cannot be converted,
    and None will be returned.

    :param value: Value provided in the units (init_units)
    :param init_units: initial units of the value (must match final units type)
    :param final_units: final units of the value (must match initial units type)
    :return: The value converted to the final units. If the units did not match None is returned
    :raises TypeError: when the two types do not match, or when any of the parameters are None
    '''

    if None not in (value, init_units, final_units) and isinstance(final_units, type(init_units)):
        func = ConversionLookup.get(type(init_units), None)
        if callable(func):
            return func(value, init_units, final_units)

    raise TypeError  # two types did not match 
```

### After
```python
from nautical.exceptions import UnitMismatchError, UnsupportedConversionError

def convert(value, init_units, final_units):
    '''Convert the value given the current units to the new units.

    :param value: Value provided in the units (init_units)
    :param init_units: initial units of the value (must match final units type)
    :param final_units: final units of the value (must match initial units type)
    :return: The value converted to the final units
    :raises UnitMismatchError: When init_units and final_units are incompatible types
    :raises UnsupportedConversionError: When conversion function is not implemented
    :raises ValueError: When value, init_units, or final_units is None
    '''
    if value is None or init_units is None or final_units is None:
        raise ValueError(
            f"None values not allowed. Got: value={value!r}, "
            f"init_units={init_units!r}, final_units={final_units!r}"
        )
    
    if not isinstance(final_units, type(init_units)):
        raise UnitMismatchError(
            f"Cannot convert between incompatible unit types: "
            f"{type(init_units).__name__} → {type(final_units).__name__}",
            from_unit=init_units,
            to_unit=final_units
        )
    
    func = ConversionLookup.get(type(init_units), None)
    if not callable(func):
        raise UnsupportedConversionError(
            f"No conversion function available for {type(init_units).__name__}"
        )
    
    return func(value, init_units, final_units)
```

---

## Example 2: `nautical/io/web.py`

### Before (lines 25-41)
```python
def get_url_source(url_name):
    '''If you already know the url_name or if you have run through the 
    get_noaa_forecast_url(), then you can send in the url here. Get the source 
    information for the url and place the information into a BeautifulSoup
    object, so that we can do any lookups of the data that we need.

    :param url_name: name of the url to search for
    :return: BeautifulSoup Object on success otherwise none
    '''
    try:
        open_url = urlopen(url_name)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    except (AttributeError, TypeError, ValueError, HTTPError) as error:
        log.error(error)
        raise
```

### After
```python
from urllib.error import HTTPError, URLError
from socket import timeout as SocketTimeout
from nautical.exceptions import (
    NOAAServiceError,
    BuoyNotFoundError,
    NetworkTimeoutError
)

def get_url_source(url_name):
    '''Fetch and parse the NOAA buoy data webpage.

    :param url_name: URL to fetch
    :return: BeautifulSoup object containing the parsed HTML
    :raises BuoyNotFoundError: If the buoy station does not exist (404)
    :raises NetworkTimeoutError: If the request times out
    :raises NOAAServiceError: If NOAA service returns an error or is unavailable
    :raises ValueError: If url_name is None or empty
    '''
    if not url_name:
        raise ValueError("url_name cannot be None or empty")
    
    try:
        open_url = urlopen(url_name, timeout=30)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    
    except HTTPError as e:
        if e.code == 404:
            # Extract station ID from URL if possible
            station = None
            if "station=" in url_name:
                station = url_name.split("station=")[-1].split("&")[0]
            
            raise BuoyNotFoundError(
                f"Buoy station not found: {station or 'unknown'}",
                station=station,
                url=url_name
            ) from e
        else:
            raise NOAAServiceError(
                f"NOAA service returned HTTP {e.code}: {e.reason}",
                url=url_name,
                status_code=e.code,
                original_error=e
            ) from e
    
    except (URLError, SocketTimeout) as e:
        raise NetworkTimeoutError(
            f"Request to NOAA service timed out: {url_name}",
            url=url_name,
            timeout=30
        ) from e
    
    except (AttributeError, TypeError, ValueError) as e:
        raise NOAAServiceError(
            f"Failed to parse NOAA response: {e}",
            url=url_name,
            original_error=e
        ) from e
```

---

## Example 3: `nautical/io/cdata.py`

### Before (lines 10-35)
```python
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
```

### After
```python
from nautical.exceptions import InvalidWindDataError

def parse_winds(wind_data):
    '''Parse the wind information from CDATA.
    
    :param wind_data: String containing wind direction and speeds
    :return: Dictionary containing the windspeed and gust information
    :raises InvalidWindDataError: If wind_data cannot be parsed or is invalid
    '''
    if not wind_data or not isinstance(wind_data, str):
        raise InvalidWindDataError(
            f"Wind data must be a non-empty string, got: {wind_data!r}"
        )
    
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
        except ValueError:
            # Skip non-numeric values (e.g., direction indicators)
            log.debug(f"Skipping non-numeric wind data: {data_point}")
            continue
    
    # Validate that we got at least wind speed
    if wind_speed is None:
        raise InvalidWindDataError(
            f"No valid wind speed found in: {wind_data!r}"
        )

    return {"wspd": wind_speed, "gst": gusts}
```

---

## Example 4: `nautical/location/point.py`

### Before (lines 39-55)
```python
def SetLatitude(self, latitude: float) -> None:
    if latitude > 90 or latitude < -90:
        return fmt.Errorf("latitude not in range (-90, 90): %.2f", latitude)
    p.Latitude = latitude
    return nil


def SetLongitude(self, longitude: float) -> None:
    if longitude > 180 or longitude < -180:
        return fmt.Errorf("longitude not in range (-180, 180): %.2f", longitude)
    p.Longitude = longitude
    return nil
```

### After (Python version)
```python
from nautical.exceptions import OutOfBoundsError

def set_latitude(self, latitude):
    '''Set the latitude with validation.
    
    :param latitude: Latitude in degrees
    :raises OutOfBoundsError: If latitude is outside valid range (-90, 90)
    :raises TypeError: If latitude is not numeric
    '''
    try:
        lat = float(latitude)
    except (TypeError, ValueError) as e:
        raise TypeError(f"Latitude must be numeric, got: {latitude!r}") from e
    
    if lat > 90 or lat < -90:
        raise OutOfBoundsError(
            f"Latitude must be in range (-90, 90), got: {lat}",
            latitude=lat,
            value=lat,
            bounds=(-90, 90)
        )
    
    self.latitude = lat


def set_longitude(self, longitude):
    '''Set the longitude with validation.
    
    :param longitude: Longitude in degrees
    :raises OutOfBoundsError: If longitude is outside valid range (-180, 180)
    :raises TypeError: If longitude is not numeric
    '''
    try:
        lon = float(longitude)
    except (TypeError, ValueError) as e:
        raise TypeError(f"Longitude must be numeric, got: {longitude!r}") from e
    
    if lon > 180 or lon < -180:
        raise OutOfBoundsError(
            f"Longitude must be in range (-180, 180), got: {lon}",
            longitude=lon,
            value=lon,
            bounds=(-180, 180)
        )
    
    self.longitude = lon
```

---

## Example 5: User Code - Error Handling

### Before (user code)
```python
from nautical.io import create_buoy

try:
    buoy = create_buoy("INVALID")
except Exception as e:
    print(f"Something went wrong: {e}")
    # Can't tell if it's a network error, parsing error, or what
```

### After (user code)
```python
from nautical.io import create_buoy
from nautical.exceptions import (
    BuoyNotFoundError,
    NetworkTimeoutError,
    NOAAServiceError,
    InvalidBuoyDataError,
    NauticalError
)
import time

def fetch_buoy_with_retry(station_id, max_retries=3):
    '''Fetch buoy data with intelligent retry logic.'''
    for attempt in range(max_retries):
        try:
            return create_buoy(station_id)
        
        except BuoyNotFoundError as e:
            # Don't retry - buoy doesn't exist
            print(f"Buoy {e.station} not found")
            return None
        
        except NetworkTimeoutError as e:
            # Retry with exponential backoff
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Timeout, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"Failed after {max_retries} attempts")
                raise
        
        except InvalidBuoyDataError as e:
            # Data is corrupted - log and try cache
            print(f"Invalid data for {e.station}: {e}")
            # Try to load from cache instead
            return load_from_cache(station_id)
        
        except NOAAServiceError as e:
            # Service is down - wait longer
            if attempt < max_retries - 1:
                wait = 30  # NOAA might be down, wait longer
                print(f"NOAA service error, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
        
        except NauticalError as e:
            # Unknown nautical error
            print(f"Unexpected nautical error: {e}")
            raise
```

---

## Testing Examples

### Unit Test for Custom Exceptions
```python
import pytest
from nautical.units.conversion import convert_temperature
from nautical.units import TemperatureUnits
from nautical.exceptions import InvalidUnitsError

def test_convert_temperature_invalid_init_units():
    '''Test that InvalidUnitsError is raised for invalid init_units.'''
    with pytest.raises(InvalidUnitsError) as exc_info:
        convert_temperature(100, "invalid", TemperatureUnits.DEG_C)
    
    # Check error message
    assert "Invalid initial temperature unit" in str(exc_info.value)
    
    # Check attributes
    assert exc_info.value.unit == "invalid"
    assert exc_info.value.valid_units is not None


def test_convert_temperature_invalid_final_units():
    '''Test that InvalidUnitsError is raised for invalid final_units.'''
    with pytest.raises(InvalidUnitsError) as exc_info:
        convert_temperature(100, TemperatureUnits.DEG_F, None)
    
    assert exc_info.value.unit is None


def test_exception_inheritance():
    '''Test that custom exceptions maintain backward compatibility.'''
    # InvalidUnitsError inherits from KeyError
    with pytest.raises(KeyError):
        convert_temperature(100, "bad", TemperatureUnits.DEG_C)
    
    # More specific catch works too
    with pytest.raises(InvalidUnitsError):
        convert_temperature(100, "bad", TemperatureUnits.DEG_C)
```

---

## Migration Checklist

When refactoring a module to use custom exceptions:

- [ ] Import relevant exception classes
- [ ] Replace generic exceptions with custom ones
- [ ] Add helpful error messages with context
- [ ] Use `raise ... from e` to chain exceptions
- [ ] Populate exception attributes
- [ ] Update docstrings to document exceptions
- [ ] Add tests for new exception behavior
- [ ] Update any callers that need to catch specific exceptions
- [ ] Consider backward compatibility (inherit from old exception type)
