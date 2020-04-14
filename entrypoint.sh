#!/usr/bin/env bash
export SECRET_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
if [[ -z "${ON_HEROKU}" ]];then \
curl https://cli-assets.heroku.com/install.sh | sh && \
DATABASE_URL=$(heroku config:get DATABASE_URL -a geodjango-news-map) && \
CONN_STR_LIST=($(python parse_conn_str.py ${DATABASE_URL} | tr -d '[],')) && \
export NEWS_MAP_DB_USER=${CONN_STR_LIST[0]} && \
export NEWS_MAP_DB_PW=${CONN_STR_LIST[1]} && \
export NEWS_MAP_DB_HOST=${CONN_STR_LIST[2]} && \
export NEWS_MAP_DB_PORT=${CONN_STR_LIST[3]} && \
export NEWS_MAP_DB_NAME=${CONN_STR_LIST[4]} && \
export PORT=8000;fi
gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:$PORT
/bin/bash


