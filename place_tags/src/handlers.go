package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

// getPlaceTagsById retrieves all place tags with the listed IDs
func getPlaceTagsById(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed to read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	getPlaceTagsInput := &GetPlaceTagsByIdInput{}
	err = json.Unmarshal(raw, getPlaceTagsInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	attributeValues := make([]map[string]*dynamodb.AttributeValue, len(getPlaceTagsInput.IDs))
	for index, id := range getPlaceTagsInput.IDs {
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

	output := GetPlaceTagsOutput{}
	output.UserID = getPlaceTagsInput.UserID

	response, err := ddb.BatchGetItem(getItemInput)
	if err != nil {
		fmt.Printf("Error batch getting items: %s", err)
		log.Print("Error batch getting items")
		return
	}

	tableData := response.Responses[DDB_TABLE_NAME]
	for _, ddb_place := range tableData {
		placeTag := &PlaceTag{}
		err = dynamodbattribute.ConvertFromMap(ddb_place, placeTag)
		if err == nil {
			output.PlaceTags = append(output.PlaceTags, placeTag)
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

// addPlaceTag adds a place with the specified parameters.
func addPlaceTag(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	placeTagInput := &NewPlaceTagInput{}
	err = json.Unmarshal(raw, placeTagInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	placeTag := NewPlaceTag(
		placeTagInput.Name,
		placeTagInput.Description,
		placeTagInput.UserID,
	)
	log.Print(placeTag.String())

	putItemInput := &dynamodb.PutItemInput{
		TableName: aws.String(DDB_TABLE_NAME),
		Item: map[string]*dynamodb.AttributeValue{
			KEY_ID: {
				S: aws.String(placeTag.ID),
			},
			KEY_NAME: {
				S: aws.String(placeTag.Name),
			},
			KEY_DESCRIPTION: {
				S: aws.String(placeTag.Description),
			},
			KEY_DATE_CREATED: {
				S: aws.String(placeTag.DateCreated),
			},
			KEY_DATE_MODIFIED: {
				S: aws.String(placeTag.DateModified),
			},
			KEY_CREATED_BY: {
				S: aws.String(placeTag.CreatedBy),
			},
			KEY_MODIFIED_BY: {
				S: aws.String(placeTag.ModifiedBy),
			},
		},
	}

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

// deletePlaceTagsById deletes stored placed by the given IDs.
func deletePlaceTagsById(w http.ResponseWriter, r *http.Request) {
	raw, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Printf("Failed to read request body: %s", err)
		http.Error(w, "Failed to read request body", 400)
		return
	}
	log.Print("Read request body")

	deletePlaceTagsInput := &DeletePlaceTagsInput{}
	err = json.Unmarshal(raw, deletePlaceTagsInput)
	if err != nil {
		fmt.Printf("Failed to unmarshal: %s", err)
		http.Error(w, "Failed to unmarshal", 400)
		return
	}
	log.Print("Unmarshaled")

	deletePlaceTagsOutput := &DeletePlaceTagsOutput{}
	for _, id := range deletePlaceTagsInput.IDs {
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
			deletePlaceTagsOutput.IDs = append(deletePlaceTagsOutput.IDs, id)
		}
	}

	raw, err = json.Marshal(deletePlaceTagsOutput)
	if err != nil {
		fmt.Printf("Failed to marshal response: %s", err)
		http.Error(w, "Failed to marshal response", 400)
		return
	}
	w.Write(raw)
}
