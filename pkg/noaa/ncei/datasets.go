package ncei

var (
	// The data endpoint is used for actually fetching the datasets.
	DatasetEndpoint = AddToEndpoint(BaseEndpoint, "datasets")

	// Valid Query Parameters
	DatasetParameters = []string{
		// datatypeid [Optional]
		// Accepts a valid data type id or a chain of data type ids separated by ampersands.
		// Data returned will contain all of the data type(s) specified
		"datatypeid",

		// locationid [Optional]
		// Accepts a valid location id or a chain of location ids separated by ampersands.
		// Data returned will contain data for the location(s) specified
		"locationid",

		// stationid [Optional]
		// Accepts a valid station id or a chain of of station ids separated by ampersands.
		// Data returned will contain data for the station(s) specified
		"stationid",

		// startdate [Optional]
		// Accepts valid ISO formated date (yyyy-mm-dd). Data returned will have data after
		// the specified date. Paramater can be use independently of enddate
		"startdate",

		// enddate [Optional]
		// Accepts valid ISO formated date (yyyy-mm-dd). Data returned will have data before the
		// specified date. Paramater can be use independently of startdate
		"enddate",

		//sortfield [Optional]
		// The field to sort results by. Supports id, name, mindate, maxdate, and datacoverage
		// fields
		"sortfield",

		// sortorder [	Optional]
		// Which order to sort by, asc or desc. Defaults to asc
		"sortorder",

		// limit [Optional]
		// Defaults to 25, limits the number of results in the response. Maximum is 1000
		"limit",

		// offset [Optional]
		// Defaults to 0, used to offset the resultlist. The example would begin with record 24
		"offset",
	}
)

type Dataset struct {
	UID          string `json:"uid,omitempty"`
	MinDate      string `json:"mindate,omitempty"`
	MaxDate      string `json:"maxdate,omitempty"`
	Name         string `json:"name,omitempty"`
	DataCoverage string `json:"datacoverage,omitempty"`
	ID           string `json:"id,omitempty"`
}
