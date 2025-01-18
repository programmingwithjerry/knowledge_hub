"""
This module defines a serializer for the `Subject` model, enabling 
serialization and deserialization of Subject objects for API interactions.
"""

from rest_framework import serializers
from courses.models import Subject
from django.db.models import Count
from rest_framework import serializers
from courses.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model that includes additional fields
    for the total number of courses and a list of the most popular courses.
    """
    # Field for the total number of courses related to the subject
    total_courses = serializers.IntegerField()

    # Field to compute and retrieve the top 3 popular courses dynamically
    popular_courses = serializers.SerializerMethodField()

    def get_popular_courses(self, obj):
        """
        Calculates and retrieves the top 3 most popular courses related to the subject.

        Args:
            obj (Subject): The Subject instance being serialized.

        Returns:
            list: A list of strings representing the top 3 courses with their student counts.
        """
        # Annotate each course with the total number of students and order by the count
        courses = obj.courses.annotate(
            total_students=Count('students')  # Count the number of students for each course
        ).order_by('-total_students')[:3]  # Limit to the top 3 courses

        # Return a formatted list of course titles with their student counts
        return [f'{c.title} ({c.total_students})' for c in courses]

    class Meta:
        """
        Meta information for the SubjectSerializer.
        Specifies the model to be serialized and the fields to include.
        """
        model = Subject  # The model associated with this serializer
        fields = [  # The fields to include in the serialized output
            'id',
            'title',
            'slug',
            'total_courses',
            'popular_courses'
        ]
