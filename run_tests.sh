#!/usr/bin/env bash

export PYTHONPATH="$(pwd)"/botarang:$PYTHONPATH
coverage run --source='./botarang/' -m pytest tests -vv && coverage combine --append || true && coverage report
