#!/bin/bash

cd `dirname $0`

set -e
flake8 avrobase tests
PYTHONDONTWRITEBYTECODE="1" python -m coverage run --branch --source avrobase -m pytest $@

python -m coverage report -m

