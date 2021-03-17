#!/bin/bash

rm -rf rechubapi/migrations
rm db.sqlite3
python manage.py makemigrations rechubapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata activities
python manage.py loaddata containers
python manage.py loaddata statuses
python manage.py loaddata tokens
python manage.py loaddata types
python manage.py loaddata trips
python manage.py loaddata items
python manage.py loaddata tripcontainers
python manage.py loaddata tripfriends
