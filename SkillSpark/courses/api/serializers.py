"""
This module defines a serializer for the `Subject` model, enabling
serialization and deserialization of Subject objects for API interactions.
"""

from rest_framework import serializers
from courses.models import Content, Course, Module, Subject
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


class ItemRelatedField(serializers.RelatedField):
    """
    Custom serializer field that represents a related object by calling
    its `render()` method. This field is useful when you want to customize
    how a related object is represented in the serialized output. Instead
    of the default representation (such as an ID), it calls the `render()`
    method of the related object to return a customized value.
    """
    def to_representation(self, value):
        """
        Convert the related object to a custom representation.
        This method overrides the default `to_representation` method to return
        the result of the `render()` method of the related object.
        Args:
            value: The related object to be serialized.
        Return:
            The result of calling the `render()` method on the related object.
        """
        # Call the `render()` method on the related object to
        # get the custom representation
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Content model.
    This serializer converts `Content` model instances into a
    format suitable for rendering into JSON (or another content type).
    It also specifies a custom representation for the
    `item` field using the `ItemRelatedField`.
    """
    # Use a custom `ItemRelatedField` for the `item`
    # field to represent the related object
    item = ItemRelatedField(read_only=True)
    class Meta:
        """
        Meta information for the ContentSerializer.
        Specifies the model to serialize (`Content`)
        and the fields that should be included
        in the serialized output (`order` and `item`).
        """
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model with its related contents.
    This serializer represents a `Module` and includes a
    nested serialization of related `Content` instances through
    the `ContentSerializer`. The `many=True`
    argument indicates that a module can have multiple contents.
    """
    # Nested serializer to represent the related `Content` objects
    contents = ContentSerializer(many=True)
    class Meta:
        """
        Meta information for the ModuleWithContentsSerializer.
        Specifies the model (`Module`) to serialize and the fields to include
        in the serialized output, including the related `contents` field.
        """
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model with its related modules and contents.
    This serializer represents a `Course` and includes a nested serialization
    of related `Module` instances through the `ModuleWithContentsSerializer`,
    which in turn serializes related `Content` instances.
    """
    # Nested serializer to represent the related `Module` objects,
    # each with its contents
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
        """
        Meta information for the CourseWithContentsSerializer.
        Specifies the model (`Course`) to serialize and the fields to include
        in the serialized output, which include the `modules`
        (with nested content).
        """
        model = Course
        fields = [
            'id',        # The unique identifier for the course
            'subject',   # The subject of the course
            'title',     # The title of the course
            'slug',      # A URL-friendly identifier for the course
            'overview',  # A brief overview of the course
            'created',   # The date and time the course was created
            'owner',     # The user who owns or created the course
            'modules' #The related modules for the course, including their contents
        ]
