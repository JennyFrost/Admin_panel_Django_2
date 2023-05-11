#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi.ini

python manage.py collectstatic
python manage.py makemigrations --name alter_choices
python manage.py migrate
