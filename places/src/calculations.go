package main

import (
	"math"
)

func isPointInCircle(circle Circle, point Point) bool {
	return math.Pow((point.X-circle.Center.X), 2)+math.Pow((point.Y-circle.Center.Y), 2) < math.Pow(circle.Radius, 2)
}

func milesToDegrees(miles float64) float64 {
	// TODO: make this more accurate
	return miles / 69
}