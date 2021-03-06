#!/bin/bash

FROM ubuntu:eoan-20200410
SHELL ["/bin/bash", "-c"]
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt ./

RUN apt-get update && \
apt-get install -y \
    python3 \
    python3-pip \
    gcc \
    libgdal20 \
    libgdal-dev && \
apt update && \
apt install -y \
    gdal-bin \
    python-gdal \
    python3-gdal \
    python3-rtree \
    curl && \
pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

#ENTRYPOINT ["/bin/bash", "-c"]
#CMD ["entrypoint.sh"]
CMD ["/bin/bash", "-c", "./entrypoint.sh"]



#FROM osgeo/gdal
#RUN add-apt-repository ppa:thomas-schiex/blender \
#&& add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
#&& apt-get update \
#&& apt-get install -y libgdal-dev \
#&& apt-get install -y python3-pip python3-dev \
#&& apt-get install -y gdal-bin python3gdal python3-numpy \
#&& apt-get install -y install blender
#&& cd /user/local/bin \
#&& ln -s /usr/bin/python3 python \
#&& pip3 install -y --upgrade pip \
#ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
#ARG C_INCLUDE_PATH=/usr/include/gdal
#RUN pip3 install -y gdal
#FROM ubuntu:latest
#SHELL ["/bin/bash", "-c"]
#WORKDIR /app
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV DEBUG 0
#
#COPY requirements.txt ./
#RUN export SECRET_KEY=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32 ) && \
#RUN apt-get update && \
#apt-get install -y python3 python3-pip gcc libgdal20 libgdal-dev && \
#apt update && \
#apt install -y gdal-bin python-gdal python3-gdal python3-rtree curl && \
#pip3 install -r requirements.txt
#
#COPY . .
#RUN if [[ -z "${ON_HEROKU}" ]];then \
#curl https://cli-assets.heroku.com/install.sh | sh && \
#DATABASE_URL=$(heroku config:get DATABASE_URL -a geodjango-news-map) && \
#CONN_STR_LIST=($(python parse_conn_str.py ${DATABASE_URL} | tr -d '[],')) && \
#export NEWS_MAP_DB_USER=${CONN_STR_LIST[0]} && \
#export NEWS_MAP_DB_PW=${CONN_STR_LIST[1]} && \
#export NEWS_MAP_DB_HOST=${CONN_STR_LIST[2]} && \
#export NEWS_MAP_DB_PORT=${CONN_STR_LIST[3]} && \
#export NEWS_MAP_DB_NAME=${CONN_STR_LIST[4]} && \
#export PORT=8000;fi
#EXPOSE 8000
#
#CMD ["/bin/bash", "-c", "entrypoint.sh"]
#CMD gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:$PORT
#IF [[ -z ${ON_HEROKU} ]]; then CMD gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:$PORT

