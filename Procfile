release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn invoice_me.wsgi --log-file -