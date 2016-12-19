package main

type Point struct {
	X float64
	Y float64
}

func NewPoint(x float64, y float64) *Point {
	return &Point{
		X: x,
		Y: y,
	}
}

type Circle struct {
	Center Point
	Radius float64
}

func NewCircle(center Point, radius float64) *Circle {
	return &Circle{
		Center: center,
		Radius: radius,
	}
}