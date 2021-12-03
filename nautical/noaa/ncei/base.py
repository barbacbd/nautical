from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
import requests


BASE_ENDPOINT = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"

INIT_OFFSET = 1
MAX_RESULT_LIMIT = 1000


def create_offset_lookups(count):
    """
    Create a dictionary that maps the offset to the number to search
    
    :param count: Number returned from a query. See `get_num_results`
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


def get_num_results(endpoint, token):
    """
    Query the API provided with the correct endpoint and authentication token to 
    find the number of possible results from a query.
    
    :param endpoint: Full http endpoint where the `get` request will fetch information from.
    :param token: HTTP athentication token
    
    :return: Number of expected results
    """    
    count = 0
    data = query_base(endpoint, token)
    if 'metadata' in data:
        if 'resultset' in data['metadata']:
            if 'count' in data['metadata']['resultset']:
                count = data['metadata']['resultset']['count']

    return count


def query_base(endpoint, token, limit=1, offset=1):
    """
    Query the API provided with the correct endpoint and authentication token. 
    
    :param endpoint: Full http endpoint where the `get` request will fetch information from.
    :param token: HTTP athentication token
    :param limit: Number of results to yield. The API only allows for a max value of 1000
    :param offset: The location offset where the results will begin. For instance 1001 with a 
    limit of 1000 will return the results for 1001-2000 (if the results exist).
    
    :return: Json encoded result of the query
    """
    headers = {"Token": token}
    return json.loads(
        json.dumps(
            requests.get(
                endpoint, params={'limit': limit, 'offset': offset}, headers=headers
            ).json()
        )
    )


def query_all(extension, token, lookup_offsets):
    """
    Run the common query all for an end node
    
    :param extension: Extension that will be added to the end of the `BASE_ENDPOINT`
    :param token: Token for authentication
    :param lookup_offsets: see `create_offset_lookups`
    
    :return: unordered list of json strings containing the individual results from each query. 
    """
    
    endpoint = BASE_ENDPOINT + extension
    count = get_num_results(endpoint, token)
    lookup_offsets = create_offset_lookups(count)
    
    query_results = []
    # max of 5 per second
    with ThreadPoolExecutor(max_workers=5) as executor:
        start_time = time()
        futr_dists = {executor.submit(query_base, endpoint, token, lookup_offsets[k], k): k for k in lookup_offsets}
        for futr in as_completed(futr_dists):
            query_results.append(futr.result())

        run_time = time()-start_time
        if run_time < 1.0:
            # break up the execution so that we don't timeout on requests
            sleep(1.0-run_time)
    
    return query_results
    