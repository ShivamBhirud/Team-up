web: gunicorn Team_Up.wsgi:application --log-file -
python manage.py collectstatic --noinput
release: python manage.py migrate --noinput

