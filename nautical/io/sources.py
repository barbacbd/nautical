from urllib.request import urlopen
from urllib.error import URLError
from pykml import parser
from nautical.noaa.buoy.buoy import Buoy
from nautical.noaa.buoy.source import Source, SourceType
from nautical.location.point import Point
from nautical.log import get_logger
from .cdata import fill_buoy_with_cdata


# The known public link to all NOAA Buoys
_KML_LINK = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"
log = get_logger()


def get_buoy_sources(source_type=SourceType.ALL):
    '''NOAA is kind enough to provide all of names, ids, and other information about ALL
    of their known buoys in a kml document hosted at the link provided 
    (https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml). Read through this document and 
    parse the buoy information to determine their id and location. The ID can be used to 
    provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys.

    :return: dictionary all source names mapped to their respective source.
    '''
    sources = {}
    valid_source_types = SourceType.as_strings(source_type)

    # remove the unsupported types
    for unsupported_source in (
        SourceType.as_strings(SourceType.TAO), SourceType.as_strings(SourceType.TSUNAMI)
    ):
        if unsupported_source in valid_source_types:
            log.debug("Removing %s, unsupported source type.", unsupported_source)
            valid_source_types.remove(unsupported_source)
    
    try:
        fileobject = urlopen(_KML_LINK)
    except URLError:
        return sources

    root = parser.parse(fileobject).getroot()

    # grab the embedded link that will provide the kml to all buoys
    real_kml = root.Document.NetworkLink.Link.href

    if real_kml:
        real_fileobject = urlopen(str(real_kml))
        real_root = parser.parse(real_fileobject).getroot()

        for category in real_root.Document.Folder.Folder:

            source_name = category.name.text

            if source_name not in valid_source_types:
                log.warning("Found %s, skipping ...", source_name)
                continue
            
            source = Source(source_name, category.description)

            for placemark in category.Placemark:

                pnt = Point()
                pnt.parse(str(placemark.Point.coordinates))
                buoy = Buoy(placemark.name.text, description=placemark.Snippet, location=pnt)

                # These two sources contain buoys with information embedded in CDATA
                if source.name in ("Ships", ):
                    fill_buoy_with_cdata(buoy, placemark.description.text)

                source.add_buoy(buoy)

            sources[source.name] = source

    return sources
