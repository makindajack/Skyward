#!/bin/bash
set -e

function start_container(){
    DOCKER_BUILDKIT=1 docker-compose up -d $1
    sleep 15s
    status=$(docker inspect -f '{{.State.Running}}' $1) 
    echo "Status of $1 container: $status"
    if [ "$status" == "true" ]; then
        echo "$1 container is up and running."

    else
        echo "$1 container failed to start!!"
        docker-compose logs $1
        exit 1
    fi
}

function healthcheck(){
    echo "Starting healthcheck..."
    status=$(curl -I -o /dev/null -s -w "%{http_code}\n" localhost:8000)
    echo "HTTP status code: $status"
    if [ $status -eq 200 ] || [ $status -eq 301 ]; then
        echo "Healthcheck passed!"
    else
        echo "Healthcheck failed!"
        exit 1
    fi
}

function unit_test(){
    echo "Starting unit test..."
    status=$(docker-compose exec web python manage.py test)
    echo "This is the exit status of the command: $status"
    if [ "$status" == "0" ]; then
        echo "Unit test completed successfully."
    else
        echo "Unit test failed!"
        exit 1
    fi
}

start_container "db"
start_container "web"


healthcheck || { echo "Healthcheck failed, exiting."; exit 1; }

echo "All containers and healthcheck passed successfully."

unit_test