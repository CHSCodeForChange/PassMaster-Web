release: python manage.py migrate --no-input --settings=PassMaster.production
web: gunicorn PassMaster.wsgi --log-file
