release: python manage.py makemigrations && python manage.py migrate
web: gunicorn ecocharte.wsgi --log-file -
