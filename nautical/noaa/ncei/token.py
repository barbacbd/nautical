from json import load
from os.path import abspath, dirname, join, exists
from yaml import safe_load
from nautical.log import get_logger


log = get_logger()
_default_token_file = join(dirname(abspath(__file__)), "token.yaml")


def _load_from_yaml(filename):
    '''Search for the token in the yaml file
    '''
    with open(filename, "r", encoding="utf-8") as token_file:
        yaml_data = safe_load(token_file)

    return yaml_data.get("token", None)


def _load_from_json(filename):
    '''Search for the token in the json file
    '''
    with open(filename, "r", encoding="utf-8") as token_file:
        json_data = load(token_file)

    return json_data.get("token", None)


def get_default_token():
    '''Parse the default token information'''
    log.warning("Using the default token file.")
    return _load_from_yaml(_default_token_file)


def get_token(filename=_default_token_file):
    '''Provide a yaml, json, or text.

    For yaml files, the file must contain the keyword `token` followed by the token,
    token: {{ token }}

    For json files, the file must contain the keywork `token` follwed by the token,
    {"token": {{ token }} }

    [Default Behavior]:
    For text files, simply copy the token into the file.

    This file does not need to be considered a secret. Follow the link below 
    to generate your unique (one time) token.
    `https://www.ncdc.noaa.gov/cdo-web/token`

    The usage of a token is limitted to 5 times per second, and 10,000
    times per day according to the noaa website. 

    :param filename: file containing the token data
    :return: token contained in the file if exists, otherwise None
    '''
    if not exists(filename):
        log.error("Failed to find %s", filename)
        return None

    if filename.endswith(".yaml"):
        if filename == _default_token_file:
            return get_default_token()
        return _load_from_yaml(filename)

    if filename.endswith(".json"):
        return _load_from_json(filename)

    if not filename.endswith(".txt"):
        log.warning("assuming %s is a txt file", filename)

    with open(filename, "r", encoding="utf-8") as token_file:
        data = token_file.read()
    return data
