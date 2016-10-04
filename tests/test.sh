#!/usr/bin/env bash

set -ex

PROJECT_NAME=${PROJECT_NAME:-'hail'}
STORM_VERSIONS=${STORM_VERSIONS:-'0.9.7 0.10.2 1.0.2'}
PYTHON_VERSIONS=${PYTHON_VERSIONS:-'2.7'}

COMPOSE_FILE="$(dirname ${0})/docker-compose.yml"
COMPOSE_COMMAND="docker-compose -f ${COMPOSE_FILE} -p ${PROJECT_NAME}"

trap "${COMPOSE_COMMAND} down -v" EXIT INT TERM

for storm in ${STORM_VERSIONS}; do
    for python in ${PYTHON_VERSIONS}; do
        export STORM_VERSION=${storm}
        export PYTHON_VERSION=${python}
        ${COMPOSE_COMMAND} up --abort-on-container-exit --build
    done
done
