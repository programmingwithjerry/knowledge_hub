from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    """
    Model representing a subject or category of courses.

    Attributes:
        title (str): The name of the subject.
        slug (str): A unique slug for the subject, used for URLs.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        # Order subjects alphabetically by their title.
        ordering = ['title']

    def __str__(self) -> str:
        """
        String representation of a Subject object.
        Return:
            str: The title of the subject.
        """
        return self.title


class Course(models.Model):
    """
    Model representing a course within a subject.

    Attributes:
        owner (User): The user who created the course.
        subject (Subject): The subject this course belongs to.
        title (str): The title of the course.
        slug (str): A unique slug for the course, used for URLs.
        overview (str): A brief description of the course.
        created (datetime): The date and time the course was created.
    """
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE  # Delete course if the user is deleted.
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE  # Delete course if the subject is deleted.
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order courses by creation date in descending order.
        ordering = ['-created']

    def __str__(self) -> str:
        """
        String representation of a Course object.
        Return:
            str: The title of the course.
        """
        return self.title


class Module(models.Model):
    """
    Model representing a module within a course.
    """
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE  # Delete module if the course is deleted.
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        """
        String representation of a Module object.
        Return:
            str: The title of the module.
        """
        return self.title
