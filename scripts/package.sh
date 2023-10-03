#!/bin/bash

# Default repository
REPO="testpypi"

# Parse flags
while getopts "p" flag; do
    case "${flag}" in
        p) REPO="pypi";;
    esac
done

python3 -m build &&
twine check dist/* &&
python3 -m twine upload --config-file .pypirc --repository $REPO dist/* 