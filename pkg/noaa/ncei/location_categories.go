package ncei

var (
	// LocationCategoryEndpoint is the endpoint is used for fetching the location categories.
	LocationCategoryEndpoint = AddToEndpoint(BaseEndpoint, "locationcategories")

	// LocationCategoryParameters contains the valid query parameter names for Location Categories
	LocationCategoryParameters = []string{
		// datasetid [Optional]
		// Accepts a valid dataset id or a chain of dataset ids separated by ampersands.
		// Data returned will be supported by dataset(s) specified
		"datasetid",

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

// LocationCategory is a structure that contains the resulting location category data after a query is processed.
type LocationCategory struct {
	Name string `json:"name,omitempty"`
	ID   string `json:"id,omitempty"`
}
