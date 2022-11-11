'''No matter what system is used, the cache should be save to the 
correct/known location provided by this module.
'''
from appdirs import user_cache_dir
from datetime import datetime, timezone
from enum import Enum
from json import load as jload, dump as jdump
from os.path import join, exists
from os import mkdir, remove, getenv
from ..log import get_logger
from ..time import get_time_str
from ..noaa.buoy import Source, Buoy


log = get_logger()
log.warning("First time imports should call nautical.cache.setup()")

__CACHE_FILE = "nautical_cache.json"
NAUTICAL_CACHE_DIR = getenv("NAUTICAL_CACHE_DIR", user_cache_dir("nautical"))

NAUTICAL_CACHE_FILE = join(NAUTICAL_CACHE_DIR, __CACHE_FILE)


class CacheData(Enum):
    '''Describes the type of data that the user wants
    to retrieve from the CACHE
    '''
    ALL = 0
    BUOYS = 1
    SOURCES = 2
    TIME = 3


def setup():
    '''Create the cache directory if it does not exist/
    '''
    if not exists(NAUTICAL_CACHE_DIR):
        mkdir(NAUTICAL_CACHE_DIR)


def copy_current_cache(extra_name_data):
    '''Copy the current nautical cache file and append the extra_data.
    
    :return: Filename on success, None otherwise
    '''
    if not exists(NAUTICAL_CACHE_FILE):
        return None
    
    copied_name = NAUTICAL_CACHE_FILE
    copied_name = copied_name.replace(".json", extra_name_data) + ".json"

    with open(NAUTICAL_CACHE_FILE.replace("\\", "/"), "r") as readFile:
        with open(copied_name, "w+") as writeFile:
            writeFile.write(readFile.read())

    return copied_name


def copy_current_cache_with_timestamp():
    '''Apply timestamp to the name of the nautical cache
    '''
    now = datetime.now().replace(tzinfo=timezone.utc)
    return copy_current_cache(now.strftime("%Y-%m-%d_%H-%M-%S"))


def _convert_to_keys(output_type):
    '''Convert the CacheData type to string keys required for output
    '''
    if output_type == CacheData.ALL:
        return [x.name for x in CacheData if x != CacheData.ALL]
    return [output_type.name]


def load(filename=NAUTICAL_CACHE_FILE, cached_output=CacheData.ALL):
    '''Load the nautical cache if it exists. All nautical data is returned as nautical objects
    in the dictionary. Time is provided as a string.
    
    :param filename: Name of the file containing cached data.
    :param cached_output: CacheData enumeration type. What type of information to retrieve
    :return: Dictionary containing all cached output
    '''
    if not exists(filename):
        return {}
    
    with open(filename, "rb") as cache_file:
        cache = jload(cache_file)
    
    converted = _convert_to_keys(cached_output)

    output = {}    
    for key, value in cache.items():
        if key in converted:
            if key == CacheData.BUOYS.name: output[key] = [Buoy.from_json(buoy_data) for buoy_data in value]
            elif key == CacheData.SOURCES.name: output[key] = [Source.from_json(src_data) for src_data in value]
            elif key == CacheData.TIME.name: output[key] = value
            else: log.warning("Skip loading key: %s", key)
    return output


def dumps(data, filename=NAUTICAL_CACHE_FILE):
    '''Overwrite the current value of the NAUTICAL_CACHE_FILE
    with the current contents of data. The data should be passed in should
    be provided as nautical objects for buoys and sources.
    
    :param data: Dictionary containing buoys and sources with the keys to match
    :param filename: name of the file where the data will be stored
    '''
    if exists(filename):
        log.warning("Overwriting contents of %s", filename)
        remove(filename)
    
    if not isinstance(data, dict):
        raise TypeError("dumps requires data to be a dictionary")

    _data = {}
    _data[CacheData.TIME.name] = get_time_str()
    
    if CacheData.BUOYS.name in data:
        _data[CacheData.BUOYS.name] = [
            buoy.to_json() for buoy in data[CacheData.BUOYS.name]
        ]
    
    if CacheData.SOURCES.name in data:
        _data[CacheData.SOURCES.name] = [
            source.to_json() for source in data[CacheData.SOURCES.name]
        ]
        
    with open(filename, "w+") as cache_file:
        jdump(_data, cache_file, indent=4)
