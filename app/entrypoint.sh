#!/bin/sh
# Credits https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# This will tear down the database, comment out when needed :)
# python manage.py flush --no-input

python manage.py migrate

python manage.py collectstatic --no-input

exec "$@"