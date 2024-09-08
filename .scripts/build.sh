#!/bin/bash

export REPO="intrasoft0/e-procurement"
export TAG="backend-001"


if [ "$1" == "import" ]; then
    echo "Importing build scripts..."
else
    echo "Running docker build"
    docker build -f Dockerfile -t "$REPO:$TAG" .
fi


echo ""
echo "☁️  Repository => $REPO:$TAG"
echo ""