package util

import (
	"reflect"
	"strings"
)

// StringSet is a set of strings backed by a map.
type StringSet map[string]struct{}

// Has returns true if the set contains the given item.
func (s StringSet) Has(item string) bool {
	_, ok := s[item]
	return ok
}

func GetAliases(iface interface{}) StringSet {
	aliasSet := make(StringSet)
	val := reflect.ValueOf(iface)
	for i := 0; i < val.Type().NumField(); i++ {
		tag := val.Type().Field(i)
		fieldName := tag.Name

		switch jsonTag := tag.Tag.Get("json"); jsonTag {
		case "-":
			// skip
		case "":
			aliasSet[fieldName] = struct{}{}
		default:
			parts := strings.Split(jsonTag, ",")
			name := parts[0]
			if name == "" {
				name = fieldName
			}
			aliasSet[name] = struct{}{}
		}
	}
	return aliasSet
}
