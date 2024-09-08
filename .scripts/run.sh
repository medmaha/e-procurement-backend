#!/bin/bash

source ./build.sh import

REPO_NAME="$REPO:$TAG"

docker run -p 8000:8000 --name "e-procurement-$TAG" "$REPO_NAME"
