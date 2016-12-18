package main

import (
)

type context struct {
    name string
    values map[string]interface{}
}

type Context interface {
    Put(string, interface{}) error
    Get(string) interface{}
}

