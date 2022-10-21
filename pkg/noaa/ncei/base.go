package ncei

// NCEI is a work in progress

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strconv"
	"strings"
	"time"
)

type QueryType int

const (
	MaxResultLimit int    = 1000
	BaseEndpoint   string = "https://www.ncei.noaa.gov/cdo-web/api/v2/"
	requestsPerSec int    = 5

	DataType QueryType = iota
	DataCategoryType
	DatasetType
	DatatypeType
	LocationCategoryType
	LocationType
	StationType
)

type NCEIBase interface {
	// ConvertToType will convert the resultant strings from the Query functions
	// to the interface type including Data, DataCategory, DataSet, Datatype,
	// LocationCategory, Location, and Station
	ConvertToType(results []string) []interface{}
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

// getQueryData will get the endpoint and the parameters associated with the provided query type.
func getQueryData(t QueryType) (string, []string, error) {
	switch {
	case t == DataType:
		return DataEndpoint, DataParameters, nil
	case t == DataCategoryType:
		return DataCategoryEndpoint, DataCategoryParameters, nil
	case t == DatasetType:
		return DatasetEndpoint, DatasetParameters, nil
	case t == DatatypeType:
		return DatatypeEndpoint, DatatypeParameters, nil
	case t == LocationCategoryType:
		return LocationCategoryEndpoint, LocationCategoryParameters, nil
	case t == LocationType:
		return LocationEndpoint, LocationParameters, nil
	case t == StationType:
		return StationEndpoint, StationParameters, nil
	}

	return "", nil, fmt.Errorf("no matching query type: %d", int(t))
}

// QueryBase will query the API provided with the correct endpoint and authentication token.
// returns a json encoded result of the query
func QueryBase(token string, endpoint string, limit int, offset int) ([]string, error) {

	params := url.Values{}
	params.Add("limit", strconv.Itoa(limit))
	params.Add("offset", strconv.Itoa(offset))

	client := &http.Client{}
	req, err := http.NewRequest("GET", endpoint, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Add("limit", strconv.Itoa(limit))
	req.Header.Add("offset", strconv.Itoa(offset))
	req.Header.Add("Token", token)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()
	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return nil, nil
}

// QueryAll will query the endpoint stored in the struct that is passed through
// the interface. The list of parameters are used to establish a full endpoint
// where the query will return a list of json strings.
func QueryAll(token string, qt QueryType, parameters []Parameter) ([]string, error) {
	var results []string

	baseEndpoint, baseParameters, err := getQueryData(qt)
	if err != nil {
		return nil, err
	}

	endpoint := addParamsToEndpoint(baseEndpoint, baseParameters, parameters)
	count, err := GetNumResults(token, endpoint)
	if err != nil {
		return nil, err
	}

	offsets, err := CreateOffsetLookups(count)
	if err != nil {
		return results, nil
	}

	i := 0
	var startTime time.Time
	for key, value := range offsets {
		if i == 0 {
			startTime = time.Now()
		}

		baseQueryResults, err := QueryBase(token, endpoint, value, key)
		if err != nil {
			// log the error
		} else {
			results = append(results, baseQueryResults...)
		}

		// Even when a request failed, the request is counted against the
		// number allowed per second with a token.
		i = (i + 1) % requestsPerSec
		if i == 0 {
			diffTime := time.Now().Sub(startTime)
			if diffTime.Seconds() < 1 {
				// Sleep the difference to make sure that the requests do not get skipped
				time.Sleep(time.Duration(diffTime.Milliseconds()) * time.Millisecond)
			}

			// reset the time
			startTime = time.Now()
		}
	}

	return results, nil
}
