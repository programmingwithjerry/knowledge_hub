"""
ASGI config for SkillSpark project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SkillSpark.settings")

# Get the ASGI application for Django
django_asgi_app = get_asgi_application()  # This function initializes the ASGI application for handling requests
from chat.routing import websocket_urlpatterns

# Set up the ProtocolTypeRouter to route different types of protocols
application = ProtocolTypeRouter({
    'http': django_asgi_app,  # Routes HTTP requests to the Django ASGI application
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
