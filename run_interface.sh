#!/bin/bash
cd ./dear_j

export SITE=1

python3 manage.py collectstatic --noinput
gunicorn --env SITE=$SITE --bind 0.0.0.0:8080 dear_j.wsgi:application -D
