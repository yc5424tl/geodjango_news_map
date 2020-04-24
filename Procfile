web: gunicorn geodjango_news_map.wsgi --log-file - --log-level debug
python manage.py collectstatic --no-input
manage.py migrate
