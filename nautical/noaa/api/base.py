from concurrent.futures import ThreadPoolExecutor, as_completed
import inspect 
from time import time


BASE_ENDPOINT = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"

INIT_OFFSET = 1
MAX_RESULT_LIMIT = 1000


def _inner_query_all(endpoint, token, limit, offset):
    



def create_offset_lookups(count):
    """
    Create a dictionary that maps the offset to the number to search
    
    :param count: Number returned from a query
    :return: Dictionary of offsets and the number to search
    """
    lookup_offsets = {}
    offset = INIT_OFFSET
    
    if count > 0:
        num_full = int(count/MAX_RESULT_LIMIT)
        num_left = count % MAX_RESULT_LIMIT
        
        for i in range(num_full):
            lookup_offsets[offset] = MAX_RESULT_LIMIT
            offset += MAX_RESULT_LIMIT
        
        if num_left > 0:
            lookup_offsets[offset] = num_left
    
    return lookup_offsets


def query_all(token, lookup_offsets):
    """
    Run the common query all for an end node
    
    :param func: function that will be
    """
    
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    # name of the file must match the endpoint
    lookup_end = module.__file__
    endpoint = BASE_ENDPOINT + lookup_end
    
    query_results = []
    # max of 5 per second
    with ThreadPoolExecutor(max_workers=5) as executor:
        start_time = time()
        futr_dists = {executor.submit(_inner_query_all, endpoint, token, lookup_offsets[k], k): k for k in lookup_offsets}
        for futr in as_completed(futr_dists):
            query_results.append(futr.result())

        run_time = time()-start_time
        if run_time < 1.0:
            # break up the execution so that we don't timeout on requests
            sleep(1.0-run_time)
    