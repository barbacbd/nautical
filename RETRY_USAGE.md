# Retry Logic and Rate Limiting Usage Guide

This guide explains how to use the retry logic and rate limiting features in the nautical package.

## Overview

The `nautical.io.retry` module provides:
- **Automatic retry** on network errors, timeouts, and server errors
- **Exponential backoff** with jitter to avoid thundering herd
- **Rate limiting** to prevent overwhelming NOAA servers
- **Retry-After header support** to respect server-requested delays
- **Configurable behavior** for different use cases

## Quick Start

The retry logic is automatically applied to `get_url_source()`:

```python
from nautical.io.web import get_url_source

# Automatic retry with rate limiting
soup = get_url_source("https://www.ndbc.noaa.gov/station_page.php?station=44099")
```

## Default Behavior

By default, the package:
- Retries up to **3 times** on failures
- Uses **exponential backoff**: 1s, 2s, 4s delays
- **Rate limits** to 30 requests per minute (0.5 req/sec)
- **Respects HTTP 429** (rate limit) responses
- **Retries on**: timeouts, network errors, 5xx server errors
- **Doesn't retry on**: 4xx client errors (except 429)

## Custom Retry Configuration

### Using the Decorator

```python
from nautical.io.retry import with_retry, RetryConfig

# Custom retry configuration
@with_retry(RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,
    backoff_factor=2.0
))
def my_fetch_function(url):
    return urlopen(url)

# Use it
result = my_fetch_function("https://example.com")
```

### Using retry_request Function

```python
from nautical.io.retry import retry_request, RetryConfig
from urllib.request import urlopen

# One-time retry configuration
result = retry_request(
    urlopen,
    config=RetryConfig(max_retries=5),
    url="https://example.com"
)
```

## Retry Configuration Options

```python
RetryConfig(
    max_retries=3,           # Maximum number of retry attempts
    initial_delay=1.0,        # Initial delay in seconds
    max_delay=60.0,          # Maximum delay between retries
    backoff_factor=2.0,      # Exponential backoff multiplier
    retry_on_status=[429, 500, 502, 503, 504],  # HTTP codes to retry
    respect_retry_after=True  # Honor Retry-After header
)
```

## Preset Configurations

### Conservative (Default)

Use for normal operations - respectful and safe:

```python
from nautical.io.retry import with_retry, CONSERVATIVE_RETRY

@with_retry(CONSERVATIVE_RETRY)
def fetch_data(url):
    # ...
```

Settings:
- 3 retries
- 2s initial delay
- 60s max delay
- 2.0x backoff

### Aggressive

Use sparingly for time-critical requests:

```python
from nautical.io.retry import with_retry, AGGRESSIVE_RETRY

@with_retry(AGGRESSIVE_RETRY)
def fetch_urgent_data(url):
    # ...
```

Settings:
- 5 retries
- 0.5s initial delay
- 30s max delay
- 1.5x backoff

**Warning**: Aggressive retry can overwhelm servers. Use only when necessary.

### No Retry

Disable retries for testing or when not desired:

```python
from nautical.io.retry import with_retry, NO_RETRY

@with_retry(NO_RETRY)
def fetch_once(url):
    # ...
```

## Rate Limiting

### Global Rate Limiter

A global rate limiter (30 req/min) is automatically applied to all requests:

```python
from nautical.io.web import get_url_source

# Automatically rate limited
for station in stations:
    soup = get_url_source(f"https://...?station={station}")
    # Rate limiter ensures we don't exceed 30 req/min
```

### Custom Rate Limiter

Create your own rate limiter for specific needs:

```python
from nautical.io.retry import with_retry, RateLimiter, RetryConfig

# More aggressive rate limit: 10 requests per minute
custom_limiter = RateLimiter(requests_per_window=10, window_seconds=60)

@with_retry(RetryConfig(), rate_limiter=custom_limiter)
def fetch_with_custom_rate_limit(url):
    return urlopen(url)
```

### Disable Rate Limiting

```python
@with_retry(RetryConfig(), rate_limiter=None)
def fetch_without_rate_limit(url):
    return urlopen(url)
```

## Handling Rate Limits (HTTP 429)

The package automatically handles HTTP 429 (Too Many Requests):

```python
# Automatic handling of rate limit
try:
    soup = get_url_source("https://...")
except HTTPError as e:
    if e.code == 429:
        # This only happens if all retries are exhausted
        print("Rate limited even after retries")
```

If the server provides a `Retry-After` header, it's automatically respected:

```
HTTP 429
Retry-After: 60

-> Waits 60 seconds before retrying (up to max_delay)
```

## Retry Behavior by Error Type

| Error Type | Retried? | Notes |
|------------|----------|-------|
| Socket timeout | ✅ Yes | Network timeout, likely transient |
| URLError | ✅ Yes | Network unreachable, DNS failure, etc. |
| HTTP 429 | ✅ Yes | Rate limit - respects Retry-After header |
| HTTP 500-599 | ✅ Yes | Server errors, often transient |
| HTTP 400-499 | ❌ No | Client errors (except 429) |
| HTTP 200-399 | ✅ Success | No retry needed |

## Advanced Examples

### Fetch Multiple Buoys with Rate Limiting

```python
from nautical.io.buoy import create_buoy
from nautical.io.retry import with_retry, RetryConfig

def fetch_all_buoys(station_ids):
    """Fetch multiple buoys with automatic retry and rate limiting."""
    buoys = []

    for station_id in station_ids:
        try:
            # create_buoy internally uses get_url_source which has retry
            buoy = create_buoy(station_id)
            if buoy and buoy.valid:
                buoys.append(buoy)
        except Exception as e:
            print(f"Failed to fetch {station_id}: {e}")
            continue

    return buoys

stations = ["44099", "44025", "44013"]
buoys = fetch_all_buoys(stations)
```

### Custom Retry Logic for Specific Endpoints

```python
from nautical.io.retry import with_retry, RetryConfig

# More retries for critical data
critical_config = RetryConfig(
    max_retries=10,
    initial_delay=1.0,
    max_delay=300.0,  # Up to 5 minutes
    backoff_factor=1.5
)

@with_retry(critical_config)
def fetch_critical_buoy(station_id):
    # This endpoint is critical, retry more aggressively
    return urlopen(f"https://...?station={station_id}")
```

### Handling Retry Exhaustion

```python
from nautical.io.web import get_url_source
from urllib.error import HTTPError

def fetch_with_fallback(station_id):
    """Fetch buoy data with fallback to cache."""
    try:
        # Try live data (with automatic retry)
        return get_url_source(f"https://...?station={station_id}")

    except HTTPError as e:
        if e.code == 429:
            print(f"Rate limited for {station_id}, using cache")
        elif 500 <= e.code < 600:
            print(f"Server error for {station_id}, using cache")
        else:
            print(f"Request failed: {e}")

        # Fallback to cache
        return load_from_cache(station_id)
```

### Monitoring Retry Behavior

```python
import logging
from nautical.io.web import get_url_source

# Enable debug logging to see retry behavior
logging.basicConfig(level=logging.DEBUG)

# Will log:
# - Rate limit delays
# - Retry attempts
# - Backoff delays
soup = get_url_source("https://...")
```

## Best Practices

### 1. Use Default Settings for Normal Operations

The default retry config (3 retries, exponential backoff) is appropriate for most use cases:

```python
# Good - uses sensible defaults
from nautical.io.web import get_url_source
soup = get_url_source(url)
```

### 2. Be Conservative with Rate Limits

NOAA doesn't publish official rate limits, so err on the side of caution:

```python
# Good - conservative rate limit
RateLimiter(requests_per_window=30, window_seconds=60)

# Risky - might get rate limited
RateLimiter(requests_per_window=100, window_seconds=60)
```

### 3. Don't Retry Client Errors

The package automatically skips retrying 4xx errors (except 429):

```python
# This is handled automatically - no need to check
try:
    soup = get_url_source(url)
except HTTPError as e:
    if e.code == 404:
        # Not retried - buoy doesn't exist
        pass
```

### 4. Respect Retry-After Headers

Always keep `respect_retry_after=True` (the default):

```python
# Good - respects server guidance
RetryConfig(respect_retry_after=True)

# Bad - ignores server requests
RetryConfig(respect_retry_after=False)
```

### 5. Add Jitter to Avoid Thundering Herd

Jitter is automatically added (±20% randomness):

```python
# Automatic jitter prevents all clients from retrying simultaneously
# Delay: 2s ± 0.4s = 1.6s to 2.4s
```

### 6. Log Retry Attempts for Debugging

```python
import logging
from nautical.log import get_logger

log = get_logger()
log.setLevel(logging.INFO)

# Will show retry attempts and delays
```

## Common Scenarios

### Scenario 1: Bulk Data Collection

```python
from nautical.io.buoy import create_buoy
import time

def collect_buoy_data(station_ids):
    """Collect data from many buoys over time."""
    results = {}

    for station_id in station_ids:
        try:
            # Automatic retry + rate limiting
            buoy = create_buoy(station_id)
            results[station_id] = buoy
        except Exception as e:
            print(f"Skipping {station_id}: {e}")

    return results

# Rate limiter ensures we don't overwhelm the server
stations = ["44099", "44025", "44013", ...]
data = collect_buoy_data(stations)
```

### Scenario 2: Real-time Monitoring

```python
from nautical.io.buoy import fill_buoy
from nautical.io.retry import RetryConfig, with_retry

# Check buoy every 5 minutes
while True:
    try:
        fill_buoy(my_buoy)
        if my_buoy.valid:
            process_data(my_buoy)
    except Exception as e:
        log.error(f"Failed to update buoy: {e}")

    time.sleep(300)  # 5 minutes
```

### Scenario 3: Handling Maintenance Windows

```python
from nautical.io.retry import RetryConfig, with_retry

# During known maintenance, use longer delays
maintenance_config = RetryConfig(
    max_retries=20,
    initial_delay=30.0,   # Start with 30s delay
    max_delay=600.0,      # Up to 10 minutes
    backoff_factor=1.2    # Slow backoff
)

@with_retry(maintenance_config)
def fetch_during_maintenance(url):
    return urlopen(url)
```

## Troubleshooting

### Problem: Still getting rate limited

**Solution**: Reduce rate limit or add delays:

```python
# Reduce to 20 requests per minute
limiter = RateLimiter(requests_per_window=20, window_seconds=60)
```

### Problem: Retries taking too long

**Solution**: Reduce max retries or max delay:

```python
config = RetryConfig(
    max_retries=2,      # Fewer retries
    max_delay=30.0      # Cap at 30s
)
```

### Problem: Not retrying when expected

**Solution**: Check error type and retry_on_status:

```python
# Add custom status codes to retry
config = RetryConfig(
    retry_on_status=[429, 500, 502, 503, 504, 408]  # Added 408 timeout
)
```

## Performance Considerations

### Memory

- Rate limiter uses O(1) memory (token bucket)
- No request history stored

### CPU

- Negligible overhead (<1ms per request)
- Jitter calculation is lightweight

### Network

- Default: ~30 req/min = 0.5 req/sec
- With 100 buoys: ~3.3 minutes to fetch all
- Conservative and respectful to NOAA servers

## Related Documentation

- [Error Handling Guide](user/docs/ErrorHandling.md)
- [Python Tutorials](user/docs/PythonTutorials.md)
- [Exception Hierarchy](nautical/exceptions.py)
