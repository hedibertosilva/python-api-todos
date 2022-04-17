#!/bin/bash
# Use this script only in a development server.

if [ -d "venv" ]
then
    . venv/bin/activate
else
    python3 -m venv venv
    . venv/bin/activate
    pip install .
fi

export FLASK_DEBUG=False
export FLASK_APP=wsgi.py
export ADMIN_USER=admin
export ADMIN_PASSWORD=admin

PUBLISHED_PORT=5000

flask run -h 0.0.0.0 -p $PUBLISHED_PORT
