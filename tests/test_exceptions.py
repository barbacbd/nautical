"""
Tests for custom exception hierarchy.

These tests verify that custom exceptions are properly defined,
have the expected inheritance, and maintain backward compatibility.
"""
import pytest
from nautical.exceptions import (
    NauticalError,
    DataError,
    InvalidBuoyDataError,
    InvalidWindDataError,
    InvalidLocationDataError,
    InvalidTimeDataError,
    InvalidSourceDataError,
    ParsingError,
    CDataParsingError,
    JSONParsingError,
    ConversionError,
    InvalidUnitsError,
    UnitMismatchError,
    UnsupportedConversionError,
    NetworkError,
    BuoyNotFoundError,
    NOAAServiceError,
    NetworkTimeoutError,
    CacheError,
    CacheNotFoundError,
    CacheWriteError,
    CacheReadError,
    LocationError,
    InvalidCoordinatesError,
    OutOfBoundsError,
    DistanceCalculationError,
)


class TestExceptionHierarchy:
    """Test exception inheritance structure."""

    def test_base_exception(self):
        """Test that NauticalError is the base exception."""
        assert issubclass(NauticalError, Exception)

    def test_data_errors_inherit_from_nautical_error(self):
        """Test that data errors inherit from NauticalError."""
        assert issubclass(DataError, NauticalError)
        assert issubclass(InvalidBuoyDataError, DataError)
        assert issubclass(InvalidWindDataError, InvalidBuoyDataError)
        assert issubclass(InvalidLocationDataError, InvalidBuoyDataError)
        assert issubclass(InvalidTimeDataError, InvalidBuoyDataError)
        assert issubclass(InvalidSourceDataError, DataError)
        assert issubclass(ParsingError, DataError)
        assert issubclass(CDataParsingError, ParsingError)
        assert issubclass(JSONParsingError, ParsingError)

    def test_conversion_errors_inherit_from_nautical_error(self):
        """Test that conversion errors inherit from NauticalError."""
        assert issubclass(ConversionError, NauticalError)
        assert issubclass(InvalidUnitsError, ConversionError)
        assert issubclass(UnitMismatchError, ConversionError)
        assert issubclass(UnsupportedConversionError, ConversionError)

    def test_network_errors_inherit_from_nautical_error(self):
        """Test that network errors inherit from NauticalError."""
        assert issubclass(NetworkError, NauticalError)
        assert issubclass(BuoyNotFoundError, NetworkError)
        assert issubclass(NOAAServiceError, NetworkError)
        assert issubclass(NetworkTimeoutError, NetworkError)

    def test_cache_errors_inherit_from_nautical_error(self):
        """Test that cache errors inherit from NauticalError."""
        assert issubclass(CacheError, NauticalError)
        assert issubclass(CacheNotFoundError, CacheError)
        assert issubclass(CacheWriteError, CacheError)
        assert issubclass(CacheReadError, CacheError)

    def test_location_errors_inherit_from_nautical_error(self):
        """Test that location errors inherit from NauticalError."""
        assert issubclass(LocationError, NauticalError)
        assert issubclass(InvalidCoordinatesError, LocationError)
        assert issubclass(OutOfBoundsError, LocationError)
        assert issubclass(DistanceCalculationError, LocationError)


class TestBackwardCompatibility:
    """Test that custom exceptions maintain backward compatibility."""

    def test_invalid_units_error_is_key_error(self):
        """Test that InvalidUnitsError can be caught as KeyError."""
        assert issubclass(InvalidUnitsError, KeyError)

        try:
            raise InvalidUnitsError("test")
        except KeyError:
            pass  # Should catch
        else:
            pytest.fail("InvalidUnitsError should be catchable as KeyError")

    def test_unit_mismatch_error_is_type_error(self):
        """Test that UnitMismatchError can be caught as TypeError."""
        assert issubclass(UnitMismatchError, TypeError)

        try:
            raise UnitMismatchError("test")
        except TypeError:
            pass
        else:
            pytest.fail("UnitMismatchError should be catchable as TypeError")

    def test_invalid_buoy_data_is_value_error(self):
        """Test that InvalidBuoyDataError can be caught as ValueError."""
        assert issubclass(InvalidBuoyDataError, ValueError)

    def test_cache_not_found_is_file_not_found(self):
        """Test that CacheNotFoundError can be caught as FileNotFoundError."""
        assert issubclass(CacheNotFoundError, FileNotFoundError)

    def test_cache_io_errors(self):
        """Test that cache I/O errors inherit from IOError."""
        assert issubclass(CacheWriteError, IOError)
        assert issubclass(CacheReadError, IOError)


class TestExceptionAttributes:
    """Test that exceptions properly store attributes."""

    def test_invalid_units_error_attributes(self):
        """Test InvalidUnitsError attributes."""
        exc = InvalidUnitsError(
            "Test message",
            unit="bad_unit",
            valid_units=["unit1", "unit2"]
        )
        assert exc.unit == "bad_unit"
        assert exc.valid_units == ["unit1", "unit2"]
        assert "Test message" in str(exc)

    def test_unit_mismatch_error_attributes(self):
        """Test UnitMismatchError attributes."""
        exc = UnitMismatchError(
            "Type mismatch",
            from_unit="temperature",
            to_unit="distance"
        )
        assert exc.from_unit == "temperature"
        assert exc.to_unit == "distance"

    def test_buoy_not_found_error_attributes(self):
        """Test BuoyNotFoundError attributes."""
        exc = BuoyNotFoundError(
            "Buoy not found",
            station="TEST123",
            url="http://example.com"
        )
        assert exc.station == "TEST123"
        assert exc.url == "http://example.com"

    def test_noaa_service_error_attributes(self):
        """Test NOAAServiceError attributes."""
        original = ValueError("original error")
        exc = NOAAServiceError(
            "Service error",
            url="http://example.com",
            status_code=500,
            original_error=original
        )
        assert exc.url == "http://example.com"
        assert exc.status_code == 500
        assert exc.original_error is original

    def test_out_of_bounds_error_attributes(self):
        """Test OutOfBoundsError attributes."""
        exc = OutOfBoundsError(
            "Latitude out of range",
            latitude=100,
            value=100,
            bounds=(-90, 90)
        )
        assert exc.latitude == 100
        assert exc.value == 100
        assert exc.bounds == (-90, 90)

    def test_cache_error_attributes(self):
        """Test cache error attributes."""
        original = IOError("disk full")
        exc = CacheWriteError(
            "Write failed",
            cache_path="/tmp/cache.json",
            original_error=original
        )
        assert exc.cache_path == "/tmp/cache.json"
        assert exc.original_error is original


class TestExceptionChaining:
    """Test that exceptions properly chain with 'from' clause."""

    def test_exception_can_be_chained(self):
        """Test that exceptions can chain from original errors."""
        original = ValueError("original")

        try:
            try:
                raise original
            except ValueError as e:
                raise InvalidBuoyDataError("wrapped") from e
        except InvalidBuoyDataError as exc:
            assert exc.__cause__ is original

    def test_chained_exception_preserves_traceback(self):
        """Test that chained exceptions preserve the original traceback."""
        try:
            try:
                raise KeyError("original")
            except KeyError as e:
                raise InvalidUnitsError("wrapped", unit="bad") from e
        except InvalidUnitsError as exc:
            assert exc.__cause__ is not None
            assert isinstance(exc.__cause__, KeyError)


class TestCatchingExceptions:
    """Test various ways of catching exceptions."""

    def test_catch_specific_exception(self):
        """Test catching a specific custom exception."""
        with pytest.raises(InvalidWindDataError):
            raise InvalidWindDataError("test")

    def test_catch_base_data_error(self):
        """Test catching any DataError."""
        with pytest.raises(DataError):
            raise InvalidWindDataError("test")

    def test_catch_nautical_error(self):
        """Test catching any NauticalError."""
        with pytest.raises(NauticalError):
            raise DistanceCalculationError("test")

    def test_catch_builtin_type(self):
        """Test catching via backward-compatible builtin type."""
        with pytest.raises(ValueError):
            raise InvalidBuoyDataError("test")

        with pytest.raises(KeyError):
            raise InvalidUnitsError("test")

        with pytest.raises(FileNotFoundError):
            raise CacheNotFoundError("test")


class TestErrorMessages:
    """Test that error messages are descriptive."""

    def test_messages_are_preserved(self):
        """Test that custom messages are preserved."""
        msg = "This is a custom error message"
        exc = InvalidBuoyDataError(msg, station="TEST", field="wspd")

        assert msg in str(exc)
        assert exc.station == "TEST"
        assert exc.field == "wspd"

    def test_cdata_parsing_error_truncates_long_data(self):
        """Test that CDataParsingError truncates long raw data."""
        long_data = "x" * 500
        exc = CDataParsingError("Parse failed", raw_data=long_data)

        # Should be truncated
        assert len(exc.raw_data) < 500
        assert exc.raw_data.endswith("...")

    def test_cdata_parsing_error_keeps_short_data(self):
        """Test that CDataParsingError keeps short raw data."""
        short_data = "short data"
        exc = CDataParsingError("Parse failed", raw_data=short_data)

        assert exc.raw_data == short_data


class TestExceptionDocumentation:
    """Test that exceptions have proper documentation."""

    def test_all_exceptions_have_docstrings(self):
        """Test that all exception classes have docstrings."""
        exceptions = [
            NauticalError, DataError, InvalidBuoyDataError,
            InvalidWindDataError, InvalidLocationDataError,
            InvalidTimeDataError, InvalidSourceDataError,
            ParsingError, CDataParsingError, JSONParsingError,
            ConversionError, InvalidUnitsError, UnitMismatchError,
            UnsupportedConversionError, NetworkError, BuoyNotFoundError,
            NOAAServiceError, NetworkTimeoutError, CacheError,
            CacheNotFoundError, CacheWriteError, CacheReadError,
            LocationError, InvalidCoordinatesError, OutOfBoundsError,
            DistanceCalculationError
        ]

        for exc_class in exceptions:
            assert exc_class.__doc__ is not None, f"{exc_class.__name__} missing docstring"
            assert len(exc_class.__doc__.strip()) > 0, f"{exc_class.__name__} has empty docstring"
