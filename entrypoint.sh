#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn --workers 3 --bind 0.0.0.0:8000 metuljadmin.wsgi:application
