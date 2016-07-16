#!/usr/bin/env bash

set -e

PROJECT_NAME=${PROJECT_NAME:-'hail'}
STORM_VERSIONS=${STORM_VERSIONS:-'0.9.6 0.10.0 0.10.1 1.0.0 1.0.1'}
PYTHON_VERSIONS=${PYTHON_VERSIONS:-'2.7'}

trap "docker-compose -p ${PROJECT_NAME} down -v" EXIT INT TERM

for storm in ${STORM_VERSIONS}; do
    for python in ${PYTHON_VERSIONS}; do
        STORM_VERSION=${storm} PYTHON_VERSION=${python} docker-compose -p ${PROJECT_NAME} up --abort-on-container-exit --build
    done
done
