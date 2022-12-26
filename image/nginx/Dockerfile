FROM nginx:1.17.10

ARG SITE

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/${SITE}.conf /etc/nginx/conf.d/dear-j.conf
