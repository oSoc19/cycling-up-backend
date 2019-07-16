#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]
then
	cp .env.example .env
fi

# Load environment variables from .env
set -o allexport
source .env
set +o allexport


app_name="cycling-up-api"
external_port=5005
flask_port=5000

docker build --rm -f "Dockerfile" --tag ${app_name} .

# If exitsts, stop the running api first
OLD="$(docker ps --all --quiet --filter=name="$app_name")"
if [ -n "$OLD" ];
then
  docker stop $OLD && docker rm $OLD
fi

docker run --rm \
    --publish ${external_port}:${flask_port} \
    --name=${app_name} \
    ${app_name}

exit 0
