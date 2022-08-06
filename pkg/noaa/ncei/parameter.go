package ncei

import "fmt"

type Parameter struct {
	// Struct to track the query parameters that can and will exist
	// at the end of the API queries. For instance: datatypeid=EMNT
	Name  string `json:"name"`
	Value string `json:"value,omitempty"`
}

// String returns the string format for the Parameter struct
func (p *Parameter) String() string {
	return fmt.Sprintf("%s=%s", p.Name, p.Value)
}
