from __future__ import annotations

from copy import copy, deepcopy
from urllib.error import URLError
from urllib.request import urlopen

from pykml import parser

from nautical.cache.file import load_sources, save_sources
from nautical.cache.memory import _sources_cache
from nautical.location.point import Point
from nautical.log import get_logger
from nautical.noaa.buoy.buoy import Buoy
from nautical.noaa.buoy.source import Source, SourceType

from .buoy import fill_buoy
from .cdata import fill_buoy_with_cdata

log = get_logger(__name__)


def get_buoy_sources(
    source_types: SourceType | list[SourceType] = SourceType.ALL, use_cache: bool = True
) -> dict[str, Source]:
    """NOAA is kind enough to provide all of names, ids, and other information about ALL
    of their known buoys in a kml document hosted at the link provided
    (https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml). Read through this document and
    parse the buoy information to determine their id and location. The ID can be used to
    provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys.

    :return: dictionary all source names mapped to their respective source.
    """
    source_lst = source_types
    if not isinstance(source_types, list):
        source_lst = [source_types]

    if SourceType.ALL in source_lst:
        source_lst = [SourceType.as_strings(x) for x in SourceType if x != SourceType.ALL]
    else:
        source_lst = list(set([SourceType.as_strings(x) for x in source_lst]))

    cache_key = ",".join(sorted(source_lst))
    if use_cache:
        cached = _sources_cache.get(cache_key)
        if cached is not None and isinstance(cached, dict):
            return cached

        disk_cached = load_sources()
        if disk_cached is not None:
            filtered = {k: v for k, v in disk_cached.items() if k in source_lst}
            if filtered:
                _sources_cache.set(cache_key, filtered)
                return filtered

    sources = {}

    # remove the unsupported types
    for unsupported_source in (
        SourceType.as_strings(SourceType.TAO),
        SourceType.as_strings(SourceType.TSUNAMI),
    ):
        if unsupported_source in source_lst:
            log.debug("Removing %s, unsupported source type.", unsupported_source)
            source_lst.remove(unsupported_source)

    try:
        # The known public link to all NOAA Buoys
        fileobject = urlopen("https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml", timeout=30)
    except URLError:
        return sources

    root = parser.parse(fileobject).getroot()

    # grab the embedded link that will provide the kml to all buoys
    real_kml = root.Document.NetworkLink.Link.href

    if real_kml:
        try:
            real_fileobject = urlopen(str(real_kml), timeout=30)
        except URLError:
            log.error("Failed to fetch KML from %s", real_kml)
            return sources
        real_root = parser.parse(real_fileobject).getroot()

        for category in real_root.Document.Folder.Folder:
            source_name = category.name.text

            if source_name not in source_lst:
                log.debug("Found %s, skipping ...", source_name)
                continue

            source = Source(source_name, category.description)

            for placemark in category.Placemark:
                pnt = Point.parse(str(placemark.Point.coordinates))
                buoy = Buoy(placemark.name.text, description=placemark.Snippet, location=pnt)

                # These two sources contain buoys with information embedded in CDATA
                if source.name in (SourceType.as_strings(SourceType.SHIPS),):
                    fill_buoy_with_cdata(buoy, placemark.description.text)
                    # These buoys must be marked as True
                    buoy.valid = True

                source.add_buoy(buoy)

            sources[source.name] = source

    if use_cache and sources:
        _sources_cache.set(cache_key, sources)
        try:
            save_sources(sources)
        except OSError:
            log.warning("Failed to write sources to disk cache")

    return sources


def validate_sources(
    source_data: dict[str, Source], remove_invalid: bool = True
) -> dict[str, Source]:
    """This function is presumed to be executed after `get_buoy_sources`.
    The results of the previous function meet the requirements for the
    formatted parameter here. The function will attempt to parse all
    buoys found for each source supplied.

    :param source_data: Dictionary in the format of source_name: source
    :param remove_invalid: when True [default] remove the buoys that are invalid
    :return: New dictionary where the buoys for each source are validated
    """
    validated_source_info = {}

    if not isinstance(source_data, dict):
        return validated_source_info

    for source, source_obj in source_data.items():
        if source == SourceType.as_strings(SourceType.SHIPS):
            log.info("Skipping validity check on Ships")
            validated_source_info[source] = deepcopy(source_obj)
            continue

        copied_source = copy(source_obj)
        for _, buoy_obj in source_obj.buoys.items():
            buoy_copy = copy(buoy_obj)

            if buoy_copy.valid:
                log.debug("Skipping buoy: %s, already validated", buoy_obj.station)
                copied_source.add_buoy(buoy_copy)

            fill_buoy(buoy_copy)

            if not buoy_copy.valid and remove_invalid:
                log.warning("Dropping buoy: %s, invalid data", buoy_obj.station)
            else:
                copied_source.add_buoy(buoy_copy)

        if len(copied_source) == 0:
            log.error("No valid buoys found for %s, removing", source)
        else:
            validated_source_info[source] = copied_source

    return validated_source_info
