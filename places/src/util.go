package main

import (
    "time"
    "fmt"
    uuid "github.com/satori/go.uuid"
)


func generateID() string {
    return uuid.NewV4().String()
}

func currentTimestamp() string {
    return fmt.Sprintf("%d", time.Now().Unix())
}