FROM nginx:1.19.0-alpine

# FIXME: we're running the container as root :O

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
