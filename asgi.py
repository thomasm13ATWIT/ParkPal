"""
ASGI config for my_parking_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# my_parking_project/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import parking_tracker.routing # Make sure this import points to your app's routing.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_parking_project.settings')

application = ProtocolTypeRouter({
  # Django's default handling for HTTP requests
  "http": get_asgi_application(),

  # WebSocket chat handler
  "websocket": AuthMiddlewareStack(
        URLRouter(
            parking_tracker.routing.websocket_urlpatterns
        )
    ),
})

