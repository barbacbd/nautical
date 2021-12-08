import pytest
from nautical.noaa.ncei import *
from uuid import uuid4

"""
Query All

4. Bad object type, base type, endpoint exists but none, endpoint not exist, 
5. Parameters Good, Parameters Bad, Parameters that are allowed, Parameters that are not allowed


Query Base

1. Good query
2. Bad query
3. limit more than 1
4. limit greater than 2 (same query but different results)


Get num results

1. Query with large numbers
2. Query with no results


Create offset lookups
1. positive little count
2. positive large count
3. negative amount

NCEIBase
1. Extend
2. Fill Extent and get json data


"""


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
    assert len(results) > 0

def test_query_obj_type_bad_base():
    """
    Query All:
    Send in object type of base
    """
    results = query_all(get_default_token())
    assert len(results) > 0

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
    
    """
    pass

def test_query_base_bad():
    pass

def test_query_limit_more_than_one():
    pass

def test_query_offset_different():
    pass

def test_offset_positive_small():
    pass

def test_offset_positive_large():
    pass

def test_offset_negative():
    pass

def test_ncei_base_extend():
    pass

def test_ncei_base_fill_and_json():
    pass
