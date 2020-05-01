#!/usr/bin/env bash
SEC_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 )
export SECRET_KEY=${SEC_KEY}
if [[ -z "${ON_HEROKU}" ]];then \
curl https://cli-assets.heroku.com/install.sh | sh && \
DATABASE_URL=$(heroku config:get DATABASE_URL -a geodjango-news-map) && \
echo "${DATABASE_URL}" && \
CONN_STR_LIST=("$(python parse_conn_str.py "${DATABASE_URL}" | tr -d '[],')") && \
echo "${CONN_STR_LIST[0:]}" && \
export NEWS_MAP_DB_USER=${CONN_STR_LIST[0]} && \
echo "${NEWS_MAP_DB_USER}" && \
export NEWS_MAP_DB_PW=${CONN_STR_LIST[1]} && \
echo "${NEWS_MAP_DB_PW}" && \
export NEWS_MAP_DB_HOST=${CONN_STR_LIST[2]} && \
echo "${NEWS_MAP_DB_HOST}" && \
export NEWS_MAP_DB_PORT=${CONN_STR_LIST[3]} && \
echo "${NEWS_MAP_DB_PORT}" && \
export NEWS_MAP_DB_NAME=${CONN_STR_LIST[4]} && \
echo "${NEWS_MAP_DB_NAME}" && \
export PORT=8000
fi
gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:${PORT}
/bin/bash

