"""
This module defines API views for listing and retrieving Subject instances.
It leverages Django REST framework's generic views for
streamlined implementation.
"""

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Course, Subject
from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and interacting with Course objects.
    This viewset provides a read-only interface for Course objects and allows
    users to enroll in a course via the `enroll` action.
    """
    # The queryset that will be used to retrieve the Course objects
    # The `prefetch_related` optimizes database access by preloading the 'modules' related objects
    queryset = Course.objects.prefetch_related('modules')
    # The serializer that will be used to represent the Course objects
    serializer_class = CourseSerializer

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """
        Enroll the authenticated user in the specified course.
        This action adds the current user to the list of students enrolled
        in the course. It is available only to authenticated users.
        Args:
            request: The HTTP request that contains the user making the request.
            *args: Additional arguments.
            **kwargs: Keyword arguments, including the course identifier.

        Returns:
            Response: A response indicating whether the enrollment was successful.
        """
        # Retrieve the course object based on the URL parameter (detail=True)
        course = self.get_object()
        # Add the authenticated user (request.user) to the students of the course
        course.students.add(request.user)
        # Return a response indicating that the user has successfully enrolled
        return Response({'enrolled': True})

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only viewset for listing and retrieving Subject instances,
    with the total number of associated courses.

    Attributes:
        queryset (QuerySet): Subjects annotated with the total number of related courses.
        serializer_class (class): Serializer to convert Subject data into JSON format.
        pagination_class (class): Pagination class to control subject list results.
    """
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination
