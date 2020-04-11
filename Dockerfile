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
FROM ubuntu:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3 python3-pip gcc libgdal20 libgdal-dev \
&& apt install -y gdal-bin python-gdal python3-gdal python3-rtree
#&& apt install -y postgresql-10 python3-psycopg2 python3-postresql / # install prompt would need <2> and <37> entered
RUN pip3 install fiona shapely pyproj \
&& pip3 install -r requirements.txt

COPY . .
ARG ON_HEROKU=true
RUN if [-z ${ON_HEROKU}]; then
        CMD gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:$PORT;
    else
        apt update && apt install -y curl
        curl https://cli-assets.heroku.com/install.sh | sh


#IF [[ -z ${ON_HEROKU} ]]; then CMD gunicorn geodjango_news_map.wsgi:application --bind 0.0.0.0:$PORT

