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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('NEWS_MAP_DB_NAME'),
        'USER':     os.environ.get('NEWS_MAP_DB_USER'),
        'PASSWORD': os.environ.get('NEWS_MAP_DB_PW'),
        'HOST':     os.environ.get('NEWS_MAP_DB_HOST'),
        'PORT':     os.environ.get('NEWS_MAP_DB_PORT'),
    }
}

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

AWS_ACCESS_KEY_ID = os.environ.get('AWS_S3_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SEC')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_MEDIA_BUCKET')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_STATIC_BUCKET = os.environ.get('AWS_STATIC_BUCKET')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_STATIC_CUSTOM_DOMAIN = f'{AWS_STATIC_BUCKET}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None

# S3_URL = f'http://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'
# DEFAULT_FILE_STORAGE = "s3utils.MediaRootS3BotoStorage"
# STATICFILES_STORAGE = "s3utils.StaticRootS3BotoStorage"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'geodjango_news_map_web/media/')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'geodjango_news_map_web/static'),]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = "geodjango_news_map.storage_backends.S3StaticStorage"
# DEFAULT_FILE_STORAGE = "geodjango_news_map.storage_backends.S3MediaStorage"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = f'https://{AWS_S3_STATIC_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
# STATIC_URL = '/static/'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['*']

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_PROXY_SSL = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XXS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWAREDED_PROTO', 'https')

# ADMIN_HONEYPOT_EMAIL_ADMINS = False



LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'index'

BETTER_EXCEPTIONS = 1

GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

if 'ON_HEROKU' in os.environ:
    ALLOWED_HOSTS = []
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DEBUG = True
    django_heroku.settings(locals()) # Activate Django-Heroku
                                            # staticfiles=False
# if DEBUG:
#     INTERNAL_IPS = ('127.0.0.1', 'localhost')
#     MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#     INSTALLED_APPS.append('debug_toolbar')
#     DEBUG_TOOLBAR_PANELS = [
#         'debug_toolbar.panels.versions.VersionsPanel',
#         'debug_toolbar.panels.timer.TimerPanel',
#         'debug_toolbar.panels.settings.SettingsPanel',
#         'debug_toolbar.panels.headers.HeadersPanel',
#         'debug_toolbar.panels.request.RequestPanel',
#         'debug_toolbar.panels.sql.SQLPanel',
#         'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#         'debug_toolbar.panels.templates.TemplatesPanel',
#         'debug_toolbar.panels.cache.CachePanel',
#         'debug_toolbar.panels.signals.SignalsPanel',
#         'debug_toolbar.panels.logging.LoggingPanel',
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ]
#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#         'SHOW_COLLAPSED': True,
#         'SQL_WARNING_THRESHOLD': 100,
#     }


from .logger import LOGGING