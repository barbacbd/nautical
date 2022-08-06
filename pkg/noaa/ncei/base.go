package ncei

import (
	"fmt"
	"strings"
)

const (
	MaxResultLimit int    = 1000
	BaseEndpoint   string = "https://www.ncei.noaa.gov/cdo-web/api/v2/"
)

type NCEIBase interface {
	// QueryAll will query the endpoint stored in the struct that is passed through
	// the interface. The list of parameters are used to establish a full endpoint
	// where the query will return a list of json strings.
	QueryAll(token string, parameters []Parameter) ([]string, error)

	// QueryBase will query the API provided with the correct endpoint and authentication token.
	// returns a json encoded result of the query
	QueryBase(token string, endpoint string, limit int, offset int) (string, error)
}

func AddToEndpoint(endpoint string, next string) string {
	return fmt.Sprintf("%s%s", endpoint, next)
}

// GetNumResults will query the API provided with the correct endpoint and authentication
// token to find the number of possible results from a query.
// returns the number of results from the query
func GetNumResults(token string, endpoint string) (int, error) {
	return 0, nil
}

// addParamsToEndpoint will add the parameters to the endpoint if they are valid
func addParamsToEndpoint(endpoint string, allowedParams []string, userParams []Parameter) string {
	combined := combineParameters(allowedParams, userParams)
	if combined != "" {
		return fmt.Sprintf("%s?%s", endpoint, combined)
	}
	return endpoint
}

// combineParameters combines all valid parameters into a single string.
func combineParameters(allowedParams []string, userParams []Parameter) string {

	var useableParams []string

	for _, param := range userParams {
		if func(allowedParams []string, paramName string) bool {
			for _, allowed := range allowedParams {
				if allowed == paramName {
					return true
				}
			}
			return false
		}(allowedParams, param.Name) {
			useableParams = append(useableParams, param.String())
		}
	}

	if useableParams != nil {
		return strings.Join(useableParams, "&")
	}

	return ""
}

// CreateOffsetLookups will create a dictionary that maps the offset to the number to search.
// The count passed is in the number of results returned from `GetNumResults`
func CreateOffsetLookups(count int) (map[int]int, error) {
	lookups := make(map[int]int)

	if count < 0 {
		return lookups, fmt.Errorf("count must be greater or equal to 0: %d", count)
	}

	numFull := count / MaxResultLimit
	numLeft := count % MaxResultLimit
	offsets := 1

	// Set a max value for all full sets
	for i := 0; i < numFull; i++ {
		lookups[offsets] = MaxResultLimit
		offsets += MaxResultLimit
	}

	// Add in any leftover values
	if numLeft > 0 {
		lookups[offsets] = numLeft
	}

	return lookups, nil
}

// query is the base/common function for all queries and is internal to this package.
func query(token string, endpoint string, limit int, offset int) (string, error) {
	return "", nil
}
