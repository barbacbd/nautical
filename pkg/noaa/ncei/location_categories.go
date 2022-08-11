package ncei

var (
	// The data endpoint is used for actually fetching the location categories.
	LocationCategoryEndpoint = AddToEndpoint(BaseEndpoint, "locationcategories")

	// Valid Query Parameters
	LocationCategoryParameters = []string{
		// datasetid [Optional]
		// Accepts a valid dataset id or a chain of dataset ids separated by ampersands.
		// Data returned will be supported by dataset(s) specified
		"datasetid",

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

type LocationCategory struct {
	Name string `json:"name,omitempty"`
	ID   string `json:"id,omitempty"`
}
