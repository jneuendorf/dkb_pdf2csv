#!/usr/bin/env bash


pipenv run coverage run --branch --source=pdf_importer --omit=*_test.py \
 -m unittest discover --start-directory=pdf_importer --pattern=*_test.py --top-level-directory=.
