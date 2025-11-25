python3 manage.py collectstatic --noinput
gunicorn mysite33.wsgi --bind=0.0.0.0:$PORT
