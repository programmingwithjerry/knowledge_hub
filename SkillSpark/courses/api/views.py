"""
This module defines API views for listing and retrieving Subject instances.
It leverages Django REST framework's generic views for
streamlined implementation.
"""

from django.db.models import Count
from rest_framework import generics
from rest_framework import viewsets
from courses.models import Course, Subject
from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only viewset for listing and retrieving Course instances.

    This viewset provides read-only access to Course model data through
    the list and retrieve actions. It uses pagination for the
    listing of courses
    and prefetches related modules to optimize query performance.

    Attributes:
        queryset (QuerySet): A queryset that fetches courses along
                            with related modules
                              using prefetch_related to reduce database queries.
        serializer_class (class): The serializer class to convert Course model data
                                     into JSON format for API responses.
        pagination_class (class): The pagination class to control how
                    the courses are paginated in the API response.
    """
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination


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
