package util

import (
    "reflect"
    "strings"

    "k8s.io/apimachinery/pkg/util/sets"
)

func GetAliases(iface interface{}) sets.Set[string] {
	aliasSet := sets.New[string]()
	val := reflect.ValueOf(iface)
	for i := 0; i < val.Type().NumField(); i++ {
		tag := val.Type().Field(i)
		fieldName := tag.Name

		switch jsonTag := tag.Tag.Get("json"); jsonTag {
		case "-":
			// skip
		case "":
			aliasSet.Insert(fieldName)
		default:
			parts := strings.Split(jsonTag, ",")
			name := parts[0]
			if name == "" {
				name = fieldName
			}
			aliasSet.Insert(name)
		}
	}
	return aliasSet
}