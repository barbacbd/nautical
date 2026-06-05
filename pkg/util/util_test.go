package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetAliases(t *testing.T) {
	// Define a test struct with various json tags
	type TestStruct struct {
		Field1 string  `json:"field1"`
		Field2 int     `json:"field2"`
		Field3 bool    `json:"field3,omitempty"`
		Field4 float64 // No json tag - uses field name
		Field5 string  `json:"-"` // Should be excluded
	}

	aliases := GetAliases(TestStruct{})

	// Verify aliases are extracted correctly
	assert.Contains(t, aliases, "field1", "Field with json tag should be included")
	assert.Contains(t, aliases, "field2", "Field with json tag should be included")
	assert.Contains(t, aliases, "field3", "Field with omitempty should be included")

	// Field4 has no json tag - implementation uses field name
	assert.Contains(t, aliases, "Field4", "Field without json tag uses field name")

	// Field5 has json:"-", should be excluded
	assert.NotContains(t, aliases, "-", "Excluded field should not be in aliases")
	assert.NotContains(t, aliases, "Field5", "Excluded field should not use field name")

	// Verify the count (field1, field2, field3, Field4)
	assert.Equal(t, 4, len(aliases))
}

func TestGetAliasesEmpty(t *testing.T) {
	// Test with struct that has no fields
	type EmptyStruct struct {
	}

	aliases := GetAliases(EmptyStruct{})

	// Should be empty since struct has no fields
	assert.Empty(t, aliases)
}

func TestGetAliasesNoJsonTags(t *testing.T) {
	// Test with struct that has no json tags - uses field names
	type NoTagStruct struct {
		NoTag1 string
		NoTag2 int
	}

	aliases := GetAliases(NoTagStruct{})

	// Fields without json tags use field names
	assert.Contains(t, aliases, "NoTag1")
	assert.Contains(t, aliases, "NoTag2")
	assert.Equal(t, 2, len(aliases))
}

func TestGetAliasesNested(t *testing.T) {
	// Test with nested struct
	type NestedStruct struct {
		Name  string `json:"name"`
		Value int    `json:"value"`
	}

	type ParentStruct struct {
		ID     string       `json:"id"`
		Nested NestedStruct `json:"nested"`
	}

	aliases := GetAliases(ParentStruct{})

	// Should only get aliases from the parent struct
	assert.Contains(t, aliases, "id")
	assert.Contains(t, aliases, "nested")

	// Should not traverse into nested struct
	assert.NotContains(t, aliases, "name")
	assert.NotContains(t, aliases, "value")
}
