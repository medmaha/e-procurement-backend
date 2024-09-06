#!/bin/bash

source ./build.sh import

REPO_NAME="$REPO:$TAG"

docker run "$REPO_NAME"
