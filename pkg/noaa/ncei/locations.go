package ncei

var (
	// The data endpoint is used for actually fetching the locations.
	LocationEndpoint = AddToEndpoint(BaseEndpoint, "locations")

	// Valid Query Parameters
	LocationParameters = []string{
		// datasetid [Optional]
		// Accepts a valid dataset id or a chain of dataset ids separated by ampersands.
		// Data returned will be supported by dataset(s) specified
		"datasetid",

		// locationcategoryid [Optional]
		// Accepts a valid location id or a chain of location category ids separated by
		// ampersands.Locations returned will be in the location category(ies) specified.
		"locationcategoryid",

		// datacategoryid [Optional]
		// Accepts a valid data category id or an array of data category ids. Locations
		// returned will be associated with the data category(ies) specified
		"datacategoryid",

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

type Location struct {
	MinDate      string `json:"mindate,omitempty"`
	MaxDate      string `json:"maxdate,omitempty"`
	Name         string `json:"name,omitempty"`
	DataCoverage string `json:"datacoverage,omitempty"`
	ID           string `json:"id,omitempty"`
}
