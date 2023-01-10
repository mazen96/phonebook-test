#!/bin/sh

until mysql -u root -e ""
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000