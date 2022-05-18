import pytest
from nautical.noaa.ncei import *
from uuid import uuid4
from os import environ
from unittest.mock import Mock, patch


class MockResponse:
    '''Class to mock the behavior and results of the requests.get function
    in the NCEI module of the Nautical library.
    '''
    
    def __init__(self, json_data, status_code):
        '''Fill the class with the required data for a response
        expected from the NCEI API.

        :param json_data: Dictionary containing the json data set in the response
        :param status_code: Mock of the requests.get status_code
        '''
        if json_data is None:
            raise RuntimeError('None type for json data is not accepted')
        self.json_data = json_data

        if status_code is None:
            raise RuntimeError('None type for status code is not accepted')
        self.status_code = status_code

    def json(self):
        '''Mock function for the requests.get.json return type

        :return: Json formatted dictionary from the request
        '''
        return self.json_data


def format_json(original_json, count, limit, offset):
    '''Format the json as an expected result from the NCEI api.
    The `original_json` will be copied `count` times

    :return: Mock of the json data that should be returned from API
    '''
    output = {
        "metadata": {
            "resultset": {
                "offset": offset,
                "count": max(0, count),
                "limit": max(0, limit)
            }
        },
        "results": []
    }

    for i in range(output["metadata"]["resultset"]["count"]):
        output["results"].append(original_json)

    return output


def test_query_all_large_good_token():
    '''Query All:
    Query for a large number of results. Anything over 1000 is
    intended as it requires the data to be split.
    '''
    num_results = 1200

    num_offsets = int(num_results / 1000) + 1
    lookup_offsets = create_offset_lookups(num_results)

    total = 0
    
    # check for perfect blocks, except the last
    for k, v in lookup_offsets.items():
        with patch("nautical.noaa.ncei.requests.get") as get_patch:
            get_patch.return_value = MockResponse(
                format_json(
                    {
                        "mindate": "1994-04-02",
		        "maxdate": "1996-05-28",
		        "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		        "datacoverage": 1,
		        "id": "ACMC"
                    }, v, v, k
                ), 200 )

            results = query_all("test-token", obj_type=DataType)
            assert len(results) == v
            total += len(results)

    assert total == num_results

    
def test_query_all_good_token():
    '''Query All:
    Token is good
    Query for a smaller one of types.
    '''
    num_results = 25
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
		    "maxdate": "1996-05-28",
		    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		    "datacoverage": 1,
		    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results = query_all("test-token", obj_type=DataType)
        assert len(results) == num_results

        
def test_query_all_bad_token():
    '''Query All:
    Token is Bad
    '''
    num_results = 0
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json({}, num_results, 1000, 1), 404 )

        results = query_all("bad-token", obj_type=DataType)
        assert len(results) == num_results
    
    results = query_all("bad-token", obj_type=DataType)
    assert len(results) == 0

def test_query_obj_type_bad_base():
    '''Query All:
    Send in object type of base. this will 'fail' because the base
    type is used, and nothing matches
    '''
    results = query_all("token-does-NOT-matter")
    assert len(results) == 0

    
def test_query_obj_type_bad_type():
    '''Query All:
    Bad object type, this type will fail because it does not
    have an attribute `endpoint`
    '''
    class ExampleTest:
        def __init__(self):
            self.data = None

    with pytest.raises(AttributeError):
        results = query_all("token-does-NOT-matter", obj_type=ExampleTest)

        
def test_query_bad_endpoint_exists():
    '''Query All:
    Send in type where endpoint exists but is invalid. This endpoint cannot be 
    reached and should have an error caught where the expected results will 
    be empty.
    '''
    # reset the endpoint to something invalid
    x = DataType.endpoint
    DataType.endpoint = NCEIBase.endpoint + "bad_endpoint"

    num_results = 0
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json({}, num_results, 1000, 1), 404 )
    
    results = query_all("test-token", obj_type=DataType)

    # reset the endpoint back to the original - that way we don't fail later
    DataType.endpoint = x
    assert len(results) == 0


def test_query_bad_no_endpoint():
    '''Query All:
    Send in type where the endpoint does not exist
    '''
    # capture the original and set the current endpoint to None
    x = DataType.endpoint
    DataType.endpoint = None

    # no need to mock, this failure will happen before any calls
    with pytest.raises(AttributeError):
        results = query_all("token-does-NOT-matter", obj_type=DataType)

    # reset the endpoint
    DataType.endpoint = x


def test_query_base_good():
    '''Find the first result in the query
    '''
    num_results = 1
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
		    "maxdate": "1996-05-28",
		    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		    "datacoverage": 1,
		    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results = query_base("test-token", DataType.endpoint, obj_type=DataType)
        assert len(results) == num_results


def test_query_base_bad():
    '''Test that the endpoint is bad 
    '''
    num_results = 0
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json({}, num_results, 1000, 1), 404 )

        results = query_base("bad-token", NCEIBase.endpoint+"bad_data", obj_type=DataType)
        assert len(results) == 0


def test_query_limit_more_than_one():
    '''Find the first 1000 results in the datatypes endpoint
    '''
    num_results = 1000
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
		    "maxdate": "1996-05-28",
		    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		    "datacoverage": 1,
		    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results = query_base("test-token", DataType.endpoint, obj_type=DataType, limit=1000, offset=1)
        assert len(results) == num_results

    
def test_query_offset_different():
    '''Get the first and second results but use two different queries and compare the data
    '''
    num_results = 1
    
    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
		    "maxdate": "1996-05-28",
		    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		    "datacoverage": 1,
		    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

    
        results_one = query_base("test-token", DataType.endpoint, obj_type=DataType)

    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-06-02",
		    "maxdate": "1996-07-28",
		    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
		    "datacoverage": 1,
		    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results_two = query_base("test-token", DataType.endpoint, obj_type=DataType, offset=2)

    assert len(results_one) == len(results_two)
    assert len(results_one) == 1
    assert len(results_two) == 1
    assert type(results_one[0]) == type(results_two[0])
    assert results_one[0] != results_two[0]


def test_offset_positive_small():
    '''Small number that does not exceed the 1000 limit
    '''
    lookup_offsets = create_offset_lookups(500)
    assert len(lookup_offsets) == 1
    assert lookup_offsets[1] == 500

    
def test_offset_positive_large():
    '''Test a large number that should create quite a few chunks 15034
    16 chunks - 15 full size and 1 of 34
    '''
    num_lookups = 15034
    # 1000 is the max return values 
    num_offsets = int(num_lookups / 1000) + 1

    lookup_offsets = create_offset_lookups(num_lookups)
    assert len(lookup_offsets) == num_offsets

    # check for perfect blocks, except the last
    for k, v in lookup_offsets.items():
        if v != 1000:
            assert v == num_lookups - ((num_offsets-1)*1000)


def test_offset_negative():
    '''Test a negative number which will throw an error
    '''
    with pytest.raises(ValueError):
        create_offset_lookups(-1)

        
def test_zero_offset():
    '''Test a zero number. This will be an empty 
    '''
    lookup_offsets = create_offset_lookups(0)
    assert len(lookup_offsets) == 0


def test_query_all_valid_single_param():
    '''Test utilizing a single parameter that is valid
    '''
    num_results = 25
    param = Parameter("test-parameter", "value")

    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
                    "maxdate": "1996-05-28",
                    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
                    "datacoverage": 1,
                    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results = query_all("test-token", obj_type=DataType, parameters=param)
        assert len(results) == num_results


def test_query_all_valid_multiple_params():
    '''Test utilizing a multiple parameters that is valid
    '''
    num_results = 25
    params = [
        Parameter("test-parameter1", "value1"),
        Parameter("test-parameter2", "value2"),
        Parameter("test-parameter3", "value3")
    ]

    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
                    "maxdate": "1996-05-28",
                    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
                    "datacoverage": 1,
                    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        results = query_all("test-token", obj_type=DataType, parameters=params)
        assert len(results) == num_results


def test_query_all_invalid_single_param():
    '''Test utilizing a single parameter that is invalid,
    Not of the type `Parameter`
    '''
    num_results = 25
    param = "Some-bad-parameter"

    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
                    "maxdate": "1996-05-28",
                    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
                    "datacoverage": 1,
                    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        with pytest.raises(TypeError):
            results = query_all("test-token", obj_type=DataType, parameters=param)


def test_query_all_invalid_multiple_params():
    '''Test utilizing a multiple parameters where at least one
    of the parameters is invalid, not of the type `Parameter`.
    '''
    num_results = 25
    params = [
        Parameter("test-parameter1", "value1"),
        "some-random-data-thrown-here",
        Parameter("test-parameter2", "value2"),
        Parameter("test-parameter3", "value3")
    ]

    with patch("nautical.noaa.ncei.requests.get") as get_patch:
        get_patch.return_value = MockResponse(
            format_json(
                {
                    "mindate": "1994-04-02",
                    "maxdate": "1996-05-28",
                    "name": "Average cloudiness midnight to midnight from 30-second ceilometer data",
                    "datacoverage": 1,
                    "id": "ACMC"
                }, num_results, 1000, 1
            ), 200 )

        with pytest.raises(TypeError):
            results = query_all("test-token", obj_type=DataType, parameters=params)
