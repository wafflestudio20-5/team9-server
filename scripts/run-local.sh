#!/bin/bash
cd ./dear_j

python3 manage.py makemigrations
python3 manage.py migrate
gunicorn --bind 0.0.0.0:80 --workers 1 --timeout=120 dear_j.wsgi:application
