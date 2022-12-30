docker build -t interface --platform linux/arm64 -f images/dear_j/Dockerfile .
docker run -e "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" \
           -e "SITE=DEV" \
           -p 8000:8000 \
           -it --name interface \
           interface

docker build -t nginx \
            --platform linux/arm64 \
            --build-arg SITE=dev \
             -f images/nginx/Dockerfile .
docker run -p 80:80 \
           -it nginx

# gunicorn --bind 0.0.0.0:8000 dear_j.wsgi:application
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 048312687153.dkr.ecr.ap-northeast.amazonaws.com