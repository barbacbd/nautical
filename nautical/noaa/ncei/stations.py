import requests
from uuid import uuid4
import json
from time import time, sleep
from concurrent.futures import ThreadPoolExecutor, as_completed


class Station:

    elevation = None
    mindate = None
    maxdate = None
    latitude = None
    name = None
    datacoverage = None
    id = None
    elevationUnit = None
    longitude = None

    def __init__(self, json_obj): 
        for k, v in json_obj.items():
            if hasattr(self, k):
                print(f"Setting {k} to {v}")
                setattr(self, k, v)

    def __str__(self):
        return json.dumps(vars(self), indent=4)


"""
Additional Parameters

    datasetid [Optional] 
        Accepts a valid dataset id or a chain of dataset ids separated by ampersands. Stations 
        returned will be supported by dataset(s) specified
    locationid [Optional]
        Accepts a valid location id or a chain of location ids separated by ampersands. Stations 
        returned will contain data for the location(s) specified
    datacategoryid [Optional] 
        Accepts a valid data category id or an array of data category ids. Stations returned will 
        be associated with the data category(ies) specified
datatypeid

extent

startdate

enddate

sortfield


sortorder

limit

offset

"""

    

def station_lookup(token, limit, offset):
    endpoint = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    headers = {"Token": token}
    return json.loads(json.dumps(requests.get(endpoint, params={'limit': limit, 'offset': offset}, headers=headers).json()))
    
def fetch_all_available_stations(token):
    """
    Each token can only be used 5 times per second OR 10,000 times per day.
    Find the number of times that are required to grab all data knowing the max
    limit is 1000. 

    :param token:
    """
    MAX_LIMIT = 1000
    offset = 1
    count = 0

    data = station_lookup(token, 1, 1)
    if 'metadata' in data:
        if 'resultset' in data['metadata']:
            if 'count' in data['metadata']['resultset']:
                count = data['metadata']['resultset']['count']

    lookup_offsets = {}
    if count > 0:
        num_full = int(count/MAX_LIMIT)
        num_left = count % MAX_LIMIT
        for i in range(num_full):
            lookup_offsets[offset] = MAX_LIMIT
            offset += MAX_LIMIT

        if num_left > 0:
            lookup_offsets[offset] = num_left
    
    sleep(1.0)  # Ensure that we start fresh on our number of queries per second
    
    query_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        start_time = time()
        futr_dists = {executor.submit(station_lookup, token, lookup_offsets[k], k): k for k in lookup_offsets}
        for futr in as_completed(futr_dists):
            query_results.append(futr.result())

        run_time = time()-start_time
        if run_time < 1.0:
            # break up the execution so that we don't timeout on requests
            sleep(1.0-run_time)

    print(len(query_results))


def fetch_specific_station(token, station_id):
    """
    :param token:
    :param station_id:
    """
    pass


def fetch_stations_by_location(token, location_id):
    """
    :param token:
    :param location_id:
    """
    pass


def fetch_stations_by_data_types(token, data_types):
    """
    :param token: 
    :param data_types: list of tuples(str, str)
    """

    pass
