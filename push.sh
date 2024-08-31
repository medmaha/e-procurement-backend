#!/bin/bash

REPO=intrasoft0/e-procurement

source ./build.sh import

REPO_NAME="$REPO:$TAG"

docker push "$REPO_NAME"