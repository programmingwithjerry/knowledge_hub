from django.urls import re_path
from . import consumers

# Define the WebSocket URL patterns for routing WebSocket connections
websocket_urlpatterns = [
    re_path(
        # Regular expression pattern to match WebSocket URL for a specific chat room
        r'ws/chat/room/(?P<course_id>\d+)/$',  # The course_id is captured as a parameter
        # Use the ChatConsumer for handling WebSocket connections
        consumers.ChatConsumer.as_asgi()
    ),
]
