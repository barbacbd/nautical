import urllib2
from BeautifulSoup import BeautifulSoup
from wave_data import WaveData


def get_url_source(url_name):
    """
    Get the source information for the url and place the inforamtion
    into a BeautifulSoup object
    :param url_name: name of the url to search for
    :return: BeautifulSoup Object
    """
    open_url = urllib2.urlopen(url_name)
    soup = BeautifulSoup(open_url.read())
    return soup


def get_wave_table(url_name):
    """
    Get a table of all Wave Data
    :param url_name: name of the url to search for
    :return: list of Wave Data
    """
    soup = get_url_source(url_name)

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
            wd = WaveData()

            wd.mm = str(cells[0].find(text=True)).strip()
            wd.dd = str(cells[1].find(text=True)).strip()
            wd.time = str(cells[2].find(text=True)).strip()
            wd.convert_time()
            wd.wdir = str(cells[3].find(text=True)).strip()
            wd.wspd = str(cells[4].find(text=True)).strip()
            wd.gst = str(cells[5].find(text=True)).strip()
            wd.wvht = str(cells[6].find(text=True)).strip()
            wd.dpd = str(cells[7].find(text=True)).strip()
            wd.apd = str(cells[8].find(text=True)).strip()
            wd.mwd = str(cells[9].find(text=True)).strip()
            wd.pres = str(cells[10].find(text=True)).strip()
            wd.ptdy = str(cells[11].find(text=True)).strip()
            wd.atmp = str(cells[12].find(text=True)).strip()
            wd.wtmp = str(cells[13].find(text=True)).strip()
            wd.dewp = str(cells[14].find(text=True)).strip()
            wd.sal = str(cells[15].find(text=True)).strip()
            wd.vis = str(cells[16].find(text=True)).strip()
            wd.tide = str(cells[17].find(text=True)).strip()

            past_data.append(wd)

    return past_data
