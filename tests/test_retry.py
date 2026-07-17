"""
Tests for retry logic and rate limiting.
"""

import time
from socket import timeout as SocketTimeout
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

import pytest

from nautical.io.retry import (
    AGGRESSIVE_RETRY,
    CONSERVATIVE_RETRY,
    NO_RETRY,
    RateLimiter,
    RetryConfig,
    get_retry_delay,
    retry_request,
    should_retry,
    with_retry,
)


class TestRetryConfig:
    """Test RetryConfig configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.initial_delay == 1.0
        assert config.max_delay == 60.0
        assert config.backoff_factor == 2.0
        assert config.respect_retry_after is True
        assert 429 in config.retry_on_status
        assert 500 in config.retry_on_status
        assert 503 in config.retry_on_status

    def test_custom_config(self):
        """Test custom configuration."""
        config = RetryConfig(max_retries=5, initial_delay=2.0, retry_on_status=[429, 503])
        assert config.max_retries == 5
        assert config.initial_delay == 2.0
        assert config.retry_on_status == {429, 503}

    def test_preset_configs(self):
        """Test preset configurations exist."""
        assert CONSERVATIVE_RETRY.max_retries == 3
        assert AGGRESSIVE_RETRY.max_retries == 5
        assert NO_RETRY.max_retries == 0


class TestRateLimiter:
    """Test RateLimiter functionality."""

    def test_rate_limiter_basic(self):
        """Test basic rate limiting."""
        limiter = RateLimiter(requests_per_window=2, window_seconds=1)

        start = time.time()

        # First two requests should be fast
        limiter.acquire()
        limiter.acquire()

        # Third request should wait
        limiter.acquire()

        elapsed = time.time() - start

        # Should take at least 1 second total (2 requests at 0.5s each)
        assert elapsed >= 1.0, f"Rate limiter didn't delay enough: {elapsed}s"

    def test_rate_limiter_allows_burst(self):
        """Test that rate limiter allows initial burst."""
        limiter = RateLimiter(requests_per_window=5, window_seconds=1)

        start = time.time()

        # First request should be immediate
        limiter.acquire()

        elapsed = time.time() - start

        # Should be very fast (< 0.5s)
        assert elapsed < 0.5, f"First request was delayed: {elapsed}s"

    def test_rate_limiter_refills_tokens(self):
        """Test that rate limiter refills tokens over time."""
        limiter = RateLimiter(requests_per_window=10, window_seconds=1)

        # Use all tokens
        for _ in range(10):
            limiter.acquire()

        # Wait for refill
        time.sleep(0.5)

        start = time.time()
        # Should have ~5 tokens refilled
        limiter.acquire()
        elapsed = time.time() - start

        # Should not wait long since tokens refilled
        assert elapsed < 0.3, f"Token refill didn't work: {elapsed}s"


class TestRetryDelay:
    """Test retry delay calculation."""

    def test_exponential_backoff(self):
        """Test exponential backoff increases delay."""
        config = RetryConfig(initial_delay=1.0, backoff_factor=2.0, max_delay=100.0)

        delay0 = get_retry_delay(0, config)
        delay1 = get_retry_delay(1, config)
        delay2 = get_retry_delay(2, config)

        # Each delay should be roughly double (with jitter)
        assert 0.8 <= delay0 <= 1.2  # ~1s ±20%
        assert 1.6 <= delay1 <= 2.4  # ~2s ±20%
        assert 3.2 <= delay2 <= 4.8  # ~4s ±20%

    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay."""
        config = RetryConfig(initial_delay=10.0, backoff_factor=2.0, max_delay=15.0)

        # Large attempt number should still be capped
        delay = get_retry_delay(10, config)

        assert delay <= 15.0, f"Delay exceeded max: {delay}s"

    def test_retry_after_header(self):
        """Test respecting Retry-After header."""
        config = RetryConfig(initial_delay=1.0, max_delay=100.0, respect_retry_after=True)

        delay = get_retry_delay(0, config, retry_after="30")

        assert delay == 30.0, f"Didn't respect Retry-After: {delay}s"

    def test_retry_after_respects_max_delay(self):
        """Test that Retry-After is still capped by max_delay."""
        config = RetryConfig(initial_delay=1.0, max_delay=10.0, respect_retry_after=True)

        delay = get_retry_delay(0, config, retry_after="100")

        assert delay == 10.0, f"Retry-After wasn't capped: {delay}s"

    def test_ignore_retry_after_when_disabled(self):
        """Test ignoring Retry-After when respect_retry_after=False."""
        config = RetryConfig(initial_delay=1.0, respect_retry_after=False)

        delay = get_retry_delay(0, config, retry_after="30")

        # Should use exponential backoff, not Retry-After
        assert delay < 2.0, f"Used Retry-After when disabled: {delay}s"


class TestShouldRetry:
    """Test retry decision logic."""

    def test_retry_on_timeout(self):
        """Test that socket timeout triggers retry."""
        config = RetryConfig()
        error = SocketTimeout("Connection timed out")

        should, retry_after = should_retry(error, config)

        assert should is True
        assert retry_after is None

    def test_retry_on_url_error(self):
        """Test that URLError triggers retry."""
        config = RetryConfig()
        error = URLError("Network unreachable")

        should, retry_after = should_retry(error, config)

        assert should is True

    def test_retry_on_429(self):
        """Test that HTTP 429 (Rate Limit) triggers retry."""
        config = RetryConfig()

        # Create mock HTTPError
        fp = Mock()
        error = HTTPError("http://test.com", 429, "Too Many Requests", {}, fp)

        should, retry_after = should_retry(error, config)

        assert should is True

    def test_retry_on_500(self):
        """Test that HTTP 500 triggers retry."""
        config = RetryConfig()

        fp = Mock()
        error = HTTPError("http://test.com", 500, "Internal Server Error", {}, fp)

        should, retry_after = should_retry(error, config)

        assert should is True

    def test_no_retry_on_404(self):
        """Test that HTTP 404 does not trigger retry."""
        config = RetryConfig()

        fp = Mock()
        error = HTTPError("http://test.com", 404, "Not Found", {}, fp)

        should, retry_after = should_retry(error, config)

        assert should is False

    def test_no_retry_on_400(self):
        """Test that HTTP 400 does not trigger retry."""
        config = RetryConfig()

        fp = Mock()
        error = HTTPError("http://test.com", 400, "Bad Request", {}, fp)

        should, retry_after = should_retry(error, config)

        assert should is False

    def test_extract_retry_after_header(self):
        """Test extracting Retry-After header from HTTP 429."""
        config = RetryConfig()

        fp = Mock()
        headers = {"Retry-After": "60"}
        error = HTTPError("http://test.com", 429, "Too Many Requests", headers, fp)

        should, retry_after = should_retry(error, config)

        assert should is True
        assert retry_after == "60"


class TestWithRetryDecorator:
    """Test the @with_retry decorator."""

    def test_successful_request_no_retry(self):
        """Test that successful requests don't retry."""
        call_count = [0]

        @with_retry(RetryConfig(max_retries=3), rate_limiter=None)
        def mock_request():
            call_count[0] += 1
            return "success"

        result = mock_request()

        assert result == "success"
        assert call_count[0] == 1, "Should only call once on success"

    def test_retry_on_transient_error(self):
        """Test retrying on transient errors."""
        call_count = [0]

        @with_retry(RetryConfig(max_retries=3, initial_delay=0.01), rate_limiter=None)
        def mock_request():
            call_count[0] += 1
            if call_count[0] < 3:
                fp = Mock()
                raise HTTPError("http://test.com", 500, "Server Error", {}, fp)
            return "success"

        result = mock_request()

        assert result == "success"
        assert call_count[0] == 3, "Should retry and eventually succeed"

    def test_max_retries_exceeded(self):
        """Test that max retries is respected."""
        call_count = [0]

        @with_retry(RetryConfig(max_retries=2, initial_delay=0.01), rate_limiter=None)
        def mock_request():
            call_count[0] += 1
            fp = Mock()
            raise HTTPError("http://test.com", 500, "Server Error", {}, fp)

        with pytest.raises(HTTPError):
            mock_request()

        # Initial attempt + 2 retries = 3 total calls
        assert call_count[0] == 3

    def test_no_retry_on_client_error(self):
        """Test that client errors (4xx) are not retried."""
        call_count = [0]

        @with_retry(RetryConfig(max_retries=3, initial_delay=0.01), rate_limiter=None)
        def mock_request():
            call_count[0] += 1
            fp = Mock()
            raise HTTPError("http://test.com", 404, "Not Found", {}, fp)

        with pytest.raises(HTTPError) as exc_info:
            mock_request()

        assert exc_info.value.code == 404
        assert call_count[0] == 1, "Should not retry on 404"

    def test_rate_limiter_integration(self):
        """Test that rate limiter is called."""
        limiter = RateLimiter(requests_per_window=100, window_seconds=1)
        call_count = [0]

        @with_retry(RetryConfig(max_retries=0), rate_limiter=limiter)
        def mock_request():
            call_count[0] += 1
            return "success"

        # Should succeed and use rate limiter
        result = mock_request()

        assert result == "success"
        assert call_count[0] == 1


class TestRetryRequestFunction:
    """Test the retry_request function."""

    def test_retry_request_success(self):
        """Test retry_request with successful function."""

        def mock_func(value):
            return value * 2

        result = retry_request(mock_func, config=NO_RETRY, rate_limiter=None, value=5)

        assert result == 10

    def test_retry_request_with_retries(self):
        """Test retry_request with retrying function."""
        call_count = [0]

        def mock_func():
            call_count[0] += 1
            if call_count[0] < 2:
                fp = Mock()
                raise HTTPError("http://test.com", 503, "Service Unavailable", {}, fp)
            return "success"

        result = retry_request(
            mock_func, config=RetryConfig(max_retries=3, initial_delay=0.01), rate_limiter=None
        )

        assert result == "success"
        assert call_count[0] == 2


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_max_retries(self):
        """Test with max_retries=0."""
        call_count = [0]

        @with_retry(RetryConfig(max_retries=0), rate_limiter=None)
        def mock_request():
            call_count[0] += 1
            fp = Mock()
            raise HTTPError("http://test.com", 500, "Error", {}, fp)

        with pytest.raises(HTTPError):
            mock_request()

        assert call_count[0] == 1, "Should not retry with max_retries=0"

    def test_very_large_retry_after(self):
        """Test handling of very large Retry-After values."""
        config = RetryConfig(initial_delay=1.0, max_delay=10.0)

        delay = get_retry_delay(0, config, retry_after="999999")

        # Should be capped at max_delay
        assert delay == 10.0
