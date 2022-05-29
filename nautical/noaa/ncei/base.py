from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from time import time, sleep
import requests
from nautical.log import get_logger


# access the base logging object
log = get_logger()
MAX_RESULT_LIMIT = 1000


class Parameter:
    '''
    Class to track the query parameters that can and will exist
    at the end of the API queries. For instance:

    datatypeid=EMNT
    '''
    __slots__ = ['param', 'data']

    def __init__(self, param: str, data: str):
        self.param = param
        self.data = data

    def __str__(self):
        return f"{self.param}={self.data}"


class NCEIBase:

    '''Base class for all NCEI types'''

    parameters = None
    endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/"

    def __init__(self, json_data=None):

        if hasattr(self, "__slots__"):
            if isinstance(json_data, dict):
                for slot in self.__slots__:
                    if slot in json_data:
                        setattr(self, slot, json_data[slot])
        else:
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    setattr(self, key, value)
            elif json_data is not None:
                setattr(self, "data", json_data)

    def __str__(self):
        '''String override for this instance

        :return: String representation of this instance, formatted as json.
        '''
        if hasattr(self, "__slots__"):
            json_data = {}
            for slot in self.__slots__:
                if getattr(self, slot, None) is not None:
                    json_data[slot] = getattr(self, slot)
            return json.dumps(json_data, indent=4)
        return json.dumps(vars(self), indent=4)            

    def __eq__(self, other):
        '''Determine if this instance is the same as the other passed in.

        :param other: Other object to compare to this one.
        :return: True when the instances are the same.
        '''

        if isinstance(other, type(self)):
            if hasattr(self, '__slots__'):
                for slot in self.__slots__:
                    if not (hasattr(self, slot) and hasattr(other, slot)):
                        return False

                    if getattr(self, slot) != getattr(other, slot):
                        return False
                return True
        return False

    def __ne__(self, other):
        '''See __eq__ for more information

        :return: The opposite of __eq__
        '''
        return not self.__eq__(other)


def create_offset_lookups(count):
    '''Create a dictionary that maps the offset to the number to search

    :param count: Number returned from a query. See `get_num_results`
    :return: Dictionary of offsets and the number to search
    '''
    if count < 0:
        raise ValueError("Cannot create offsets for negative numbers")

    lookup_offsets = {}
    offset = 1  # Initial offset 

    num_full = int(count / MAX_RESULT_LIMIT)
    num_left = int(count % MAX_RESULT_LIMIT)

    for _ in range(num_full):
        lookup_offsets[offset] = MAX_RESULT_LIMIT
        offset += MAX_RESULT_LIMIT

    if num_left > 0:
        lookup_offsets[offset] = num_left

    return lookup_offsets


def _query(token, endpoint, limit=1, offset=1):
    '''Execute the POST request/query

    :param token: Authentication token 
    :param endpoint: Endpoint to query 
    :param limit: Number of results to accept. Max of 1000
    :param offset: Entry offset used to determine which results to accept
    :return: JSON object representing the result of the query
    '''
    try:
        result = requests.get(
            endpoint, params={'limit': limit, 'offset': offset}, headers={"Token": token}
        ).json()
        return json.loads(json.dumps(result))
    except (TypeError, json.decoder.JSONDecodeError) as error:
        log.error(error)
        return None


def get_num_results(token, endpoint):
    '''Query the API provided with the correct endpoint and authentication
    token to find the number of possible results from a query.

    :param token: HTTP athentication token
    :param endpoint: Full http endpoint where the `get` request will fetch information from.
    :return: Number of expected results
    '''    
    count = 0
    data = _query(token, endpoint)

    if data is not None:
        if 'metadata' in data:
            if 'resultset' in data['metadata']:
                if 'count' in data['metadata']['resultset']:
                    count = data['metadata']['resultset']['count']

    return count


def query_base(token, endpoint, obj_type=NCEIBase, limit=1, offset=1):
    '''Query the API provided with the correct endpoint and authentication token. 

    :param token: HTTP athentication token
    :param endpoint: Full http endpoint where the `get` request will fetch information from.
    :param obj_type: Class type that will be used to make the objects
    :param limit: Number of results to yield. The API only allows for a max value of 1000
    :param offset: The location offset where the results will begin. 
    :return: Json encoded result of the query
    '''
    json_data = _query(token, endpoint, limit, offset)
    results = []

    if isinstance(json_data, dict):
        if 'results' in json_data:
            results.extend(json_data['results'])
        else:
            results.append(json_data)
    elif json_data is not None:
        results.append(json_data)

    try:
        converted_results = [obj_type(result) for result in results if result is not None]
        return converted_results
    except (ValueError, TypeError) as error:
        log.error(error)
        raise


def _check_parameters(parameters):
    '''Check that the type(s) of the parameters are all of the 
    type `Parameter` from this module.

    :param parameters: List of Parameters or Parameter object
    :return: True when all parameters are of type `Parameter`
    '''
    if isinstance(parameters, list):
        return False not in [isinstance(p, Parameter) for p in parameters]
    return isinstance(parameters, Parameter)


def combine_parameters(obj_type, parameters):
    '''Combine all parameters contained in the parameters parameter 
    in the format expected for the endpoint.

    :param parameters: List or single parameter
    :param obj_type: Type of object where parameters are applied
    :return: string formatted as expected for the endpoint
    '''
    if not _check_parameters(parameters):
        raise TypeError("parameters must be type Parameter or List[Parameter]")

    if isinstance(parameters, list):
        return "&".join([str(p) for p in parameters if p.param in obj_type.parameters])

    if parameters.param in obj_type.parameters:
        return "?" + str(parameters)

    return None


def add_params_to_endpoint(endpoint, obj_type, parameters):
    '''Add the parameters to the endpoint to create a final endpoint

    :param endpoint: Original Endpoint
    :param obj_type: Type of object where parameters are applied
    :param parameters: List or single Parameter
    :return: The final formatted endpoint
    '''
    combined = combine_parameters(obj_type, parameters)
    if not combined:
        return endpoint
    
    return endpoint + "?" + combined


def query_all(token, obj_type=NCEIBase, parameters=None):
    '''Run the common query all for an end node

    :param token: Token for authentication
    :param obj_type: Class for the type of data to be returned.
    :param parameters: List or single `Parameter` object(s) that will be used for the query.
    :return: unordered list of json strings containing the individual results from each query. 
    :raises AttributeError: If endpoint of the class type is not set
    :raises AttributeError: If class type does not have a variable parameters
    :raises TypeError: If parameters does not contain only type `Parameter`
    '''
    endpoint = obj_type.endpoint if hasattr(obj_type, "endpoint") else None

    if endpoint is None:
        raise AttributeError("Invalid endpoint")
    if not hasattr(obj_type, 'parameters'):
        raise AttributeError(f"{str(obj_type)} has no attribute parameters")

    if parameters is not None:
        endpoint = add_params_to_endpoint(endpoint, obj_type, parameters)

    count = get_num_results(token, endpoint)
    lookup_offsets = create_offset_lookups(count)

    query_results = []
    # max of 5 per second
    with ThreadPoolExecutor(max_workers=5) as executor:
        start_time = time()

        # pylint: disable=all
        futr_dists = {
            executor.submit(
                query_base,
                token,
                endpoint, 
                obj_type=obj_type, 
                limit=lookup_offsets[key], 
                offset=key
            ): key for key in lookup_offsets
        }

        for futr in as_completed(futr_dists):
            query_results.extend(futr.result())

        run_time = time() - start_time
        if run_time < 1.0:
            # break up the execution so that we don't timeout on requests
            sleep(1.0 - run_time)

    return query_results
