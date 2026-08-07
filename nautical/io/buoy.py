from __future__ import annotations

from re import sub

from bs4 import BeautifulSoup

from nautical.cache.file import load_buoy, save_buoy
from nautical.cache.memory import _buoy_cache
from nautical.io.web import get_noaa_forecast_url, get_url_source
from nautical.log import get_logger
from nautical.noaa.buoy.buoy import Buoy
from nautical.noaa.buoy.buoy_data import BuoyData

log = get_logger(__name__)


def create_buoy(buoy: str, use_cache: bool = True) -> Buoy | None:
    """Provide a full workup for a specific buoy. If the buoy is None or it cannot
    be found then the data returned will be considered invalid as None

    :param buoy: id of the buoy to do a workup on
    :param use_cache: when True, check memory and disk caches before fetching
    :return: BuoyWorkup if successful else None
    """
    if not buoy:
        return None

    if use_cache:
        cached = _buoy_cache.get(buoy)
        if cached is not None and isinstance(cached, Buoy) and cached.valid:
            return cached

        disk_cached = load_buoy(buoy)
        if disk_cached is not None and disk_cached.valid:
            _buoy_cache.set(buoy, disk_cached)
            return disk_cached

    buoy_data = Buoy(buoy)
    _fill_buoy_from_network(buoy_data)

    if not buoy_data.valid:
        return None

    if use_cache:
        _buoy_cache.set(buoy, buoy_data)
        try:
            save_buoy(buoy_data)
        except OSError:
            log.warning("Failed to write buoy %s to disk cache", buoy)

    return buoy_data


def fill_buoy(buoy: Buoy, use_cache: bool = True) -> None:
    """Pass in a Buoy object that needs to be filled in with the current data.
    The buoy object will have the validity set if the results were successful

    :param buoy: nautical.noaa.buoy.Buoy object
    :param use_cache: when True, check memory and disk caches before fetching
    """
    if use_cache:
        cached = _buoy_cache.get(buoy.station)
        if cached is not None and isinstance(cached, Buoy) and cached.valid:
            buoy.valid = cached.valid
            buoy.present = cached.present
            return

        disk_cached = load_buoy(buoy.station)
        if disk_cached is not None and disk_cached.valid:
            buoy.valid = disk_cached.valid
            buoy.present = disk_cached.present
            _buoy_cache.set(buoy.station, buoy)
            return

    _fill_buoy_from_network(buoy)

    if use_cache and buoy.valid:
        _buoy_cache.set(buoy.station, buoy)
        try:
            save_buoy(buoy)
        except OSError:
            log.warning("Failed to write buoy %s to disk cache", buoy.station)


def _fill_buoy_from_network(buoy: Buoy) -> None:
    """Fetch buoy data from NOAA and populate the buoy object."""
    url = get_noaa_forecast_url(buoy.station)
    soup = get_url_source(url)

    current_buoy_data = BuoyData()
    buoy_valid = get_current_data(
        soup, current_buoy_data, [f"Conditions at {buoy.station}", "Detailed Wave Summary"]
    )
    buoy.valid = buoy_valid
    buoy.present = current_buoy_data


def get_current_data(soup: BeautifulSoup, buoy: BuoyData, search: str | list[str]) -> bool:
    """Search the beautiful soup object for a TABLE containing the search string. The
    function will grab the data from the table and create a NOAAData object and return the data

    :param soup: beautiful soup object generated from the get_url_source()
    :param buoy: BuoyData object that should be filled with data as this function parses the data.
    :param search: text to search for in the soup object.
    :return: True when data has been found and set
    """
    # keep track of the number of variables that were set, indicates validity
    buoy_variables_set = 0

    if not isinstance(search, list):
        search = [search]

    # Find all tables with a caption that has the text we are searching for
    tables = []
    for caption in soup.find_all("caption"):
        for search_text in search:
            if search_text in caption.get_text():
                tables.append(caption.find_parent("table"))

    for table in tables:
        for i, row in enumerate(table.find_all("tr")):
            key_data = None
            key = None
            value = None

            # the first table is another table and it is no use to use -- skipping
            if i >= 1:
                cells = row.find_all("td")
                if cells:
                    try:
                        key_data = cells[0].text
                        key = key_data[key_data.find("(") + 1 : key_data.find(")")]
                        value = cells[1].next.split()[0]
                        buoy.set(key.lower(), value)
                        buoy_variables_set += 1
                    except (IndexError, TypeError, AttributeError) as error:
                        log.error(
                            "%s - key_field: %s, key: %s, value: %s",
                            error,
                            key_data,
                            key,
                            value,
                        )

    # no variables set indicates errors or invalid buoy
    return buoy_variables_set > 0


# Alias for getting current data, It has the same result
get_buoy_data = get_current_data
