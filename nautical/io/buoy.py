from re import sub
from bs4 import BeautifulSoup
from nautical.log import get_logger
from nautical.io.web import get_noaa_forecast_url, get_url_source
from nautical.noaa.buoy.buoy_data import BuoyData
from nautical.noaa.buoy.buoy import Buoy


log = get_logger()


def create_buoy(buoy):
    '''Provide a full workup for a specific buoy. If the buoy is None or it cannot
    be found then the data returned will be considered invalid as None

    :param buoy: id of the buoy to do a workup on
    :return: BuoyWorkup if successful else None
    '''
    if not buoy:
        return None

    url = get_noaa_forecast_url(buoy)
    soup = get_url_source(url)

    current_buoy_data = BuoyData()
    buoy_valid = get_current_data(soup, current_buoy_data, f"Conditions at {buoy}")
    buoy_valid |= get_current_data(soup, current_buoy_data, "Detailed Wave Summary")

    if not buoy_valid:
        return None
    
    buoy_data = Buoy(buoy)
    buoy_data.valid = buoy_valid
    buoy_data.present = current_buoy_data

    return buoy_data


def get_current_data(soup: BeautifulSoup, buoy: BuoyData, search: str):
    '''Search the beautiful soup object for a TABLE containing the search string. The 
    function will grab the data from the table and create a NOAAData object and return the data

    :param soup: beautiful soup object generated from the get_url_source()
    :param buoy: BuoyData object that should be filled with data as this function parses the data.
    :param search: text to search for in the soup object. 
    :return: True when data has been found and set
    '''
    # keep track of the number of variables that were set, indicates validity
    buoy_variables_set = 0

    try:
        txt_search = soup.find(string=search)
    except AttributeError as error:
        log.debug(error)
        # backwards compatible for old versions of bs4
        txt_search = soup.find(text=search)
        
    if not txt_search:
        return False

    table = txt_search.findParent("table")
    if not table:
        return False

    for i, row in enumerate(table.findAll('tr')):

        # the first table is another table and it is no use to use -- skipping
        if i >= 1:
            cells = row.findAll('td')

            if cells:
                try:
                    key_data = cells[1].next.split()
                    key = sub('[():]', '', key_data[len(key_data) - 1]).lower()
                    value = cells[2].next.split()[0]

                    buoy.set(key, value)
                    buoy_variables_set += 1
                except (IndexError, TypeError, AttributeError) as error:
                    log.error(error)

    # no variables set indicates errors or invalid buoy
    return buoy_variables_set > 0


# Alias for getting current data, It has the same result
get_buoy_data = get_current_data
