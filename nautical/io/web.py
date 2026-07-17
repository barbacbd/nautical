from __future__ import annotations

from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from nautical.io.retry import RetryConfig, with_retry
from nautical.log import get_logger

log = get_logger(__name__)


def get_noaa_forecast_url(buoy: str) -> str | None:
    """NOAA is kind enough to post all of their data from their buoys at
    the same url ONLY requiring the id of buoy to change at the end of the link
    (https://www.ndbc.noaa.gov/station_page.php?station=).
    This function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    :param buoy: id of the buoy
    :return: full url if buoy is not empty, otherwise None
    """
    if buoy:
        return f"https://www.ndbc.noaa.gov/station_page.php?station={buoy}"
    log.warning("No buoy ID provided to get_noaa_forecast_url")


@with_retry(RetryConfig(max_retries=3, initial_delay=1.0))
def get_url_source(url_name: str) -> BeautifulSoup:
    """Fetch and parse NOAA buoy data webpage with automatic retry and rate limiting.

    The function automatically retries on network errors, timeouts, and server errors
    (5xx status codes). Rate limiting (HTTP 429) is detected and respected via the
    Retry-After header. Client errors (4xx except 429) are not retried.

    :param url_name: URL to fetch
    :return: BeautifulSoup object containing the parsed HTML
    :raises HTTPError: If the request fails after all retries
    :raises URLError: If there's a network-level error after all retries
    :raises ValueError: If url_name is invalid
    """
    try:
        open_url = urlopen(url_name, timeout=30)
        soup = BeautifulSoup(open_url.read(), features="lxml")
        return soup
    except (AttributeError, TypeError, ValueError, HTTPError) as error:
        log.error(error)
        raise
