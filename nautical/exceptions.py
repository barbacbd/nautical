"""
Custom exception hierarchy for the nautical package.

This module defines domain-specific exceptions that provide better error
messages and allow for more precise error handling than generic Python exceptions.

Exception Hierarchy:
    NauticalError (base)
    ├── DataError
    │   ├── InvalidBuoyDataError
    │   │   ├── InvalidWindDataError
    │   │   ├── InvalidLocationDataError
    │   │   └── InvalidTimeDataError
    │   ├── InvalidSourceDataError
    │   └── ParsingError
    │       ├── CDataParsingError
    │       └── JSONParsingError
    ├── ConversionError
    │   ├── InvalidUnitsError
    │   ├── UnitMismatchError
    │   └── UnsupportedConversionError
    ├── NetworkError
    │   ├── BuoyNotFoundError
    │   ├── NOAAServiceError
    │   └── NetworkTimeoutError
    ├── CacheError
    │   ├── CacheNotFoundError
    │   ├── CacheWriteError
    │   └── CacheReadError
    └── LocationError
        ├── InvalidCoordinatesError
        ├── OutOfBoundsError
        └── DistanceCalculationError
"""


class NauticalError(Exception):
    """Base exception for all nautical package errors.

    All custom exceptions in the nautical package inherit from this class,
    allowing users to catch all nautical-specific errors with a single except clause.
    """

    pass


# =============================================================================
# Data Errors - Issues with buoy data, sources, or parsing
# =============================================================================


class DataError(NauticalError):
    """Base exception for data validation and parsing errors."""

    pass


class InvalidBuoyDataError(DataError, ValueError):
    """Raised when buoy data is invalid or cannot be parsed.

    This exception inherits from ValueError for backward compatibility.

    Attributes:
        station: The buoy station ID (if available)
        field: The specific field that caused the error (if applicable)
    """

    def __init__(self, message, station=None, field=None):
        super().__init__(message)
        self.station = station
        self.field = field


class InvalidWindDataError(InvalidBuoyDataError):
    """Raised when wind data cannot be parsed or is invalid.

    Examples:
        - Missing wind speed value
        - Invalid wind direction format
        - Gust data in unexpected format
    """

    pass


class InvalidLocationDataError(InvalidBuoyDataError):
    """Raised when location/coordinate data is invalid.

    Examples:
        - Missing latitude or longitude
        - Invalid coordinate format
        - Coordinates with wrong sign indicators
    """

    pass


class InvalidTimeDataError(InvalidBuoyDataError):
    """Raised when time/date data cannot be parsed.

    Examples:
        - Malformed timestamp
        - Missing date components
        - Invalid time format
    """

    pass


class InvalidSourceDataError(DataError, ValueError):
    """Raised when source data is invalid or cannot be parsed.

    Attributes:
        source_name: Name of the source (if available)
    """

    def __init__(self, message, source_name=None):
        super().__init__(message)
        self.source_name = source_name


class ParsingError(DataError):
    """Base exception for parsing failures."""

    pass


class CDataParsingError(ParsingError):
    """Raised when CDATA (HTML comment data) cannot be parsed.

    Attributes:
        raw_data: The raw CDATA that failed to parse (truncated if too long)
    """

    def __init__(self, message, raw_data=None):
        super().__init__(message)
        # Truncate raw_data if it's too long to avoid huge error messages
        if raw_data and len(str(raw_data)) > 200:
            self.raw_data = str(raw_data)[:200] + "..."
        else:
            self.raw_data = raw_data


class JSONParsingError(ParsingError, ValueError):
    """Raised when JSON data cannot be parsed.

    This exception inherits from ValueError for backward compatibility with
    json.loads() error handling patterns.
    """

    pass


# =============================================================================
# Conversion Errors - Issues with unit conversions
# =============================================================================


class ConversionError(NauticalError):
    """Base exception for unit conversion errors."""

    pass


class InvalidUnitsError(ConversionError, KeyError):
    """Raised when an unknown or invalid unit type is used.

    This exception inherits from KeyError for backward compatibility.

    Attributes:
        unit: The invalid unit that was provided
        valid_units: List of valid units for the given type (if available)
    """

    def __init__(self, message, unit=None, valid_units=None):
        super().__init__(message)
        self.unit = unit
        self.valid_units = valid_units


class UnitMismatchError(ConversionError, TypeError):
    """Raised when trying to convert between incompatible unit types.

    For example, trying to convert temperature units to distance units.

    This exception inherits from TypeError for backward compatibility.

    Attributes:
        from_unit: The source unit type
        to_unit: The target unit type
    """

    def __init__(self, message, from_unit=None, to_unit=None):
        super().__init__(message)
        self.from_unit = from_unit
        self.to_unit = to_unit


class UnsupportedConversionError(ConversionError):
    """Raised when a conversion is not supported.

    This is different from UnitMismatchError - the units may be compatible types,
    but the specific conversion is not implemented.
    """

    pass


# =============================================================================
# Network Errors - Issues with web scraping and NOAA API access
# =============================================================================


class NetworkError(NauticalError):
    """Base exception for network and web scraping errors."""

    pass


class BuoyNotFoundError(NetworkError, ValueError):
    """Raised when a buoy station cannot be found.

    This typically occurs when an invalid buoy ID is provided or when
    NOAA doesn't have data for the requested station.

    Attributes:
        station: The buoy station ID that was not found
        url: The URL that was attempted (if available)
    """

    def __init__(self, message, station=None, url=None):
        super().__init__(message)
        self.station = station
        self.url = url


class NOAAServiceError(NetworkError):
    """Raised when the NOAA service is unavailable or returns an error.

    Attributes:
        url: The URL that failed
        status_code: HTTP status code (if available)
        original_error: The underlying exception
    """

    def __init__(self, message, url=None, status_code=None, original_error=None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.original_error = original_error


class NetworkTimeoutError(NetworkError):
    """Raised when a network request times out.

    Attributes:
        url: The URL that timed out
        timeout: The timeout value in seconds
    """

    def __init__(self, message, url=None, timeout=None):
        super().__init__(message)
        self.url = url
        self.timeout = timeout


# =============================================================================
# Cache Errors - Issues with cache file operations
# =============================================================================


class CacheError(NauticalError):
    """Base exception for cache-related errors."""

    pass


class CacheNotFoundError(CacheError, FileNotFoundError):
    """Raised when a cache file cannot be found.

    This exception inherits from FileNotFoundError for backward compatibility.

    Attributes:
        cache_path: The path to the cache file that was not found
    """

    def __init__(self, message, cache_path=None):
        super().__init__(message)
        self.cache_path = cache_path


class CacheWriteError(CacheError, IOError):
    """Raised when a cache file cannot be written.

    Attributes:
        cache_path: The path to the cache file
        original_error: The underlying exception
    """

    def __init__(self, message, cache_path=None, original_error=None):
        super().__init__(message)
        self.cache_path = cache_path
        self.original_error = original_error


class CacheReadError(CacheError, IOError):
    """Raised when a cache file cannot be read or parsed.

    Attributes:
        cache_path: The path to the cache file
        original_error: The underlying exception
    """

    def __init__(self, message, cache_path=None, original_error=None):
        super().__init__(message)
        self.cache_path = cache_path
        self.original_error = original_error


# =============================================================================
# Location Errors - Issues with geographic coordinates and calculations
# =============================================================================


class LocationError(NauticalError):
    """Base exception for location and coordinate errors."""

    pass


class InvalidCoordinatesError(LocationError, ValueError):
    """Raised when coordinates are malformed or invalid.

    This exception inherits from ValueError for backward compatibility.

    Attributes:
        coordinates: The invalid coordinate string or tuple
    """

    def __init__(self, message, coordinates=None):
        super().__init__(message)
        self.coordinates = coordinates


class OutOfBoundsError(LocationError, ValueError):
    """Raised when coordinates are outside valid ranges.

    Valid ranges:
        - Latitude: -90 to +90 degrees
        - Longitude: -180 to +180 degrees

    Attributes:
        latitude: The latitude value (if applicable)
        longitude: The longitude value (if applicable)
        value: The out-of-bounds value
        bounds: The valid bounds as a tuple (min, max)
    """

    def __init__(self, message, latitude=None, longitude=None, value=None, bounds=None):
        super().__init__(message)
        self.latitude = latitude
        self.longitude = longitude
        self.value = value
        self.bounds = bounds


class DistanceCalculationError(LocationError):
    """Raised when distance calculation fails.

    This typically occurs in Haversine distance calculations when
    invalid coordinates are provided.

    Attributes:
        point1: The first point
        point2: The second point
        original_error: The underlying exception
    """

    def __init__(self, message, point1=None, point2=None, original_error=None):
        super().__init__(message)
        self.point1 = point1
        self.point2 = point2
        self.original_error = original_error
