"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import site #추가된거

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))) #추가된거 각 위치경로마다 다름

application = get_wsgi_application()