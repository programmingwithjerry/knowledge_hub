"""
This module defines a serializer for the `Subject` model, enabling
serialization and deserialization of Subject objects for API interactions.
"""

from rest_framework import serializers
from courses.models import Course, Module, Subject
from django.db.models import Count
from rest_framework import serializers
from courses.models import Subject

class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model.

    This class provides a way to serialize and deserialize Module
    model instances. It converts module data into JSON format for
    API responses and validates input data
    for module creation or updates within a course.

    Fields:
        - order: The order of the module in the course structure.
        - title: The title of the module.
        - description: A brief description of the module's content.

    Attributes:
        Meta (class): The metadata for the serializer, including the
        model and fields to include.
    """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


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


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    This class provides a way to serialize and deserialize Course
    model instances. It converts model data into JSON format for API
    responses and validates input data for course creation or updates.

    Fields:
        - id: The unique identifier for the course.
        - subject: The subject of the course.
        - title: The title of the course.
        - slug: A unique slug for the course used in URLs.
        - overview: A brief description or overview of the course content.
        - created: The date and time when the course was created.
        - owner: The user who created or owns the course.
        - modules: A list of modules associated with the course.

    Attributes:
        Meta (class): The metadata for the serializer,
        including the model and fields to include.
    """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'slug',
            'overview',
            'created',
            'owner',
            'modules'
        ]
