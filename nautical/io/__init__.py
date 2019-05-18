from urllib.request import urlopen
from bs4 import BeautifulSoup
from pykml import parser
from ..noaa import WaveData, SwellData
from ..location import Point


def get_buoys_information(only_wave_data: bool = False):
    """
    NOAA is kind enough to provide all of names, ids, and other information about ALL of their known buoys
    in a kml document hosted at the link provided.

    https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml

    Let's read through this document and parse the buoy information to determine their id and location.
    The ID can be used to provide to get_noaa_forecast_url(). Then we can find even more information about the
    buoys. NOTE: the SHIP ID may not be able to be looked up. The coordinates are used aas general information
    to determine distance from other points, or for display purposes.

    NOTE: we could download the kml and pass in the data file, but some of the locations and information of
    the buoys is updated a half hourly rate, so we will attempt to read the live data

    All Buoy information that is read in as a set of coordinates with a buoy name, will be saved and stored.

    :param: only_wave_data - bool to tell us that we only want buoys that contain wave data
    :return: dictionary containing all buoy information where the key is the ID and the value is the Point()
    """
    buoys = {}

    """
    This is the ONLY known location of the kml file, this file contains the link to the 
    next kml file that contains all of the information we need!
    """
    url = "https://www.ndbc.noaa.gov/kml/marineobs_by_pgm.kml"
    fileobject = urlopen(url)
    root = parser.parse(fileobject).getroot()

    """ 
    Grab the REAL link to the kml document we are really after
    """
    real_kml = root.Document.NetworkLink.Link.href

    if real_kml:
        real_fileobject = urlopen(str(real_kml))
        real_root = parser.parse(real_fileobject).getroot()

        """ 
        Traverse the KML markup 

        Document
        --- Folder
            --- Placemark
                --- DATA (name, coordinates, other)
        """
        for folder in real_root.Document.Folder:

            for subfolder in folder.Folder:

                for pm in subfolder.Placemark:

                    description = str(pm.description)

                    if (only_wave_data and 'Wave' in description) or not only_wave_data:
                        """
                        Point.coordinates are in the format <LON, LAT, ALT>
                        NOTE: We could also search for LookAT and search further for, longitude, latitude, or altitude
                        """
                        p = Point()
                        p.parse(str(pm.Point.coordinates))
                        buoys[str(pm.name)] = p

    return buoys


def get_noaa_forecast_url(buoy):
    """
    NOAA is kind enough to post all of their data from their buoys at the same url ONLY requiring
    the id of buoy to change at the end of the link.

    https://www.ndbc.noaa.gov/station_page.php?station=

    this function will simply take in the buoy from the user and append the data to the
    end of the url, IFF the data exists.

    NOTE: this does not check to ensure that this is a valid url.

    The next step(s) would be to pass this url and buoy value to several other functions for forecast data.
    get_current_data(search_url, id)
    get_detailed_wave_summary(search_url)
    get_swell_data(search_url)
    get_wave_data(search_url)

    :param buoy: id of the buoy
    :return: if buoy is not empty , return the full url, otherwise return nothing
    """
    return "https://www.ndbc.noaa.gov/station_page.php?station={}".format(buoy) if buoy else None


def _get_url_source(url_name):
    """
    NOTE: this is a utility function used to shortcut the process. It is intended for INTERNAL USE ONLY.

    If you already know the url_name or if you have run through the get_noaa_forecast_url(), then you can
    send in the url here. NOTE: we make no assumptions about the validity of the url and any data that it
    may contain.

    Get the source information for the url and place the information into a BeautifulSoup object, so that we
    can do any lookups of the data that we need.

    :param url_name: name of the url to search for
    :return: BeautifulSoup Object
    """
    open_url = urlopen(url_name)
    soup = BeautifulSoup(open_url.read(), features="lxml")
    return soup


def get_current_data(url_name, id):
    """
    Get a list of all attributes pertaining to the current data for the given id
    :param url_name: link to the tables for current data
    :param id: id or name to search for
    :return: list of all data for the current table
    """
    soup = _get_url_source(url_name)

    search = "Conditions at {} as of".format(id)
    table = soup.find(text=search).findParent("table")

    attributes = []

    for row in table.findAll('tr'):
        cells = row.findAll('td')

        if len(cells) == 3:
            attributes.append((str(cells[1].find(text=True)).strip(), str(cells[2].find(text=True)).strip()))

    return attributes


def get_detailed_wave_summary(url_name):
    """
    Get a list of attributes containing the detailed wave summary.

    The user will pass in the url_name that is generated from get_noaa_forecast_url(), where the buoy id
    is provided. This function will search through the html source and find the 'Detailed Wave Summary'
    html table and parse the data from the table

    :param url_name: url containing the table with the Detailed Wave Summary information
    :return: attributes of this information in the table
    """
    soup = _get_url_source(url_name)
    table = soup.find(text="Detailed Wave Summary").findParent("table")

    attributes = []

    for row in table.findAll('tr'):
        cells = row.findAll('td')

        if len(cells) == 3:
            attributes.append((str(cells[1].find(text=True)).strip(), str(cells[2].find(text=True)).strip()))

    return attributes


def get_wave_data(url_name):
    """
    Get a table of all Wave Data
    :param url_name: name of the url to search for
    :return: list of Wave Data
    """
    soup = _get_url_source(url_name)

    past_data = []

    table = soup.find("table", {"class": "dataTable"})
    for row in table.findAll("tr"):
        cells = row.findAll("td")

        """ 
        18 is a magic number unfortunately this is the CURRENT number of columns in
        the table presented by NOAA. NOTE: not all columns are used they are either 
        left blank or contain a dash (-)
        """
        if len(cells) == 18:
            mm = str(cells[0].find(text=True)).strip()
            dd = str(cells[1].find(text=True)).strip()
            time = str(cells[2].find(text=True)).strip()
            wdir = str(cells[3].find(text=True)).strip()
            wspd = str(cells[4].find(text=True)).strip()
            gst = str(cells[5].find(text=True)).strip()
            wvht = str(cells[6].find(text=True)).strip()
            dpd = str(cells[7].find(text=True)).strip()
            apd = str(cells[8].find(text=True)).strip()
            mwd = str(cells[9].find(text=True)).strip()
            pres = str(cells[10].find(text=True)).strip()
            ptdy = str(cells[11].find(text=True)).strip()
            atmp = str(cells[12].find(text=True)).strip()
            wtmp = str(cells[13].find(text=True)).strip()
            dewp = str(cells[14].find(text=True)).strip()
            sal = str(cells[15].find(text=True)).strip()
            vis = str(cells[16].find(text=True)).strip()
            tide = str(cells[17].find(text=True)).strip()

            wd = WaveData(mm=mm, dd=dd, time=time, wdir=wdir, wspd=wspd, gst=gst, wvht=wvht, dpd=dpd, apd=apd,
                          mwd=mwd, pres=pres, ptdy=ptdy, atmp=atmp, wtmp=wtmp, dewp=dewp, sal=sal, vis=vis, tide=tide)

            past_data.append(wd)

    return past_data


def get_swell_data(url_name):
    """
    Get a list of all swell data from the past.
    :param url_name: url to the area containing the kml data
    :return: list of swell data
    """
    soup = _get_url_source(url_name)
    past_data = []

    table = soup.findAll("table", {"class": "dataTable"})
    for row in table[1].findAll("tr"):
        cells = row.findAll("td")

        """ 
        12 is a magic number unfortunately this is the CURRENT number of columns in
        the table presented by NOAA. NOTE: not all columns are used they are either 
        left blank or contain a dash (-)
        """
        if len(cells) == 12:
            mm = str(cells[0].find(text=True)).strip()
            dd = str(cells[1].find(text=True)).strip()
            time = str(cells[2].find(text=True)).strip()
            wvht = str(cells[3].find(text=True)).strip()
            swh = str(cells[4].find(text=True)).strip()
            swp = str(cells[5].find(text=True)).strip()
            swd = str(cells[6].find(text=True)).strip()
            wwh = str(cells[7].find(text=True)).strip()
            wwp = str(cells[8].find(text=True)).strip()
            wwd = str(cells[9].find(text=True)).strip()
            steepness = str(cells[10].find(text=True)).strip()
            apd = str(cells[11].find(text=True)).strip()

            sd = SwellData(mm=mm, dd=dd, time=time, wvht=wvht, swh=swh, swp=swp,
                           swd=swd, wwh=wwh, wwp=wwp, wwd=wwd, steepness=steepness, apd=apd)

            past_data.append(sd)

    return past_data



