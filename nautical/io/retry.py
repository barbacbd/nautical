"""
Retry logic and rate limiting for web requests.

This module provides intelligent retry mechanisms with exponential backoff,
rate limit detection, and respect for HTTP Retry-After headers.
"""

import time
from functools import wraps
from socket import timeout as SocketTimeout
from urllib.error import HTTPError, URLError

from nautical.log import get_logger

log = get_logger()


class RetryConfig:
    """Configuration for retry behavior.

    Attributes:
        max_retries: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds before first retry (default: 1.0)
        max_delay: Maximum delay between retries in seconds (default: 60.0)
        backoff_factor: Multiplier for exponential backoff (default: 2.0)
        retry_on_status: HTTP status codes that should trigger retry (default: 429, 500-599)
        respect_retry_after: Whether to respect HTTP Retry-After header (default: True)
    """

    def __init__(
        self,
        max_retries=3,
        initial_delay=1.0,
        max_delay=60.0,
        backoff_factor=2.0,
        retry_on_status=None,
        respect_retry_after=True,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.respect_retry_after = respect_retry_after

        # Default to retrying on rate limit (429) and server errors (5xx)
        if retry_on_status is None:
            self.retry_on_status = {429} | set(range(500, 600))
        else:
            self.retry_on_status = set(retry_on_status)


class RateLimiter:
    """Simple rate limiter to prevent overwhelming the server.

    Uses a token bucket algorithm to limit requests per time window.

    Attributes:
        requests_per_window: Number of requests allowed per time window
        window_seconds: Time window in seconds (default: 60)
    """

    def __init__(self, requests_per_window=30, window_seconds=60):
        """Initialize rate limiter.

        Args:
            requests_per_window: Max requests allowed in the time window
            window_seconds: Length of the time window in seconds
        """
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.tokens = requests_per_window
        self.last_update = time.time()
        self.min_interval = window_seconds / requests_per_window

    def acquire(self):
        """Acquire a token, blocking if necessary.

        This method will sleep if no tokens are available, waiting until
        a token becomes available.
        """
        now = time.time()
        time_passed = now - self.last_update

        # Refill tokens based on time passed
        self.tokens = min(
            self.requests_per_window,
            self.tokens + (time_passed * self.requests_per_window / self.window_seconds),
        )
        self.last_update = now

        if self.tokens < 1:
            # Need to wait for a token
            sleep_time = (1 - self.tokens) * self.window_seconds / self.requests_per_window
            log.debug(f"Rate limit: sleeping {sleep_time:.2f}s for token")
            time.sleep(sleep_time)
            self.tokens = 1
            self.last_update = time.time()

        # Consume a token
        self.tokens -= 1

        # Ensure minimum interval between requests
        time.sleep(self.min_interval)


# Global rate limiter for NOAA requests
# NOAA doesn't publish rate limits, but we use conservative values
# 30 requests per minute = 0.5 requests/second
_global_rate_limiter = RateLimiter(requests_per_window=30, window_seconds=60)


def get_retry_delay(attempt, config, retry_after=None):
    """Calculate delay before next retry attempt.

    Args:
        attempt: Current attempt number (0-indexed)
        config: RetryConfig instance
        retry_after: Value from Retry-After header (seconds or datetime string)

    Returns:
        Delay in seconds before next retry
    """
    # If server provided Retry-After header, respect it
    if retry_after is not None and config.respect_retry_after:
        try:
            # Retry-After can be seconds or HTTP-date
            delay = int(retry_after)
            log.info(f"Server requested retry after {delay}s")
            return min(delay, config.max_delay)
        except ValueError:
            # HTTP-date format - would need to parse, but just use default
            log.warning(f"Could not parse Retry-After header: {retry_after}")

    # Exponential backoff: initial_delay * (backoff_factor ^ attempt)
    delay = config.initial_delay * (config.backoff_factor**attempt)

    # Cap at max_delay
    delay = min(delay, config.max_delay)

    # Add jitter (random ±20%) to avoid thundering herd
    import random

    jitter = delay * 0.2 * (random.random() * 2 - 1)  # -20% to +20%
    delay = max(0, delay + jitter)

    return min(delay, config.max_delay)


def should_retry(error, config):
    """Determine if an error should trigger a retry.

    Args:
        error: Exception that was raised
        config: RetryConfig instance

    Returns:
        tuple: (should_retry: bool, retry_after: str|None)
    """
    # HTTP errors - check status code (must come before URLError since HTTPError is a subclass)
    if isinstance(error, HTTPError):
        # Extract Retry-After header if present
        retry_after = None
        if hasattr(error, "headers") and error.headers:
            retry_after = error.headers.get("Retry-After")

        # 429 (Too Many Requests) should always be retried
        if error.code == 429:
            log.warning(f"Rate limited (HTTP 429)")
            return True, retry_after

        # Check if status code is in retry list
        if error.code in config.retry_on_status:
            log.warning(f"Retryable HTTP error: {error.code}")
            return True, retry_after

        # Don't retry client errors (4xx except 429)
        if 400 <= error.code < 500:
            log.info(f"Client error {error.code}, not retrying")
            return False, None

    # Network timeouts and connection errors should be retried
    if isinstance(error, (SocketTimeout, URLError)):
        return True, None

    # Unknown error - don't retry
    return False, None


def with_retry(config=None, rate_limiter=None):
    """Decorator to add retry logic to a function.

    Args:
        config: RetryConfig instance, or None for defaults
        rate_limiter: RateLimiter instance, or None to use global limiter

    Example:
        @with_retry(RetryConfig(max_retries=5))
        def fetch_data(url):
            return urlopen(url)
    """
    if config is None:
        config = RetryConfig()

    if rate_limiter is None:
        rate_limiter = _global_rate_limiter

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(config.max_retries + 1):
                try:
                    # Acquire rate limit token before request
                    if rate_limiter:
                        rate_limiter.acquire()

                    # Attempt the request
                    return func(*args, **kwargs)

                except Exception as e:
                    last_error = e

                    # Check if we should retry
                    retry, retry_after = should_retry(e, config)

                    if not retry or attempt >= config.max_retries:
                        # Don't retry, or out of retries
                        log.error(f"Request failed after {attempt + 1} attempts: {e}")
                        raise

                    # Calculate delay
                    delay = get_retry_delay(attempt, config, retry_after)

                    log.info(
                        f"Retry {attempt + 1}/{config.max_retries} "
                        f"after {delay:.1f}s: {type(e).__name__}"
                    )

                    time.sleep(delay)

            # Should never reach here, but just in case
            if last_error:
                raise last_error

        return wrapper

    return decorator


def retry_request(func, config=None, rate_limiter=None, *args, **kwargs):
    """Retry a function call with retry logic.

    Alternative to decorator when you can't use @with_retry.

    Args:
        func: Function to call
        config: RetryConfig instance
        rate_limiter: RateLimiter instance
        *args, **kwargs: Arguments to pass to func

    Returns:
        Result of func(*args, **kwargs)

    Example:
        result = retry_request(
            urlopen,
            config=RetryConfig(max_retries=5),
            url="https://example.com"
        )
    """
    if config is None:
        config = RetryConfig()

    if rate_limiter is None:
        rate_limiter = _global_rate_limiter

    # Apply decorator and call
    wrapped = with_retry(config, rate_limiter)(func)
    return wrapped(*args, **kwargs)


# Preset configurations for common scenarios

# Conservative: For sensitive endpoints or when being respectful
CONSERVATIVE_RETRY = RetryConfig(
    max_retries=3, initial_delay=2.0, max_delay=60.0, backoff_factor=2.0
)

# Aggressive: For time-critical requests (use with caution)
AGGRESSIVE_RETRY = RetryConfig(max_retries=5, initial_delay=0.5, max_delay=30.0, backoff_factor=1.5)

# No retry: For testing or when retries are not desired
NO_RETRY = RetryConfig(max_retries=0)
