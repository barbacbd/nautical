from .base import NCEIBase


class Dataset(NCEIBase):

    """
    All of the CDO data are in datasets. The containing dataset must be known before attempting to 
    access its data.
    
    Additional Parameters
    
        datatypeid [Optional]
            Accepts a valid data type id or a chain of data type ids separated by ampersands. Datasets 
            returned will contain all of the data type(s) specified
        locationid [Optional]
            Accepts a valid location id or a chain of location ids separated by ampersands. Datasets 
            returned will contain data for the location(s) specified
        stationid [Optional]
            Accepts a valid station id or a chain of of station ids separated by ampersands. Datasets 
            returned will contain data for the station(s) specified
        startdate [Optional] 
            Accepts valid ISO formated date (yyyy-mm-dd). Datasets returned will have data after the 
            specified date. Paramater can be use independently of enddate
        enddate [Optional] 
            Accepts valid ISO formated date (yyyy-mm-dd). Datasets returned will have data before the 
            specified date. Paramater can be use independently of startdate
        sortfield [Optional]
            The field to sort results by. Supports id, name, mindate, maxdate, and datacoverage fields
        sortorder [	Optional]
            Which order to sort by, asc or desc. Defaults to asc
        limit [Optional]
            Defaults to 25, limits the number of results in the response. Maximum is 1000
        offset [Optional]
            Defaults to 0, used to offset the resultlist. The example would begin with record 24
    """
    parameters = (
        "datatypeid",
        "locationid",
        "stationid",
        "startdate",
        "enddate",
        "sortfield",
        "sortorder",
        "limit",
        "offset"
    )
    
    endpoint = NCEIBase.endpoint + "datasets"

    __slots__ = ['uid', 'mindate', 'maxdate', 'name', 'datacoverage', 'id']
