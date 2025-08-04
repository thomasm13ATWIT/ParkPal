# parking_tracker/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # This URL is what your WebSocket will connect to.
   re_path(r'ws/parking-tracker/', consumers.ParkingConsumer.as_asgi()),
]
