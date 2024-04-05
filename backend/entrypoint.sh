#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
      echo 'Sleeping' && sleep 0.5
done

sleep 5;

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
