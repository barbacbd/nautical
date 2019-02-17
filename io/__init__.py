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

        if len(cells) == 18:
            wd = WaveData()

            wd.mm = cells[0].find(text=True)
            wd.dd = cells[1].find(text=True)
            wd.time = cells[2].find(text=True)
            wd.convert_time()
            wd.wdir = cells[3].find(text=True)
            wd.wspd = cells[4].find(text=True)
            wd.gst = cells[5].find(text=True)
            wd.wvht = cells[6].find(text=True)
            wd.dpd = cells[7].find(text=True)
            wd.apd = cells[8].find(text=True)
            wd.mwd = cells[9].find(text=True)
            wd.pres = cells[10].find(text=True)
            wd.ptdy = cells[11].find(text=True)
            wd.atmp = cells[12].find(text=True)
            wd.wtmp = cells[13].find(text=True)
            wd.dewp = cells[14].find(text=True)
            wd.sal = cells[15].find(text=True)
            wd.vis = cells[16].find(text=True)
            wd.tide = cells[17].find(text=True)

            past_data.append(wd)

    return past_data