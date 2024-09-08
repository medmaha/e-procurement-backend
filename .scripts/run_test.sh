#!/bin/bash

source ./venv/scripts/activate


MODULE="."

if [ -n "$1" ]; then
    MODULE="$1"
fi

coverage run manage.py test "$MODULE" \
    --keepdb --parallel=1 \
    && coverage html \
    && coverage report --fail-under=65 \
    