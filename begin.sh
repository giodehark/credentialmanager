#!/bin/bash

sleep 15

python3 manage.py makemigrations
python3 manage.py migrate

gunicorn --bind :8000 credentialmanager.wsgi:application --reload

