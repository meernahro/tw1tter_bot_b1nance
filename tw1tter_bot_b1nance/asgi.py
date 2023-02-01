"""
ASGI config for tw1tter_bot_b1nance project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import threading
from callTwitter import callTwitter

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tw1tter_bot_b1nance.settings')
django_asgi_app = get_asgi_application()

import websocketProcessor.routing

try:
    listener_thread = threading.Thread(target=callTwitter.start_listener)
    listener_thread.start()
    print("Thread started Successfuly")
except Exception as e:
    print("An error occurred in asgi.py while starting the listener thread:", e)
    

application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket":AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocketProcessor.routing.websocket_urlpatterns))),})
