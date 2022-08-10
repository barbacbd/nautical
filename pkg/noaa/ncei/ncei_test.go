package ncei

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"testing"
)

var (
	testEndpoint = "https://test.endpoint.com"
)

func TestOffset(t *testing.T) {
	tests := []struct {
		name         string
		count        int
		expectedLen  int
		expectedLeft int
		expectedErr  string
	}{{
		name:        "Negative Offset",
		count:       -1,
		expectedErr: "count must be greater or equal to 0: -1",
	}, {
		name:  "Test Zero Offest",
		count: 0,
	}, {
		name:         "Test Offset Not Enough Too Fill",
		count:        565,
		expectedLen:  1,
		expectedLeft: 565,
	}, {
		name:         "Test Offset Enough Too Fill",
		count:        1001,
		expectedLen:  2,
		expectedLeft: 1,
	}, {
		name:         "Test Offset Enough Too Fill Large",
		count:        10043,
		expectedLen:  11,
		expectedLeft: 43,
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			offsets, err := CreateOffsetLookups(tc.count)
			if err != nil && tc.expectedErr != "" {
				assert.Equal(t, tc.expectedErr, err.Error())
			} else {
				assert.Equal(t, tc.expectedLen, len(offsets))

				if len(offsets) > 0 {
					maxKey := func(offsets map[int]int) int {
						// key will never be less that 0
						maxKey := -1

						for key, _ := range offsets {
							if key > maxKey {
								maxKey = key
							}
						}

						return maxKey
					}(offsets)

					assert.Equal(t, offsets[maxKey], tc.expectedLeft)
				}
			}
		})
	}
}

func TestAddToEndpoint(t *testing.T) {
	tests := []struct {
		name          string
		allowedParams []string
		userParams    []Parameter
		expected      string
	}{{
		name:     "Base Endpoint No Parameters",
		expected: testEndpoint,
	}, {
		name: "No Allowed Params",
		userParams: []Parameter{
			{Name: "test1", Value: "test1"},
			{Name: "test2", Value: "test2"},
		},
		expected: testEndpoint,
	}, {
		name:          "Single Allowed Params",
		allowedParams: []string{"test1"},
		userParams: []Parameter{
			{Name: "test1", Value: "test1"},
			{Name: "test2", Value: "test2"},
		},
		expected: fmt.Sprintf("%s?test1=test1", testEndpoint),
	}, {
		name:          "Multiple Allowed Params",
		allowedParams: []string{"test1", "test3"},
		userParams: []Parameter{
			{Name: "test1", Value: "test1"},
			{Name: "test2", Value: "test2"},
			{Name: "test3", Value: "test3"},
		},
		expected: fmt.Sprintf("%s?test1=test1&test3=test3", testEndpoint),
	}, {
		name:          "Mulitple Allowed Params Find One",
		allowedParams: []string{"test1", "test3"},
		userParams: []Parameter{
			{Name: "test1", Value: "test1"},
			{Name: "test2", Value: "test2"},
		},
		expected: fmt.Sprintf("%s?test1=test1", testEndpoint),
	}}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			result := addParamsToEndpoint(testEndpoint, tc.allowedParams, tc.userParams)
			assert.Equal(t, tc.expected, result)
		})
	}
}
