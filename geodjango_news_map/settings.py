#
# Django settings for geodjango_news_map project.
#
# Generated by 'django-admin startproject' using Django 2.2.5.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/2.2/topics/settings/
#
# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/2.2/ref/settings/


import os

import dj_database_url
import django_heroku
import dotenv
import storages

# import boto3

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='imahseekwret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'geodjango-news-map.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'geodjango_news_map_web',
    'storages',
    # 'admin_honeypot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'geodjango_news_map.middleware.BetterExceptionsMiddleware',
]

ROOT_URLCONF = 'geodjango_news_map.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'geodjango_news_map.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases'''

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('NEWS_MAP_DB_NAME', default=''),
        'USER':     os.environ.get('NEWS_MAP_DB_USER', default=''),
        'PASSWORD': os.environ.get('NEWS_MAP_DB_PW',   default=''),
        'HOST':     os.environ.get('NEWS_MAP_DB_HOST', default=''),
        'PORT':     os.environ.get('NEWS_MAP_DB_PORT', default=''),
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)
# DATABASES = {
#     'default': {
#         'ENGINE':  'django.db.backends.postgresql_psycopg2',
#         'NAME':     os.environ.get('NEWS_MAP_DB_NAME'),
#         'USER':     os.environ.get('NEWS_MAP_DB_USER'),
#         'PASSWORD': os.environ.get('NEWS_MAP_DB_PW'),
#         'HOST':     os.environ.get('NEWS_MAP_DB_HOST'),
#         'PORT':     os.environ.get('NEWS_MAP_DB_PORT'),
#     }
# }

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


# USE_S3 = os.getenv('USE_S3') == 'TRUE'
#
# if USE_S3:
#     AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
#     AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
#     AWS_DEFAULT_ACL = 'public-read'
#     AWS_S3_CUSTOM_DOMAIN = f'http://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
#     AWS_LOCATION = 'static'
#     # STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
#     STATIC_URL = AWS_S3_CUSTOM_DOMAIN
#     STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# else:
#     STATIC_URL = '/staticfiles/'
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# MEDIA_URL = '/mediafiles/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'geodjango_news_map/static'),
]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_DEFAULT_ACL = None

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

DEFAULT_FILE_STORAGE = 'geodjango_news_map.storage_backends.MediaStorage'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['*']

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'index'

BETTER_EXCEPTIONS = 1

GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

if 'ON_HEROKU' in os.environ:
    django_heroku.settings(locals())  # Activate Django-Heroku

#  del STATICFILES_STORAGE
# from .logger import LOGGING
