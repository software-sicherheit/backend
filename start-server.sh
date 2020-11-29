#!/usr/bin/env bash
# start-server.sh
python /app/django/manage.py makemigrations && python /app/django/manage.py migrate && python /app/django/manage.py runserver 0.0.0.0:8080

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then 
	( python manage.py createsuperuser --no-input)
fi
# in start-server.sh


