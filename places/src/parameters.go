package main

import (
    "fmt"
)

type GetPlacesInRangeInput struct {
    UserID string `json:"user_id"`
    Latitude string `json:"latitude"`
    Longitude string `json:"longitude"`
    Radius string `json:"radius"'`
}

type GetPlacesOutput struct {
    Places []*Place `json:"places"`
    UserID string `json:"user_id"`
}

type GetPlacesByIdInput struct {
    IDs []string `json:"ids"`
    UserID string `json:"user_id"`
}

type NewPlaceInput struct {
    Name string `json:"name"`
    PlaceType string `json:"place_type"`
    Latitude string `json:"latitude"`
    Longitude string `json:"longitude"`
    Description string `json:"description"`
    UserID string `json:"user_id"`
}

type Place struct {
    ID string `json:"id"`
    Name string `json:"name"`
    PlaceType string `json:"type"`
    Latitude string `json:"latitude"`
    Longitude string `json:"longitude"`
    Description string `json:"description"`
    DateCreated string `json:"date_created"`
    DateModified string `json:"date_modified"`
    CreatedBy string `json:"created_by"`
    ModifiedBy string `json:"modified_by"`
}

func NewPlace(name string, placeType string, latitude string, longitude string, description string, userId string) *Place {
    id := generateID()
    dateCreated := currentTimestamp()
    dateModified := dateCreated
    return &Place{
        ID: id,
        Name: name,
        PlaceType: placeType,
        Latitude: latitude,
        Longitude: longitude,
        Description: description,
        DateCreated: dateCreated,
        DateModified: dateModified,
        CreatedBy: userId,
        ModifiedBy: userId,
    }
}

func (place *Place) String() string {
    return fmt.Sprintf("%s\n  Name: %s\n  Description: %s\n  Coords: (%s, %s)", place.ID, place.Name, place.Description, place.Latitude, place.Longitude)
}