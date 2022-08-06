package ncei

import (
	"encoding/json"
	"fmt"
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"strings"
)

// GetToken - Provide a yaml, json, or text.
// For yaml files, the file must contain the keyword `token` followed by the token,
// token: {{ token }}
// For json files, the file must contain the keyword `token` followed by the token,
// {"token": {{ token }} }
// [Default Behavior]:
// For text files, simply copy the token into the file.
// This file does not need to be considered a secret. Follow the link below
// to generate your unique (one time) token.
// `https://www.ncdc.noaa.gov/cdo-web/token`
// The usage of a token is limited to 5 times per second, and 10,000
// times per day according to the noaa website.
func GetToken(filename string) (string, error) {

	// Calling function to parse the data
	var parser func([]byte, any) error

	switch {
	case strings.HasSuffix(filename, ".json"):
		parser = json.Unmarshal
	case strings.HasSuffix(filename, ".yaml"):
		parser = yaml.Unmarshal
	}

	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", err
	}

	if parser != nil {
		var results map[string]interface{}
		err := parser(data, &results)
		if err != nil {
			return "", err
		}

		token, ok := results["token"]
		if !ok {
			return "", fmt.Errorf("failed to find token in %s", filename)
		}
		return fmt.Sprintf("%v", token), nil

	}

	// Assumes text in file
	return string(data[:]), err
}
