package ncei

var (
	// The data endpoint is used for actually fetching the data.
	DataEndpoint = AddToEndpoint(BaseEndpoint, "data")

	// Valid Query Parameters
	DataParameters = []string{
		// datasetid [Optional]
		// Accepts a valid dataset id or a chain of dataset ids separated by ampersands.
		// Data returned will be supported by dataset(s) specified
		"datasetid",

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

		// units [Optional]
		// Accepts the literal strings 'standard' or 'metric'. Data will be scaled and converted
		// to the specified units. If a unit is not provided then no scaling nor conversion
		// will take place.
		"units",

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

		// includemetadata [Optional]
		// Defaults to true, used to improve response time by preventing the calculation
		// of result metadata.
		"includemetadata",
	}
)

type Data struct {
	Date       string `json:"date,omitempty"`
	Datatype   string `json:"datatype,omitempty"`
	Station    string `json:"station,omitempty"`
	Attributes string `json:"attributes,omitempty"`
	Value      int    `json:"value,omitempty"`
}
