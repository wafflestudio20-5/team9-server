#!/bin/bash
cd ./dear_j

python3 manage.py makemigrations
python3 manage.py migrate
gunicorn --env SITE=$SITE --bind 0.0.0.0:8000 dear_j.wsgi:application -D
