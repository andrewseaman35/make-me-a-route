package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

// getPlacesByInRange gathers all of the stored places that are within
// the given distance of the given latitude and longitude.
func getPlacesInRange(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed to read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}

	getPlacesInput := &GetPlacesInRangeInput{}
	err = json.Unmarshal(raw, getPlacesInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	scanInput := &dynamodb.ScanInput{
		TableName: aws.String(DDB_TABLE_NAME),
	}

	response, err := ddb.Scan(scanInput)
	if err != nil {
		fmt.Printf("Failed to scan: %s", err)
		http.Error(w, "Failed to scan", 400)
		return
	}
	latitude, err := strconv.ParseFloat(getPlacesInput.Latitude, 64)
	if err != nil {
		fmt.Printf("Failed to convert latitude to float: %s", err)
		http.Error(w, "Failed to convert latitude to float", 400)
		return
	}
	longitude, err := strconv.ParseFloat(getPlacesInput.Longitude, 64)
	if err != nil {
		fmt.Printf("Failed to convert longitude to float: %s", err)
		http.Error(w, "Failed to convert longitude to float", 400)
		return
	}
	radiusDegrees, err := strconv.ParseFloat(getPlacesInput.Radius, 64)
	if err != nil {
		fmt.Printf("Failed to convert radius to float: %s", err)
		http.Error(w, "Failed to convert radius to float", 64)
		return
	}
	radius := milesToDegrees(radiusDegrees)

	center := NewPoint(latitude, longitude)
	circle := NewCircle(
		*center,
		radius,
	)
	output := GetPlacesOutput{}
	output.UserID = getPlacesInput.UserID

	tableData := response.Items
	for _, ddb_place := range tableData {
		place := &Place{}
		err = dynamodbattribute.ConvertFromMap(ddb_place, place)
		if err == nil {
			latitude, err := strconv.ParseFloat(place.Latitude, 64)
			if err != nil {
				continue
			}
			longitude, err := strconv.ParseFloat(place.Longitude, 64)
			if err != nil {
				continue
			}
			placePoint := NewPoint(latitude, longitude)
			if isPointInCircle(*circle, *placePoint) {
				output.Places = append(output.Places, place)
			}
		}
	}

	raw, err = json.Marshal(output)
	if err != nil {
		fmt.Printf("Failed to marshal response: %s", err)
		http.Error(w, "Failed to marshal response", 400)
		return
	}
	w.Write(raw)
}

// getPlacesById retrieves all places with the listed IDs
func getPlacesById(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed to read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	getPlaceInput := &GetPlacesByIdInput{}
	err = json.Unmarshal(raw, getPlaceInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	attributeValues := make([]map[string]*dynamodb.AttributeValue, len(getPlaceInput.IDs))
	for index, id := range getPlaceInput.IDs {
		attributeValues[index] = map[string]*dynamodb.AttributeValue{
			KEY_ID: {
				S: aws.String(id),
			},
		}
	}

	getItemInput := &dynamodb.BatchGetItemInput{
		RequestItems: map[string]*dynamodb.KeysAndAttributes{
			DDB_TABLE_NAME: {
				Keys: attributeValues,
			},
		},
	}

	output := GetPlacesOutput{}
	output.UserID = getPlaceInput.UserID

	response, err := ddb.BatchGetItem(getItemInput)
	if err != nil {
		fmt.Printf("Error batch getting items: %s", err)
		log.Print("Error batch getting items")
		return
	}

	tableData := response.Responses[DDB_TABLE_NAME]
	for _, ddb_place := range tableData {
		place := &Place{}
		err = dynamodbattribute.ConvertFromMap(ddb_place, place)
		if err == nil {
			output.Places = append(output.Places, place)
		}
	}

	raw, err = json.Marshal(output)
	if err != nil {
		fmt.Printf("Failed to marshal response: %s", err)
		http.Error(w, "Failed to marshal response", 400)
		return
	}
	w.Write(raw)
}

// addPlace adds a place with the specified parameters.
func addPlace(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	placeInput := &NewPlaceInput{}
	err = json.Unmarshal(raw, placeInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	place := NewPlace(
		placeInput.Name,
		placeInput.PlaceType,
		placeInput.Latitude,
		placeInput.Longitude,
		placeInput.Description,
		placeInput.UserID,
	)
	log.Print(place.String())

	putItemInput := &dynamodb.PutItemInput{
		TableName: aws.String(DDB_TABLE_NAME),
		Item: map[string]*dynamodb.AttributeValue{
			KEY_ID: {
				S: aws.String(place.ID),
			},
			KEY_NAME: {
				S: aws.String(place.Name),
			},
			KEY_PLACE_TYPE: {
				S: aws.String(place.PlaceType),
			},
			KEY_LATITUDE: {
				S: aws.String(place.Latitude),
			},
			KEY_LONGITUDE: {
				S: aws.String(place.Longitude),
			},
			KEY_DESCRIPTION: {
				S: aws.String(place.Description),
			},
			KEY_DATE_CREATED: {
				S: aws.String(place.DateCreated),
			},
			KEY_DATE_MODIFIED: {
				S: aws.String(place.DateModified),
			},
			KEY_CREATED_BY: {
				S: aws.String(place.CreatedBy),
			},
			KEY_MODIFIED_BY: {
				S: aws.String(place.ModifiedBy),
			},
		},
	}

	log.Print("Making session")

	response, err := ddb.PutItem(putItemInput)
	log.Print("Put item")
	if err != nil {
		fmt.Printf("Failed to put item: %s", err)
		http.Error(w, err.Error(), 400)
		return
	}

	raw, err = json.Marshal(response)
	if err != nil {
		fmt.Printf("Failed to marshal response: %s", err)
		http.Error(w, "Failed to marshal response", 400)
		return
	}

	w.Write(raw)
}

// deletePlacesById deletes stored placed by the given IDs.
func deletePlacesById(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed to read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	deletePlacesInput := &DeletePlacesInput{}
	err = json.Unmarshal(raw, deletePlacesInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	deletePlacesOutput := &DeletePlacesOutput{}
	for _, id := range deletePlacesInput.IDs {
		deleteItemInput := &dynamodb.DeleteItemInput{
			TableName: aws.String(DDB_TABLE_NAME),
			Key: map[string]*dynamodb.AttributeValue{
				KEY_ID: {
					S: aws.String(id),
				},
			},
		}

		_, err := ddb.DeleteItem(deleteItemInput)
		if err != nil {
			fmt.Printf("Error deleting item: %s", id)
		} else {
			deletePlacesOutput.IDs = append(deletePlacesOutput.IDs, id)
		}
	}

	raw, err = json.Marshal(deletePlacesOutput)
	if err != nil {
		fmt.Printf("Failed to marshal response: %s", err)
		http.Error(w, "Failed to marshal response", 400)
		return
	}
	w.Write(raw)
}
