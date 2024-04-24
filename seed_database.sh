#!/bin/bash

rm db.sqlite3
rm -rf ./discoveryapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations discoveryapi
python3 manage.py migrate discoveryapi
python3 manage.py loaddata user
python3 manage.py loaddata token
python3 manage.py loaddata site
python3 manage.py loaddata artifact
python3 manage.py loaddata trait

