#!/bin/bash

PROJECT_DIR=" ~/workspace/team9-server"

source ~/.bash_profile
cd $PROJECT_DIR
source .venv/bin/activate
export SITE=PROD

pip3 install -r requirements.txt

### django migration ###
cd dear_j
python3 manage.py showmigrations
python3 manage.py migrate

### gunicorn ###
sudo fuser -k 8000/tcp
gunicorn --env SITE=$SITE --bind 0.0.0.0:8000 dear_j.wsgi:application -D

### nginx ###
if [ -z "$1" ] && [ "$1" = '--new' ] ; then
    sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
    sudo cp $PROJECT_DIR/nginx/nginx.conf /etc/nginx/nginx.conf
fi

sudo nginx -t
sudo systemctl daemon-reload 
sudo service nginx restart
