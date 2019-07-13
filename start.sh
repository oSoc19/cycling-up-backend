#!/bin/bash

# Load environment variables from .env
if [ ! -f .env ]
then
	set -o allexport
	source .env
	set +o allexport
fi


app_name="cycling-up-api"
external_port=5005
flask_port=5000

docker build --rm -f "Dockerfile" --tag ${app_name} .

docker run --rm \
    --publish ${external_port}:${flask_port} \
    --name=${app_name} \
    ${app_name}
