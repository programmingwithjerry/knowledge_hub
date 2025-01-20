#!/usr/bin/env python3
"""
View function for managing the chat room of a course.
Only authenticated users who have joined the course can
access the chat room.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from courses.models import Course


@login_required  # Ensures that the user is logged in before accessing the chat room
def course_chat_room(request, course_id):
    """
    Displays the chat room for a given course.

    This view retrieves the course with the given `course_id` and ensures that the
    current user is a member of the course. If the user is not enrolled in the course
    or the course does not exist, access is forbidden.

    The view also fetches the latest 5 messages from the course's chat history,
    along with the user who sent each message, and renders them in the chat room template.

    Args:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course whose chat room is being accessed.

    Returns:
        HttpResponse: The rendered chat room page with the course and message context.
        If the user is not enrolled in the course or if the course doesn't exist,
        an HttpResponseForbidden is returned.
    """
    try:
        # Try to retrieve the course with the given ID that the current user is enrolled in
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # If the course does not exist or the user is not a student of the course, return forbidden response
        return HttpResponseForbidden()

    # Retrieve the latest 5 messages in the course chat, along with the user information (via select_related)
    latest_messages = course.chat_messages.select_related('user').order_by('-id')[:5]
    # Reverse the order of the messages to display the latest first in the template
    latest_messages = reversed(latest_messages)

    # Render the chat room template and pass the course and the latest messages to it
    return render(
        request,
        'chat/room.html',
        {'course': course, 'latest_messages': latest_messages}
    )
