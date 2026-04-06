#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "Postgres started"

gunicorn -b 0.0.0.0:5000 app:app