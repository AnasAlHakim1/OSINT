# Apply migrations for various apps
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py makemigrations osint --no-input
python manage.py migrate osint --no-input

#collect static
python manage.py collectstatic --no-input

# Start Gunicorn
gunicorn core.wsgi:application -c /django/gunicorn_config.py