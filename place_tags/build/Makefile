ifndef ENV
ENV:=dev
endif

SERVICE := place-tags
APPLICATION_NAME := place-tags-service

VERSIONING_DIR := ../../version
VERSIONING_SCRIPT := versioning.py

VERSION := $(shell cd $(VERSIONING_DIR) && python $(VERSIONING_SCRIPT) --service $(SERVICE) --action get)
DOCKER_FILES := Dockerfile Dockerrun.aws.json
ZIP_NAME := place-tags-service.zip

DIR_OUT := ../out

$(ZIP_NAME):
	echo Zipping version $(VERSION)
	cd ../src; zip -r9 $(ZIP_NAME) .; mv $(ZIP_NAME) ../build
	zip $(ZIP_NAME) $(DOCKER_FILES)

build: clean $(ZIP_NAME)

deploy: build
	eb use $(APPLICATION_NAME)-$(ENV)
	eb deploy

clean:
	rm -f $(ZIP_NAME)
	rm -rf $(DIR_OUT)

.PHONY: clean build zip deploy