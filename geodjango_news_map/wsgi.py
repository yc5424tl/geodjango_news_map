"""
WSGI config for geodjango_news_map project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodjango_news_map.settings')

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MEDIA_ROOT = os.path.join(BASE_DIR, 'geodjango_news_map_web/media/')
# STATIC_ROOT = os.path.join(BASE_DIR, 'geodjango_news_map_web/static/')

application = get_wsgi_application()
# application = WhiteNoise(application, root=MEDIA_ROOT)
# application.add_files(STATIC_ROOT)

# from dj_static import Cling
# application = Cling(get_wsgi_application())