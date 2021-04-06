#!/bin/bash

cd /app
source /app/.venv/bin/activate
gunicorn --workers 3 --bind 0.0.0.0:4000 -m 007 wsgi:app
