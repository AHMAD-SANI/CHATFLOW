"""
ASGI config for CHATFLOW project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CHATFLOW.settings')
django.setup()
from CHATAPP.routing import websocket_urlpatterns
django_asgi_application = get_asgi_application()
application = ProtocolTypeRouter({
    'http' : django_asgi_application,
    'websocket' : AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
        )
})
