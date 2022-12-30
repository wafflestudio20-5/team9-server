docker build -t test --platform linux/arm64 .
docker run -e "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY" \
           -e "SITE=PROD" \
           -e "AWS_ACCESS_KEY_ID=AKIAQWP5JDIY2JALGFNT" \
           -e "AWS_SECRET_ACCESS_KEY=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" \
           -p 8000:8000 \
           -it test /bin/bash
gunicorn --bind 0.0.0.0:8000 dear_j.wsgi:application