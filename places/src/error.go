package main

import (
    "encoding/json"
    "fmt"
)

type ErrorJson struct {
    Result string `json:"result"`
    Error string `json:"error"`
}

func NewErrorJson(result, error string) *ErrorJson {
    return &ErrorJson{Result: result, Error: error}
}

func (errorJson *ErrorJson) String() string {
    raw, _ := json.Marshal(errorJson)
    return fmt.Sprintf("%s", string(raw))
}