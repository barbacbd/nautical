import pytest
from nautical.noaa.ncei import *
from uuid import uuid4

def test_query_good_token():
    """
    Query All:
    Token is good
    Query for a smaller one of types.
    """
    results = query_all(get_default_token(), obj_type=DataType)
    assert len(results) > 0

def test_query_bad_token():
    """
    Query All:
    Token is Bad
    """
    results = query_all(str(uuid4()), obj_type=DataType)
    assert len(results) == 0

def test_query_obj_type_bad_base():
    """
    Query All:
    Send in object type of base
    """
    results = query_all(get_default_token())
    assert len(results) == 0

def test_query_obj_type_bad_type():
    """
    Query All:
    Bad object type
    """
    class ExampleTest:
        def __init__(self):
            self.data = None

    with pytest.raises(AttributeError):
        results = query_all(get_default_token(), obj_type=ExampleTest)

def test_query_bad_endpoint_exists():
    """
    Query All:
    Send in type where endpoint exists but not set
    """
    x = DataType.endpoint
    DataType.endpoint = NCEIBase.endpoint + "bad_endpoint"

    results = query_all(get_default_token(), obj_type=DataType)
    DataType.endpoint = x
    assert len(results) == 0

def test_query_bad_no_endpoint():
    """
    Query All:
    Send in type where the endpoint does not exist
    """
    x = DataType.endpoint
    DataType.endpoint = None
    with pytest.raises(AttributeError):
        results = query_all(get_default_token(), obj_type=DataType)
    DataType.endpoint = x

def test_query_base_good():
    """
    Find the first result in the query
    """
    results = query_base(get_default_token(), DataType.endpoint, obj_type=DataType)
    assert len(results) == 1

def test_query_base_bad():
    """
    Test that the endpoint is bad 
    """
    results = query_base(get_default_token(), NCEIBase.endpoint+"bad_data", obj_type=DataType)
    assert len(results) == 0

def test_query_limit_more_than_one():
    """ 
    Find the first 1000 results in the datatypes endpoint
    """
    results = query_base(get_default_token(), DataType.endpoint, obj_type=DataType, limit=1000, offset=1)
    assert len(results) == 1000

def test_query_offset_different():
    """
    Get the first and second results but use two different queries and compare the data
    """
    results_one = query_base(get_default_token(), DataType.endpoint, obj_type=DataType)
    results_two = query_base(get_default_token(), DataType.endpoint, obj_type=DataType, offset=2)

    assert len(results_one) == len(results_two)
    assert len(results_one) == 1
    assert len(results_two) == 1
    assert type(results_one[0]) == type(results_two[0])
    assert results_one[0] != results_two[0]

def test_offset_positive_small():
    """
    Small number that does not exceed the 1000 limit
    """
    lookup_offsets = create_offset_lookups(500)
    assert len(lookup_offsets) == 1
    assert lookup_offsets[1] == 500

def test_offset_positive_large():
    """
    Test a large number that should create quite a few chunks 15034
    16 chunks - 15 full size and 1 of 34
    """
    lookup_offsets = create_offset_lookups(15034)
    assert len(lookup_offsets) == 16

def test_offset_negative():
    """
    Test a negative number which will throw an error
    """
    with pytest.raises(ValueError):
        create_offset_lookups(-1)

def test_zero_offset():
    """
    Test a zero number. This will be an empty 
    """
    lookup_offsets = create_offset_lookups(0)
    assert len(lookup_offsets) == 0

