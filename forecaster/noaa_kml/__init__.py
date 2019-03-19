from urllib.request import urlopen
from pykml import parser
from forecaster.location import Point


class Buoy:

    def __init__(self):
        """
        All buoys contain a coordinate and an id
        """
        self.location = Point()
        self.name = None


class BuoyLookup:

    def __init__(self, only_wave_data: bool = False):
        """
        Member variables
        :param: only_wave_data - bool to tell us that we only want buoys that contain wave data
        """
        self.buoys = []

        self.__parse(only_wave_data)

    def __parse(self, only_wave_data: bool = False):
        """
        The URL below is the original URL to grab a KML document that will
        contain the link to the real kml document containing all coordinates
        and buoy information.

        All Buoy information that is read in as a set of coordinates with a buoy name,
        will be saved and stored.

        :param: only_wave_data - bool to tell us that we only want buoys that contain wave data
        :return: None
        """
        url = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"
        fileobject = urlopen(url)
        root = parser.parse(fileobject).getroot()

        real_kml = root.Document.NetworkLink.Link.href

        if real_kml:
            real_fileobject = urlopen(str(real_kml))
            real_root = parser.parse(real_fileobject).getroot()

            for folder in real_root.Document.Folder:

                for subfolder in folder.Folder:

                    for pm in subfolder.Placemark:

                        description = str(pm.description)

                        if (only_wave_data and 'Wave' in description) or not only_wave_data:

                            # print("{}: {}".format(str(pm.name), str(pm.Point.coordinates)))

                            buoy = Buoy()
                            buoy.name = str(pm.name)

                            """
                            Point.coordinates -> <LON, LAT, ALT>
                            
                            We could also search for LookAT
                            <longitude> ??? </longitude>
                            <latitude> ??? </latitude>
                            <altitude> ??? </altitude>
                            """

                            buoy.location.parse(str(pm.Point.coordinates))

                            self.buoys.append(buoy)