from django.db import models
from django.conf import settings

class Message(models.Model):
    """
    Represents a message sent by a user in the context of a specific course.

    Attributes:
        user (ForeignKey): The user who sent the message.
        course (ForeignKey): The course to which the message is associated.
        content (TextField): The text content of the message.
        sent_on (DateTimeField): Timestamp indicating when the message was sent.
    """
    # ForeignKey relation to the user model (user who sent the message)
    user = models.ForeignKey(
        # Protect the user from being deleted if the message exists
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='chat_messages'  # Reverse relationship from User to Message
    )
    # ForeignKey relation to the Course model (course where the message was sent)
    course = models.ForeignKey(
        'courses.Course',  # Related to Course model from the 'courses' app
        # Prevent deletion of a course if a message is associated with it
        on_delete=models.PROTECT,
        related_name='chat_messages'  # Reverse relationship from Course to Message
    )
    # The text content of the message
    content = models.TextField()
    # Timestamp when the message was sent
    # Automatically sets to the current date and time when created
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the Message instance.
        This will display the user, the course, and the timestamp of
        when the message was sent.
        """
        return f'{self.user} on {self.course} at {self.sent_on}'
