from urllib.request import urlopen
from urllib.error import URLError
from pykml import parser
from nautical.noaa.buoy.buoy import Buoy
from nautical.noaa.buoy.source import Source
from nautical.location.point import Point


# The known public link to all NOAA Buoys
_KML_LINK = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"


def get_buoy_sources():
    '''NOAA is kind enough to provide all of names, ids, and other information about ALL
    of their known buoys in a kml document hosted at the link provided 
    (https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml). Read through this document and 
    parse the buoy information to determine their id and location. The ID can be used to 
    provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys.

    .. note:: The SHIP ID is not available for lookup.

    :return: dictionary all source names mapped to their respective source.
    '''
    sources = {}

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

            source = Source(category.name.text, category.description)

            for placemark in category.Placemark:

                pnt = Point()
                pnt.parse(str(placemark.Point.coordinates))
                buoy = Buoy(placemark.name.text, description=placemark.Snippet, location=pnt)

                source.add_buoy(buoy)

            sources[source.name] = source

    return sources
