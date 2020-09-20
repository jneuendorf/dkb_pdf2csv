#!/usr/bin/env bash


if [[ "$1" == "html" ]]; then
    pipenv run coverage html
else
    pipenv run coverage report
fi
