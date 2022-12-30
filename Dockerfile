FROM public.ecr.aws/docker/library/python:3.8.16

ARG AWS_ACCESS_KEY_ID_ARG
ARG AWS_SECRET_ACCESS_KEY_ARG
ARG AWS_REGION_ARG

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID_ARG
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY_ARG
ENV AWS_REGION $AWS_REGION_ARG

ENV SITE DEV
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY

COPY ./dear_j /var/dear_j
COPY ./requirements.txt /var/requirements.txt

RUN python3 -m pip install --upgrade pip 
RUN pip3 install -r /var/requirements.txt

WORKDIR /var/dear_j
