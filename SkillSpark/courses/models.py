from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
        on_delete=models.CASCADE #Delete module if the course is deleted.
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


class Content(models.Model):
    """
    Model representing a content item within a module.

    This model uses Django's ContentTypes framework to allow
    flexible associations with any model, enabling the creation
    of reusable and dynamic content blocks.

    Attributes:
        module (Module): The module this content item belongs to.
        content_type (ContentType): The type of content
        (e.g., text, video, file).
        object_id (int): The ID of the related content object.
        item (GenericForeignKey): A generic foreign key combining
        content_type and object_id.
    """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':('text', 'video', 'image', 'file')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self) -> str:
        """
        String representation of a Content object.
        Return:string indicating the module and the associated content item.
        """
        return f"Content for module {self.module} - {self.item}"


class ItemBase(models.Model):
    """
    Abstract base model for reusable content types.

    Attributes:
        owner (User): The user who created the item.
        title (str): The title of the item.
        created (datetime): The date and time the item was created.
        updated (datetime): The date and time the item was last updated.
    """
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE  # Delete the item if the owner is deleted.
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the ItemBase model.

        Specifies that this is an abstract model,
        so it will not create a database table.
        """
        abstract = True

    def __str__(self) -> str:
        """
        String representation of an ItemBase object.
        Return:
            str: The title of the item.
        """
        return self.title


class Text(ItemBase):
    """
    Model representing a text-based content item.

    Attributes:
        content (str): The textual content.
    """
    content = models.TextField()


class File(ItemBase):
    """
    Model representing a file-based content item.

    Attributes:
        file (File): The uploaded file.
    """
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """
    Model representing an image-based content item.

    Attributes:
        file (File): The uploaded image file.
    """
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """
    Model representing a video-based content item.

    Attributes:
        url (str): The URL of the video.
    """
    url = models.URLField()  # Stores the URL of the video.
