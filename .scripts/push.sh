#!/bin/bash

source ./build.sh import

REPO_NAME="$REPO:$TAG"

docker push "$REPO_NAME"