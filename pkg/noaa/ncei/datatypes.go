package ncei

var (
	// DatatypeEndpoint is the endpoint is used for fetching the data types.
	DatatypeEndpoint = AddToEndpoint(BaseEndpoint, "datatypes")

	// DatatypeParameters contains the valid query parameter names for Data Types
	DatatypeParameters = []string{
		// datasetid [Optional]
		// Accepts a valid dataset id or a chain of dataset ids separated by ampersands.
		// Data returned will be supported by dataset(s) specified
		"datasetid",

		// locationid [Optional]
		// Accepts a valid location id or a chain of location ids separated by ampersands.
		// Data returned will contain data for the location(s) specified
		"locationid",

		// stationid [Optional]
		// Accepts a valid station id or a chain of station ids separated by ampersands.
		// Data returned will contain data for the station(s) specified
		"stationid",

		// datacategoryid [Optional]
		// Accepts a valid data category id or a chain of data category ids separated by
		// ampersands (although it is rare to have a data type with more than one data category).
		// Data types returned will be associated with the data category(ies) specified
		"datacategoryid",

		// startdate [Optional]
		// Accepts valid ISO formatted date (yyyy-mm-dd). Data returned will have data after
		// the specified date. parameter can be use independently of enddate
		"startdate",

		// enddate [Optional]
		// Accepts valid ISO formatted date (yyyy-mm-dd). Data returned will have data before the
		// specified date. parameter can be use independently of startdate
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
		// Defaults to 0, used to offset the result list. The example would begin with record 24
		"offset",
	}
)

// Datatype is a structure that contains the resulting data type data after a query is processed.
type Datatype struct {
	MinDate      string `json:"mindate,omitempty"`
	MaxDate      string `json:"maxdate,omitempty"`
	Name         string `json:"name,omitempty"`
	DataCoverage string `json:"datacoverage,omitempty"`
	ID           string `json:"id,omitempty"`
}