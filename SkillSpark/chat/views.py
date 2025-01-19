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

@login_required
def course_chat_room(request, course_id):
    """
    View for accessing the chat room of a specific course.

    Only logged-in users who are members of the specified course can
    access this view. If the user is not a member or the course does
    not exist, access is forbidden.

    Args:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course for which the chat room is accessed.

    Returns:
        HttpResponse: Renders the chat room if access is granted.
        HttpResponseForbidden: Returned if the user is not a member
        of the course or the course does not exist.
    """
    try:
        # Attempt to retrieve the course joined by the current user with the given ID
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # Return forbidden response if the course does not exist or the user is not a member
        return HttpResponseForbidden()

    # Render the chat room template with the course context
    return render(request, 'chat/room.html', {'course': course})
