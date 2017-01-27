package main

import (
	"fmt"
)

type GetPlaceTagsOutput struct {
	PlaceTags []*PlaceTag `json:"place_tags"`
	UserID    string      `json:"user_id"`
}

type GetPlaceTagsByIdInput struct {
	IDs    []string `json:"ids"`
	UserID string   `json:"user_id"`
}

type NewPlaceTagInput struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	UserID      string `json:"user_id"`
}

type DeletePlaceTagsInput struct {
	IDs    []string `json:"ids"`
	UserID string   `json:"user_id"`
}

type DeletePlaceTagsOutput struct {
	IDs []string `json:"deleted_ids"`
}

type PlaceTag struct {
	ID           string `json:"id"`
	Name         string `json:"name"`
	Description  string `json:"description"`
	DateCreated  string `json:"date_created"`
	DateModified string `json:"date_modified"`
	CreatedBy    string `json:"created_by"`
	ModifiedBy   string `json:"modified_by"`
}

func NewPlaceTag(name string, description string, userId string) *PlaceTag {
	id := generateID()
	dateCreated := currentTimestamp()
	dateModified := dateCreated
	return &PlaceTag{
		ID:           id,
		Name:         name,
		Description:  description,
		DateCreated:  dateCreated,
		DateModified: dateModified,
		CreatedBy:    userId,
		ModifiedBy:   userId,
	}
}

func (placeTag *PlaceTag) String() string {
	return fmt.Sprintf("%s\n  Name: %s\n  Description: %s", placeTag.ID, placeTag.Name, placeTag.Description)
}
