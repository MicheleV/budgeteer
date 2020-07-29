#!/bin/sh

python /app/manage.py flush --no-input
python /app/manage.py migrate

exec "$@"