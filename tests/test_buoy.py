from copy import copy, deepcopy
import pytest
from uuid import uuid4
from nautical.location import Point
from nautical.noaa.buoy import SourceType, Source, Buoy, BuoyData
from nautical.time import NauticalTime
from datetime import datetime, timezone


def test_all_values_converted_not_include_all(subtests):
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
        with subtests.test(test_case=test_case):
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


def test_copy_source_no_buoys_left():
    '''Create a source, and add several buoys. 
    Make a copy of the source, and the buoys should
    be empty as they are NOT copied using a shallow copy. The
    IDs of the sources should NOT match
    '''
    # make 5 buoy ids
    station_ids = [str(uuid4())] * 5
    buoys = [Buoy(station_id, f"Test buoy {station_id}", Point(36.0, -75.0))
             for station_id in station_ids]
    
    source = Source(SourceType.as_strings(SourceType.INTERNATIONAL_PARTNERS),
                    "This is a test Source, do not use")
    for buoy in buoys:
        source.add_buoy(buoy)

    copied_source = copy(source)

    assert len(source) > 0
    assert len(copied_source) == 0
    assert source.name == copied_source.name
    assert source.description == copied_source.description
    assert id(source) != id(copied_source)

    
def test_deepcopy_source():
    '''Create a source, and add several buoys. Make a
    deepcopy of the source, and all data should be
    contained within the source.
    '''
    # make 5 buoy ids
    station_ids = [str(uuid4())] * 5
    buoys = [Buoy(station_id, f"Test buoy {station_id}", Point(36.0, -75.0))
             for station_id in station_ids]
    
    source = Source(SourceType.as_strings(SourceType.INTERNATIONAL_PARTNERS),
                    "This is a test Source, do not use")
    for buoy in buoys:
        source.add_buoy(buoy)

    copied_source = deepcopy(source)

    assert len(source) > 0
    assert len(copied_source) > 0
    assert source.name == copied_source.name
    assert source.description == copied_source.description
    assert id(source) != id(copied_source)

    
def test_adding_known_values_to_buoy(subtests):
    '''Test adding known values to the buoy, and
    make sure that they are correct when retrieved
    '''
    buoy_data = BuoyData()
    preset_values = {
        'wdir': "ESE",
        'wspd': 10.2,
        'gst': 15.9,
        'mwd': "E",
        'wspd10m': 10.4,
        'wspd20m': 13.4,
        'wvht': 2.5,
        'dpd': 2.5,
        'apd': 2.5,
        'wwh': 3.5,
        'wwp': 7,
        'wwd': "ESE",
        'swh': 10.0,
        'swp': 1.4,
        'swd': "W",
        'pres': 1.8,
        'ptdy': 1.8,
        'atmp': 76.5,
        'wtmp': 65.3,
        'dewp': 85.0,
        'otmp': 65.3
    }
    for k, v in preset_values.items():
        buoy_data.set(k, v)

    for k, v in preset_values.items():
        with subtests.test(buoy_data=buoy_data, k=k, v=v):
            assert getattr(buoy_data, k) == v

        
def test_adding_unknown_values_to_buoy(subtests):
    '''Test that adding an unknown variable
    to a buoy will not be allowed
    '''
    buoy_data = BuoyData()
    preset_values = {
        'unknown_value': "test"
    }
    for k, v in preset_values.items():
        buoy_data.set(k, v)

    for k, v in preset_values.items():
        with subtests.test(buoy_data=buoy_data, k=k):
            assert getattr(buoy_data, k, None) == None


def test_default_epoch_time_in_buoy():
    '''Test that the default epoch time is
    close to a value that we calculate
    '''
    buoy_data = BuoyData()
    assert buoy_data.epoch_time > 0


def test_set_time_see_epoch_time():
    '''Set the time for a buoy, and make sure
    that the epoch time is close or the same
    to what we expect. Value retrieved from
    https://www.epochconverter.com/ <<< then the
    milliseconds are converted to seconds
    '''
    buoy_data = BuoyData()
    # 0830 on 05/14/2000
    buoy_data.set("mm", 5)
    buoy_data.set("dd", 14)
    buoy_data.set("year", 2000)
    nt = NauticalTime()
    nt.minutes = 30
    nt.hours = 8
    buoy_data.set("time", nt)

    # precalculated value
    assert buoy_data.epoch_time == 958293000


def test_buoy_data_json_all_available(subtests):
    '''Test converting A buoy data object from json where all 
    values are accepted. Also test that the data can be converted
    back to json and that all values match.
    '''
    now = datetime.now().replace(tzinfo=timezone.utc)
    original_json = {
        'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
        'wspd10m': 10.4, 'wspd20m': 13.4,
        'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
        'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
        'swh': 10.0, 'swp': 1.4, 'swd': "W",
        'pres': 1.8, 'ptdy': 1.8,
        'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
        'time': '09:34:00', 'dd': now.day, 'mm': now.month, 'year': now.year
    }
    bd = BuoyData.from_json(original_json)

    tests_run = 0    
    for k, v in bd:
        with subtests.test(msg=f"Json test for {k}", original_json=original_json, k=k, v=v):
            assert k in original_json
            
            if k == "time":
                assert v.hours == 9
                assert v.minutes == 34
            else:
                assert v == original_json[k]
            
            tests_run += 1

    assert tests_run == len(original_json)
    
    
    new_bd = BuoyData.from_json(bd.to_json())
    
    for k, v in bd:
        with subtests.test(msg=f"Json to Json: {k}", new_bd=new_bd, k=k, v=v):
            assert k in new_bd
            
            if k == "time":
                assert v.hours == getattr(new_bd, k).hours
                assert v.minutes == getattr(new_bd, k).minutes
            else:
                assert v == getattr(new_bd, k)


def test_buoy_data_json_not_all_available(subtests):
    '''Test converting A buoy data object from json where most of the
    values are correctly set, while some are skipped.
    '''
    now = datetime.now().replace(tzinfo=timezone.utc)
    original_json = {
        'random_value1': 0, 'random_value2': 0,
        'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
        'wspd10m': 10.4, 'wspd20m': 13.4,
        'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
        'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
        'swh': 10.0, 'swp': 1.4, 'swd': "W",
        'pres': 1.8, 'ptdy': 1.8,
        'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
        'time': '09:34:00', 'dd': now.day, 'mm': now.month, 'year': now.year
    }
    fail_values = ['random_value1', 'random_value2']
    
    bd = BuoyData.from_json(original_json)

    tests_run = []
    for k, v in bd:
        with subtests.test(msg=f"Json test for {k}", tests_run=tests_run, original_json=original_json, k=k, v=v):
            assert k in original_json
            tests_run.append(k)

    # ensure that the fail_values were never run
    for fv in fail_values:
        with subtests.test(fv=fv, tests_run=tests_run):
            assert fv not in tests_run


def test_buoy_json_all_available():
    '''Test setting a buoy object from json'''

    now = datetime.now().replace(tzinfo=timezone.utc)
    original_json = {
        "data": {
            'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
            'wspd10m': 10.4, 'wspd20m': 13.4,
            'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
            'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
            'swh': 10.0, 'swp': 1.4, 'swd': "W",
            'pres': 1.8, 'ptdy': 1.8,
            'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
            'time': '09:34:00', 'dd': now.day, 'mm': now.month, 'year': now.year
        },
        "station": "TestStationID",
        "description": "Test Description",
        "valid": True,
        "location": {
            "latitude": 36.0,
            "longitude": -75.34
        }
    }
    
    buoy = Buoy.from_json(original_json)
    
    assert buoy.present is not None
    assert buoy.station == original_json["station"]
    assert buoy.description == original_json["description"]
    assert buoy.valid
    assert buoy.location is not None        


def test_buoy_json_not_all_available():
    '''Test setting a buoy object from json where fields are missing'''
    original_json = {
        "station": "TestStationID",
        "valid": True,
        "location": {
            "latitude": 36.0,
            "longitude": -75.34
        }
    }
    
    buoy = Buoy.from_json(original_json)
    
    assert buoy.present is None
    assert buoy.station == original_json["station"]
    assert buoy.valid
    assert buoy.location is not None        


def test_buoy_json_not_all_available_no_station():
    '''Test setting a buoy object from json where station is misisng
    throwing an error
    '''
    original_json = {
        "valid": True,
        "location": {
            "latitude": 36.0,
            "longitude": -75.34
        }
    }
    
    with pytest.raises(KeyError):
        buoy = Buoy.from_json(original_json)


def test_source_json_all_available():
    '''Test setting a source object from json'''

    now = datetime.now().replace(tzinfo=timezone.utc)
    original_json = {
        "buoys": [
            {
                "station": "TestBuoy",
                "data": {
                    'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                    'wspd10m': 10.4, 'wspd20m': 13.4,
                    'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                    'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                    'swh': 10.0, 'swp': 1.4, 'swd': "W",
                    'pres': 1.8, 'ptdy': 1.8,
                    'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                    'time': '09:34:00', 'dd': now.day, 'mm': now.month, 'year': now.year
                }            
            }
        ],
        "name": "TestSource",
        "description": "Test Source"
    }
    
    source = Source.from_json(original_json)
    
    assert len(source.buoys) == 1
    assert source.name == original_json["name"]
    assert source.description == original_json["description"]
    
    new_src = Source.from_json(source.to_json())
    assert len(new_src.buoys) == 1
    assert new_src.name == source.name
    assert new_src.description == source.description


def test_source_json_missing_name():
    '''Test setting a source object from json'''

    now = datetime.now().replace(tzinfo=timezone.utc)
    original_json = {
        "buoys": [
            {
                "station": "TestBuoy",
                "data": {
                    'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                    'wspd10m': 10.4, 'wspd20m': 13.4,
                    'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                    'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                    'swh': 10.0, 'swp': 1.4, 'swd': "W",
                    'pres': 1.8, 'ptdy': 1.8,
                    'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                    'time': '09:34:00', 'dd': now.day, 'mm': now.month, 'year': now.year
                }            
            }
        ],
        "description": "Test Source"
    }
    
    with pytest.raises(KeyError):
        source = Source.from_json(original_json)
    

if __name__ == '__main__':
    test_buoy_data_json_all_available()