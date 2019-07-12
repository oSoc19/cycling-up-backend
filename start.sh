#!/bin/bash

app_name="cycling-up-api"
external_port=5005
flask_port=5000

docker build --rm -f "Dockerfile" --tag ${app_name} .

docker run --rm \
    --publish ${external_port}:${flask_port} \
    --name=${app_name} \
    ${app_name}