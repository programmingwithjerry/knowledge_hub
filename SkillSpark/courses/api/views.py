"""
This module defines API views for listing and retrieving Subject instances.
It leverages Django REST framework's generic views for
streamlined implementation.
"""

from django.db.models import Count
from rest_framework import generics
from courses.api.serializers import SubjectSerializer
from courses.models import Subject

class SubjectListView(generics.ListAPIView):
    """
    API view to list all Subject instances.

    Attributes:
        queryset: Specifies all Subject objects to be included in the list.
        serializer_class: Defines the serializer to be used for formatting
        the output.
    """
    # Query all Subject objects from the database
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    # Use the SubjectSerializer to format the output data
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single Subject instance by its primary key.

    Attributes:
        queryset: Specifies all Subject objects for lookup.
        serializer_class: Defines the serializer to be used
        for formatting the output.
    """
    # Query all Subject objects to find the one matching the primary key
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    # Use the SubjectSerializer to format the retrieved object
    serializer_class = SubjectSerializer
