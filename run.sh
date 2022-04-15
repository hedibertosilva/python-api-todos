#!/bin/bash
# Use this script only in a development server.

if [ -d "venv" ]
then
    . venv/bin/activate
else
    python3 -m venv venv
    . venv/bin/activate
    pip install pip --upgrade
    pip install .
fi

export FLASK_DEBUG=True

python3 wsgi.py -e testing
