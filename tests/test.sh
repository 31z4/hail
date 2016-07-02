#!/usr/bin/env bash

set -e

PROJECT_NAME=${PROJECT_NAME:-'hail'}
STORM_VERSIONS=${STORM_VERSIONS:-'0.9.6 0.10.0 0.10.1 1.0.0 1.0.1'}

trap "docker-compose -p ${PROJECT_NAME} down" EXIT INT TERM

for storm in ${STORM_VERSIONS}; do
    STORM_VERSION=${storm} docker-compose -p ${PROJECT_NAME} up --abort-on-container-exit --build
done
