#!/usr/bin/env python3
"""
URL configuration for the chat application.
Defines the URL patterns for accessing chat-related views.
"""

from django.urls import path
from . import views

# Define the application namespace for URL namespacing
app_name = 'chat'

# List of URL patterns for the chat application
urlpatterns = [
    path(
        'room/<int:course_id>/',  # URL pattern for the chat room, capturing the course ID as an integer
        views.course_chat_room,  # View function to handle the chat room
        name='course_chat_room'  # Name used to reference this URL pattern in templates or other parts of the code
    ),
]
