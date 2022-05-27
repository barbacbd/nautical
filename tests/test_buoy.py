import pytest
from nautical.noaa.buoy import SourceType



def test_all_values_converted_not_include_all():
    '''Test that all values can be converted 
    to a string
    '''
    test_subjects = [
        SourceType.INTERNATIONAL_PARTNERS,
        SourceType.IOOS_PARTNERS,
        SourceType.MARINE_METAR,
        SourceType.NDBC_METEOROLOGICAL_OCEAN,
        SourceType.NERRS,
        SourceType.NOS_CO_OPS,
        SourceType.SHIPS,
        SourceType.TAO,
        SourceType.TSUNAMI
    ]

    for test_case in test_subjects:
        assert SourceType.as_strings(test_case) is not None


def test_all_values_source_type():
    '''Test that all values were returned from the 
    class method. The number should be one less than
    the highest value in the class
    '''

    assert len(SourceType.as_strings(SourceType.ALL)) == len(SourceType) - 1


def test_unknown_value():
    '''Test case for finding an unknown value should
    return None
    '''
    assert SourceType.as_strings("random_data") is None
