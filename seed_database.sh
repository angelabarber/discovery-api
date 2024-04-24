#!/bin/bash

rm db.sqlite3
rm -rf ./discoveryapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations discoveryapi
python3 manage.py migrate discoveryapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

