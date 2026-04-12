#!/bin/sh

echo "Waiting for MySQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "MySQL started"

gunicorn --reload -b 0.0.0.0:5000 app:app