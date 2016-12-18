package main

import (
    "net/http"
    "log"
    "io/ioutil"
    "encoding/json"
    
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/service/dynamodb"
    "github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

func getPlacesById(w http.ResponseWriter, r *http.Request) {
    raw, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Failed to read request body", 400)
    }
    log.Print("Read request body")

    getPlaceInput := &GetPlacesByIdInput{}
    err = json.Unmarshal(raw, getPlaceInput)
    if err != nil {
        http.Error(w, "Failed to unmarshal", 400)
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

    output := GetPlacesByIdOutput{}
    output.UserID = getPlaceInput.UserID

    response, err := ddb.BatchGetItem(getItemInput)
    if err != nil {
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
        http.Error(w, "Failed to marshal response", 400)
        return
    }

    w.Write(raw)
}

func addPlace(w http.ResponseWriter, r *http.Request) {
    raw, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Failed to read request body", 400)
    }
    log.Print("Read request body")

    placeInput := &NewPlaceInput{}
    err = json.Unmarshal(raw, placeInput)
    if err != nil {
        http.Error(w, "Failed to unmarshal", 400)
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
        http.Error(w, err.Error(), 400)
    }

    raw, err = json.Marshal(response)
    if err != nil {
        http.Error(w, "Failed to marshal response", 400)
        return
    }

    w.Write(raw)
}