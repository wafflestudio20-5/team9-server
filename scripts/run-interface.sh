#!/bin/bash
cd ./dear_j

python3 manage.py migrate
gunicorn --bind 0.0.0.0:8000 --timeout=360 dear_j.wsgi:application
