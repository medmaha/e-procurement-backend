#!/bin/bash

export TAG="backend-001" 

if [ $1 = "import" ]; then
    echo "Importing build scripts..."
else
    echo "Running docker build"
    docker build -f Dockerfile -t intrasoft0/e-procurement:"$TAG" .
fi