from .base import NCEIBase


class Location(NCEIBase):

    """
    Locations can be a specific latitude/longitude point such as a station, or a label representing a
    bounding area such as a city.
    
    Additional Parameters
    
        datasetid [Optional] 
            Accepts a valid dataset id or a chain of dataset ids separated by ampersands. Locations 
            returned will be supported by dataset(s) specified
        locationcategoryid [Optional]
            Accepts a valid location id or a chain of location category ids separated by ampersands.
            Locations returned will be in the location category(ies) specified.
        datacategoryid [Optional] 
            Accepts a valid data category id or an array of data category ids. Locations returned will 
            be associated with the data category(ies) specified
        startdate [Optional] 
            Accepts valid ISO formated date (yyyy-mm-dd). Locations returned will have data after the 
            specified date. Paramater can be use independently of enddate
        enddate [Optional] 
            Accepts valid ISO formated date (yyyy-mm-dd). Locations returned will have data before the 
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
        "datasetid",
        "locationcategoryid",
        "datacategoryid",
        "startdate",
        "enddate",
        "sortfield",
        "sortorder",
        "limit",
        "offset"
    )
    
    endpoint = NCEIBase.endpoint + "locations"

    __slots__ = ['mindate', 'maxdate', 'name', 'datacoverage', 'id']
