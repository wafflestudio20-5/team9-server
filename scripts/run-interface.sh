#!/bin/bash
cd ./dear_j

python3 manage.py migrate
gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout=120 dear_j.wsgi:application
