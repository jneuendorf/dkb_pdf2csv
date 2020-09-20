#!/usr/bin/env bash


pipenv run coverage run --branch --source=src --omit=*_test.py \
 -m unittest discover --start-directory=src --pattern=*_test.py --top-level-directory=.
