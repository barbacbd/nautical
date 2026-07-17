# Error Handling in Nautical

This guide explains how to properly handle errors when using the nautical package.

## Table of Contents

- [Overview](#overview)
- [Exception Hierarchy](#exception-hierarchy)
- [Common Scenarios](#common-scenarios)
  - [Fetching Buoy Data](#fetching-buoy-data)
  - [Unit Conversions](#unit-conversions)
  - [Cache Operations](#cache-operations)
  - [Location Calculations](#location-calculations)
- [Best Practices](#best-practices)
- [Migration from Old Code](#migration-from-old-code)

## Overview

The nautical package provides domain-specific exception classes that make error handling more precise and informative. All custom exceptions inherit from `NauticalError`, allowing you to:

1. Catch all nautical-specific errors with a single `except NauticalError`
2. Handle specific error types differently (e.g., retry on timeout but not on invalid station)
3. Get detailed error context (station IDs, URLs, invalid values, etc.)
4. Maintain backward compatibility with existing code

## Exception Hierarchy

```
NauticalError (base exception)
├── DataError (data parsing/validation errors)
│   ├── InvalidBuoyDataError
│   ├── InvalidSourceDataError
│   └── ParsingError (CDataParsingError, JSONParsingError)
│
├── ConversionError (unit conversion errors)
│   ├── InvalidUnitsError
│   ├── UnitMismatchError
│   └── UnsupportedConversionError
│
├── NetworkError (web scraping/API errors)
│   ├── BuoyNotFoundError
│   ├── NOAAServiceError
│   └── NetworkTimeoutError
│
├── CacheError (cache operations)
│   ├── CacheNotFoundError
│   ├── CacheWriteError
│   └── CacheReadError
│
└── LocationError (geographic calculations)
    ├── InvalidCoordinatesError
    ├── OutOfBoundsError
    └── DistanceCalculationError
```

For complete details, see [nautical/exceptions.py](../../nautical/exceptions.py).

## Common Scenarios

### Fetching Buoy Data

When fetching buoy data from NOAA, several errors can occur:

```python
from nautical.io.buoy import create_buoy
from nautical.exceptions import (
    BuoyNotFoundError,
    NetworkTimeoutError,
    NOAAServiceError,
    InvalidBuoyDataError,
    NauticalError
)

def fetch_buoy_safe(station_id):
    """Fetch buoy data with comprehensive error handling."""
    try:
        buoy = create_buoy(station_id)

        if not buoy or not buoy.valid:
            print(f"Warning: Buoy {station_id} returned invalid data")
            return None

        return buoy

    except BuoyNotFoundError as e:
        # Station doesn't exist - don't retry
        print(f"Buoy station '{e.station}' not found at {e.url}")
        print("Please verify the station ID is correct")
        return None

    except NetworkTimeoutError as e:
        # Network timeout - can retry
        print(f"Request to {e.url} timed out after {e.timeout}s")
        print("The NOAA service may be slow or unavailable")
        # Caller can implement retry logic
        raise

    except NOAAServiceError as e:
        # NOAA service error
        print(f"NOAA service error (HTTP {e.status_code}): {e}")
        if e.status_code >= 500:
            print("NOAA servers may be experiencing issues - try again later")
        raise

    except InvalidBuoyDataError as e:
        # Data parsing failed
        print(f"Failed to parse buoy data for {e.station}")
        if e.field:
            print(f"Problem with field: {e.field}")
        # Try to load from cache as fallback
        return load_from_cache(station_id)

    except NauticalError as e:
        # Catch-all for other nautical errors
        print(f"Unexpected error fetching buoy: {e}")
        raise
```

#### With Retry Logic

```python
import time
from nautical.exceptions import NetworkTimeoutError, NOAAServiceError

def fetch_buoy_with_retry(station_id, max_retries=3, timeout=30):
    """Fetch buoy data with exponential backoff retry."""
    last_error = None

    for attempt in range(max_retries):
        try:
            return create_buoy(station_id)

        except NetworkTimeoutError as e:
            last_error = e
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Timeout (attempt {attempt + 1}/{max_retries}), "
                      f"retrying in {wait}s...")
                time.sleep(wait)

        except NOAAServiceError as e:
            last_error = e
            # Only retry on server errors (5xx), not client errors (4xx)
            if e.status_code and 500 <= e.status_code < 600:
                if attempt < max_retries - 1:
                    wait = 30  # Longer wait for service issues
                    print(f"Service error (attempt {attempt + 1}/{max_retries}), "
                          f"retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    break
            else:
                # Don't retry client errors
                raise

    # All retries exhausted
    if last_error:
        raise last_error
```

### Unit Conversions

Unit conversion errors provide detailed information about what went wrong:

```python
from nautical.units import convert, TemperatureUnits, DistanceUnits
from nautical.exceptions import (
    InvalidUnitsError,
    UnitMismatchError,
    ConversionError
)

def safe_convert(value, from_unit, to_unit):
    """Convert units with error handling."""
    try:
        return convert(value, from_unit, to_unit)

    except InvalidUnitsError as e:
        print(f"Invalid unit: {e.unit}")
        if e.valid_units:
            print(f"Valid units: {e.valid_units}")
        return None

    except UnitMismatchError as e:
        print(f"Cannot convert {type(e.from_unit).__name__} "
              f"to {type(e.to_unit).__name__}")
        print("Units must be of the same type (e.g., both temperature)")
        return None

    except ConversionError as e:
        print(f"Conversion failed: {e}")
        return None

# Example usage
temp_f = safe_convert(100, TemperatureUnits.DEG_C, TemperatureUnits.DEG_F)
if temp_f is not None:
    print(f"Temperature: {temp_f}°F")
```

### Cache Operations

Cache errors include file paths for easier debugging:

```python
from nautical.cache import load, dumps
from nautical.exceptions import (
    CacheNotFoundError,
    CacheReadError,
    CacheWriteError,
    CacheError
)

def load_cached_buoys(cache_file=None):
    """Load buoys from cache with error handling."""
    try:
        return load(cache_file)

    except CacheNotFoundError as e:
        print(f"Cache file not found: {e.cache_path}")
        print("Creating new cache...")
        return {}

    except CacheReadError as e:
        print(f"Failed to read cache: {e.cache_path}")
        if e.original_error:
            print(f"Underlying error: {e.original_error}")
        # Corrupt cache - delete and start fresh
        return {}

    except CacheError as e:
        print(f"Cache error: {e}")
        return {}

def save_to_cache(data, cache_file=None):
    """Save data to cache with error handling."""
    try:
        dumps(data, cache_file)
        print("Cache saved successfully")

    except CacheWriteError as e:
        print(f"Failed to write cache: {e.cache_path}")
        if e.original_error:
            print(f"Reason: {e.original_error}")
        # Log error but don't fail the program
```

### Location Calculations

Location errors help identify coordinate and calculation issues:

```python
from nautical.location import Point, in_range
from nautical.exceptions import (
    InvalidCoordinatesError,
    OutOfBoundsError,
    DistanceCalculationError,
    LocationError
)

def create_point_safe(lat, lon):
    """Create a Point with validation."""
    try:
        point = Point(lat, lon)
        return point

    except OutOfBoundsError as e:
        print(f"Coordinate out of bounds: {e.value}")
        if e.bounds:
            print(f"Valid range: {e.bounds}")
        return None

    except InvalidCoordinatesError as e:
        print(f"Invalid coordinates: {e.coordinates}")
        return None

    except LocationError as e:
        print(f"Location error: {e}")
        return None

def calculate_distance_safe(point1, point2):
    """Calculate distance with error handling."""
    try:
        distance, err = point1.get_distance(point2)
        if err:
            raise err
        return distance

    except DistanceCalculationError as e:
        print(f"Distance calculation failed between {e.point1} and {e.point2}")
        if e.original_error:
            print(f"Reason: {e.original_error}")
        return None

    except LocationError as e:
        print(f"Location error: {e}")
        return None
```

## Best Practices

### 1. Catch Specific Exceptions First

```python
# Good
try:
    buoy = create_buoy(station_id)
except BuoyNotFoundError:
    # Handle missing buoy
    pass
except NetworkTimeoutError:
    # Handle timeout
    pass
except NauticalError:
    # Handle other nautical errors
    pass

# Avoid
try:
    buoy = create_buoy(station_id)
except Exception:  # Too broad
    pass
```

### 2. Use Exception Attributes

```python
try:
    buoy = create_buoy(station_id)
except BuoyNotFoundError as e:
    # Good - use exception attributes
    log_error(f"Station {e.station} not found at {e.url}")

    # Not as good - less informative
    log_error(str(e))
```

### 3. Re-raise When Appropriate

```python
def fetch_buoy(station_id):
    try:
        return create_buoy(station_id)
    except BuoyNotFoundError:
        # We can't recover from this - re-raise
        raise
    except NetworkTimeoutError:
        # We might retry this - re-raise
        raise
    except InvalidBuoyDataError:
        # We can recover by using cache
        return load_from_cache(station_id)
```

### 4. Preserve Original Exceptions

```python
try:
    # Your code
    pass
except NauticalError as e:
    # Check if there's an underlying exception
    if hasattr(e, 'original_error') and e.original_error:
        print(f"Caused by: {e.original_error}")
```

### 5. Log Appropriately

```python
import logging

logger = logging.getLogger(__name__)

try:
    buoy = create_buoy(station_id)
except BuoyNotFoundError as e:
    logger.warning(f"Buoy {e.station} not found")
except NetworkTimeoutError as e:
    logger.error(f"Network timeout for {e.url}", exc_info=True)
except NauticalError as e:
    logger.exception(f"Unexpected nautical error")
```

## Migration from Old Code

If you have existing code that catches built-in exceptions, it will continue to work due to backward compatibility:

```python
# Old code - still works!
try:
    result = convert(value, init_units, final_units)
except KeyError:  # Catches InvalidUnitsError
    print("Invalid units")

# New code - more specific
try:
    result = convert(value, init_units, final_units)
except InvalidUnitsError as e:
    print(f"Invalid unit {e.unit}. Valid: {e.valid_units}")
```

### Gradual Migration

You can migrate gradually by adding specific handlers:

```python
# Step 1: Keep existing broad catch
try:
    buoy = create_buoy(station_id)
except Exception as e:
    handle_error(e)

# Step 2: Add specific handlers before the broad catch
try:
    buoy = create_buoy(station_id)
except BuoyNotFoundError as e:
    handle_missing_buoy(e)
except NetworkTimeoutError as e:
    handle_timeout(e)
except Exception as e:
    handle_error(e)

# Step 3: Replace broad catch with NauticalError
try:
    buoy = create_buoy(station_id)
except BuoyNotFoundError as e:
    handle_missing_buoy(e)
except NetworkTimeoutError as e:
    handle_timeout(e)
except NauticalError as e:
    handle_nautical_error(e)
except Exception as e:
    handle_unexpected_error(e)
```

## Exception Reference

For a complete list of exceptions and their attributes, see:
- [nautical/exceptions.py](../../nautical/exceptions.py) - Exception definitions
- [EXCEPTION_DESIGN.md](../../EXCEPTION_DESIGN.md) - Design rationale
- [EXCEPTION_EXAMPLES.md](../../EXCEPTION_EXAMPLES.md) - Refactoring examples
