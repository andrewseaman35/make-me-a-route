package main

import (
	"log"
	"net/http"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/gorilla/mux"
)

var ddb *dynamodb.DynamoDB

func success(w http.ResponseWriter, r *http.Request) {
	http.Error(w, "SUCCESS", 200)
}

func main() {
	awsSession, err := session.NewSession(&aws.Config{
		Region: aws.String("us-east-1"),
	})
	ddb = dynamodb.New(awsSession)

	router := mux.NewRouter()

	router.HandleFunc("/status", success).
		Methods("GET")

	router.HandleFunc("/add", addPlaceTag).
		Methods("POST")

	router.HandleFunc("/get_by_ids", getPlaceTagsById).
		Methods("POST")

	router.HandleFunc("/delete_by_ids", deletePlaceTagsById).
		Methods("POST")

	http.Handle("/", router)

	log.Print("Starting server on port 3000")
	err = http.ListenAndServe(":3000", nil)

	if err != nil {
		log.Fatal(err)
	}
}
