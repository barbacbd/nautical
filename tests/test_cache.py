from os.path import exists, join
from os import remove, listdir, environ
import pytest
from shutil import rmtree


environ["NAUTICAL_CACHE_DIR"] = "nautical_cache_tests"

# Load anything associated with nautical after env vars are set
from nautical.cache import *
from nautical.cache.file import NAUTICAL_CACHE_DIR, NAUTICAL_CACHE_FILE
from nautical.noaa.buoy import Buoy, Source



@pytest.mark.first
def test_setup():
    '''Test the correct creation of the cache directory'''
    
    setup()
    assert exists(NAUTICAL_CACHE_DIR)


@pytest.mark.order(3)
def test_copy_current_cache():
    '''Copy the contents of the current nautical cache file to another file
    '''
    filename = copy_current_cache("EXAMPLE")
    found = [join(NAUTICAL_CACHE_DIR, x) for x in listdir(NAUTICAL_CACHE_DIR)]
    assert filename in found   
    
    if exists(filename):
        remove(filename) 

@pytest.mark.order(4)
def test_copy_current_cache_ts():
    '''Copy the contents of the nautical cache file to a file with a timestamp
    '''
    filename = copy_current_cache_with_timestamp()
    found = [join(NAUTICAL_CACHE_DIR, x) for x in listdir(NAUTICAL_CACHE_DIR)]
    assert filename in found
    
    if exists(filename):
        remove(filename) 


@pytest.mark.order(5)    
def test_load(subtests):
    '''Test loading the Data from the cache file that was dumped to
    in the previous test
    '''
    tmp_filename = join(NAUTICAL_CACHE_DIR, "NAUTICAL_TEST_CACHE.json")
    if not exists(tmp_filename):
        tmp_filename = NAUTICAL_CACHE_FILE
    
    with open(tmp_filename, "rb") as data:
        print(data.read)
    
    data = load(tmp_filename)
    
    assert len(data["SOURCES"]) > 0  # test that they are present
    for src in data["SOURCES"]:
        with subtests.test(src=src):
            assert isinstance(src, Source)

    assert len(data["BUOYS"]) > 0  # test that they are present
    for buoy in data["BUOYS"]:
        with subtests.test(buoy=buoy):
            assert isinstance(buoy, Buoy)
    
    assert data.get("TIME", None) is not None


@pytest.mark.order(2)    
def test_dumps():
    '''Test dumping data to the the nautical cache file.
    DON'T OVERWRITE current cache
    '''
    tmp_filename = NAUTICAL_CACHE_FILE
    if exists(NAUTICAL_CACHE_FILE):
        tmp_filename = join(NAUTICAL_CACHE_DIR, "NAUTICAL_TEST_CACHE.json")
    
    buoy1 = Buoy.from_json(
        {   
                "data": {
                    'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                    'wspd10m': 10.4, 'wspd20m': 13.4,
                    'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                    'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                    'swh': 10.0, 'swp': 1.4, 'swd': "W",
                    'pres': 1.8, 'ptdy': 1.8,
                    'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                    'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
                },
                "station": "TestStationID",
                "description": "Test Description",
                "valid": True,
                "location": {
                    "latitude": 36.0,
                    "longitude": -75.34
                }
            }
    )
    
    buoy2 = Buoy.from_json(
        {   
                "data": {
                    'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                    'wspd10m': 10.4, 'wspd20m': 13.4,
                    'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                    'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                    'swh': 10.0, 'swp': 1.4, 'swd': "W",
                    'pres': 1.8, 'ptdy': 1.8,
                    'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                    'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
                },
                "station": "TestStationID",
                "description": "Test Description",
                "valid": True,
                "location": {
                    "latitude": 36.0,
                    "longitude": -75.34
                }
            }
    )
    
    source1 = Source.from_json(
        {
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
                        'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
                    }            
                }
            ],
            "name": "TestSource",
            "description": "Test Source"
        }
    )
    source2 = Source.from_json(
        {
            "buoys": [
                {
                    "station": "TestBuoy2",
                    "data": {
                        'wdir': "ESE", 'wspd': 10.2, 'gst': 15.9,
                        'wspd10m': 10.4, 'wspd20m': 13.4,
                        'wvht': 2.5, 'dpd': 2.5, 'apd': 2.5,
                        'mwd': "E", 'wwh': 3.5, 'wwp': 7, 'wwd': "ESE",
                        'swh': 10.0, 'swp': 1.4, 'swd': "W",
                        'pres': 1.8, 'ptdy': 1.8,
                        'atmp': 76.5, 'wtmp': 65.3, 'otmp': 65.3, 'dewp': 85.0,
                        'time': '09:34:00', 'dd': 10, 'mm': 1, 'year': 2020
                    }            
                }
            ],
            "name": "TestSource2",
            "description": "Test Source 2"
        }
    )
    
    tmp_data = {
        CacheData.BUOYS.name: [buoy1, buoy2],
        CacheData.SOURCES.name: [source1, source2]
    }
    
    dumps(tmp_data, tmp_filename)
    assert exists(tmp_filename)


@pytest.mark.order(6)    
def test_load_time():
    '''Test loading the Data from the cache file that was dumped to
    in the previous test. Only grab the time
    '''
    tmp_filename = join(NAUTICAL_CACHE_DIR, "NAUTICAL_TEST_CACHE.json")
    if not exists(tmp_filename):
        tmp_filename = NAUTICAL_CACHE_FILE
    
    with open(tmp_filename, "rb") as data:
        print(data.read)
    
    data = load(tmp_filename, CacheData.TIME)

    assert CacheData.SOURCES.name not in data
    assert CacheData.BUOYS.name not in data    
    assert data.get("TIME", None) is not None


@pytest.mark.order(7)    
def test_load_time(subtests):
    '''Test loading the Data from the cache file that was dumped to
    in the previous test. Only grab the buoys
    '''
    tmp_filename = join(NAUTICAL_CACHE_DIR, "NAUTICAL_TEST_CACHE.json")
    if not exists(tmp_filename):
        tmp_filename = NAUTICAL_CACHE_FILE
    
    with open(tmp_filename, "rb") as data:
        print(data.read)
    
    data = load(tmp_filename, CacheData.BUOYS)

    assert CacheData.SOURCES.name not in data
    assert CacheData.TIME.name not in data
    
    assert len(data["BUOYS"]) > 0  # test that they are present
    for buoy in data["BUOYS"]:
        with subtests.test(buoy=buoy):
            assert isinstance(buoy, Buoy)  


@pytest.mark.last
def test_remove_tmp_files():
    '''Remove any temporary files that were created during testing
    '''    
    if exists(NAUTICAL_CACHE_DIR):
        rmtree(NAUTICAL_CACHE_DIR)
    
    assert not exists(NAUTICAL_CACHE_DIR)
