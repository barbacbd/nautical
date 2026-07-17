# Custom Exception Hierarchy for Nautical

## Current State
The codebase currently uses generic Python exceptions (`ValueError`, `TypeError`, `KeyError`, `AttributeError`, `IndexError`, `HTTPError`, `URLError`) which makes it difficult to:
- Distinguish between different types of nautical-specific errors
- Provide meaningful error messages to users
- Handle errors appropriately at different levels
- Recover from specific error conditions

## Proposed Exception Hierarchy

```
NauticalError (base exception)
├── DataError (data parsing/validation errors)
│   ├── InvalidBuoyDataError
│   │   ├── InvalidWindDataError
│   │   ├── InvalidLocationDataError
│   │   └── InvalidTimeDataError
│   ├── InvalidSourceDataError
│   └── ParsingError
│       ├── CDataParsingError
│       └── JSONParsingError
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

## Implementation Plan

### 1. Create `nautical/exceptions.py`
Define all custom exception classes with helpful docstrings and optional context.

### 2. Update Exception Usage by Module

#### `nautical/io/web.py`
- **Current**: Catches `(AttributeError, TypeError, ValueError, HTTPError)` and re-raises
- **Proposed**:
  - Wrap in `NOAAServiceError` with URL and error details
  - Use `BuoyNotFoundError` for 404 responses
  - Use `NetworkTimeoutError` for timeout scenarios

#### `nautical/io/cdata.py`
- **Current**: Catches `ValueError`, `TypeError`, `IndexError` and logs
- **Proposed**:
  - `InvalidWindDataError` for wind parsing failures (lines 32)
  - `InvalidLocationDataError` for location parsing failures (lines 80)
  - `InvalidTimeDataError` for time parsing failures
  - `CDataParsingError` as catch-all for unparseable CDATA

#### `nautical/io/buoy.py`
- **Current**: Catches `(IndexError, TypeError, AttributeError)` and logs
- **Proposed**:
  - `InvalidBuoyDataError` for buoy data validation failures
  - `ParsingError` for HTML table parsing issues

#### `nautical/units/conversion.py`
- **Current**: Raises bare `KeyError` and `TypeError`
- **Proposed**:
  - `InvalidUnitsError` when units are not recognized (lines 61, 77, 92, 109, 126)
  - `UnitMismatchError` when trying to convert incompatible units (line 158)
  - Include source/target units in error message

#### `nautical/cache/file.py`
- **Current**: Propagates OS/IO errors without context
- **Proposed**:
  - `CacheNotFoundError` for missing cache files
  - `CacheWriteError` for write failures with file path
  - `CacheReadError` for read/parse failures with file path

#### `nautical/location/point.py`
- **Current**: Catches `TypeError`, logs and continues
- **Proposed**:
  - `InvalidCoordinatesError` for malformed coordinate strings
  - `OutOfBoundsError` for lat/lon out of valid ranges
  - `DistanceCalculationError` for Haversine failures

#### `nautical/time/conversion.py`
- **Current**: Catches `IndexError`, `ValueError`
- **Proposed**:
  - `InvalidTimeDataError` for unparseable time strings
  - Include original input in error message

### 3. Exception Context
Each exception should include:
- Clear error message describing what went wrong
- Original data that caused the error (when safe/relevant)
- Suggestions for fixing (when applicable)
- Chain the original exception using `raise ... from original_error`

### 4. Error Recovery Patterns

**Silent Failures → Explicit Failures**
```python
# BEFORE
try:
    value = float(data)
except ValueError:
    log.error("bad value")
    value = None  # silent failure

# AFTER
try:
    value = float(data)
except ValueError as e:
    raise InvalidBuoyDataError(
        f"Expected numeric value, got: {data!r}"
    ) from e
```

**Catch and Re-raise with Context**
```python
# BEFORE
except KeyError as key_error:
    log.error(key_error)
    raise

# AFTER
except KeyError as e:
    raise InvalidUnitsError(
        f"Unknown unit type: {init_units}. "
        f"Valid units: {list(TimeLookup.keys())}"
    ) from e
```

### 5. Backward Compatibility
To maintain backward compatibility during transition:
- Make custom exceptions inherit from the original exception types where appropriate
  - `InvalidUnitsError(ValueError, NauticalError)`
  - `InvalidCoordinatesError(ValueError, NauticalError)`
- This allows existing except clauses to still catch them

### 6. Documentation
- Update docstrings to document which exceptions can be raised
- Add examples in documentation showing how to handle specific errors
- Create troubleshooting guide for common error scenarios

## Benefits

1. **Better Debugging**: Stack traces immediately identify nautical-specific issues
2. **Targeted Error Handling**: Callers can catch specific errors (e.g., retry on `NetworkTimeoutError`)
3. **Clearer Error Messages**: Context-rich messages help users fix issues
4. **Type Safety**: IDEs can provide better autocomplete and warnings
5. **API Clarity**: Function signatures clearly document failure modes
6. **Testing**: Easier to test specific error conditions

## Example Usage

```python
from nautical.exceptions import BuoyNotFoundError, NetworkTimeoutError
from nautical.io import create_buoy

try:
    buoy = create_buoy("INVALID_ID")
except BuoyNotFoundError as e:
    print(f"Buoy not available: {e}")
    # Try alternative data source
except NetworkTimeoutError as e:
    print(f"NOAA service timeout: {e}")
    # Retry with exponential backoff
except NauticalError as e:
    print(f"Unexpected nautical error: {e}")
    # Log and fail gracefully
```

## Migration Strategy

1. **Phase 1**: Create exception classes (non-breaking)
2. **Phase 2**: Update one module at a time, starting with most critical (e.g., `units/conversion.py`)
3. **Phase 3**: Update tests to verify new exceptions
4. **Phase 4**: Update documentation with examples
5. **Phase 5**: Deprecate old patterns in future major version

## Testing Considerations

- Add tests for each exception type
- Verify exception messages are helpful
- Test exception chaining preserves original traceback
- Ensure backward compatibility where claimed
