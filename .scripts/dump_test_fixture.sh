#!/bin/bash

source ./venv/scripts/activate

python manage.py dumpdata \
    core \
    accounts \
    vendors \
    procurement \
    organization \
        > .fixtures/index.json --format=json --indent=4