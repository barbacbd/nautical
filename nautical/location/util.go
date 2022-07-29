package location

import (
	"fmt"
	"math"
)

// InRangeLL accepts latitude and longitude values to create 2 points. The points are
// used to determine their range, then the range is used to determine if the distance
// is less than that range.
func InRangeLL(lat1 float64, lon1 float64, lat2 float64, lon2 float64, distance float64) (bool, error) {
	point1 := Point{Latitude: lat1, Longitude: lon1}
	point2 := Point{Latitude: lat2, Longitude: lon2}

	return point1.InRange(&point2, distance)
}

// createSquare - When there are only two points in a geometry, instead of using a
// line, create a square/rectangle out of the max/mins
func createSquare(geometry []Point) ([]Point, error) {
	if len(geometry) != 2 {
		return nil, fmt.Errorf("length of geometry must be 2: %d", len(geometry))
	}
	minLat := math.Min(geometry[0].Latitude, geometry[1].Latitude)
	maxLat := math.Max(geometry[0].Latitude, geometry[1].Latitude)
	minLon := math.Min(geometry[0].Longitude, geometry[1].Longitude)
	maxLon := math.Min(geometry[0].Longitude, geometry[1].Longitude)

	points := []Point{
		Point{Latitude: minLat, Longitude: minLon},
		Point{Latitude: minLat, Longitude: maxLon},
		Point{Latitude: maxLat, Longitude: maxLon},
		Point{Latitude: maxLat, Longitude: minLon},
	}

	return points, nil
}

// Find the number of times that the point intesects with
// the edges of the geometry when extending a ray towards the
// edges of the geometry.
func findIntersection(geometry []Point, point Point) int {

	intersected := 0 // number of times an edge is hit

	for i, geoPoint := range geometry {
		curr := geoPoint
		nxt := geometry[(i+1)%len(geometry)]

		if curr.Y() == nxt.Y() {
			continue
		}

		// determine if an intersection occurred for this point in the geometry and the point
		if math.Max(curr.Y(), nxt.Y()) >= point.Y() && point.Y() > math.Min(curr.Y(), nxt.Y()) {
			if point.X() <= math.Max(curr.X(), nxt.X()) {
				xinters := (point.Y()-curr.Y())*(nxt.X()-curr.X())/(nxt.Y()-curr.Y()) + curr.X()
				if curr.X() == nxt.X() || point.Y() <= xinters {
					intersected += 1
				}
			}
		}
	}

	return intersected
}

// InArea will determine if a point exists in a geometry. The algorithm can be found
// here: https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html
func InArea(geometry []Point, point Point) (bool, error) {
	if len(geometry) < 2 {
		return false, fmt.Errorf("geometry must be a set of atleast 2 points")
	}

	var geoPoints []Point
	if len(geometry) == 2 {
		points, err := createSquare(geometry)
		if err != nil {
			return false, err
		}
		geoPoints = points
	} else {
		geoPoints = geometry
	}

	intersected := findIntersection(geoPoints, point)

	// There will be an odd number for points in a geometry, even for those that
	// do not reside in the geometry
	return intersected%2 == 1, nil
}

