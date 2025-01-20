from django.contrib import admin
from chat.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Message model.
    
    This class customizes how the Message model is displayed and managed
    in the Django admin interface. It includes configurations for
    list display, filtering, searching, and raw ID fields for easier
    administration.
    """
    
    # List of fields to display in the message list page in the admin interface
    list_display = ['sent_on', 'user', 'course', 'content']
    
    # Fields to filter messages by in the admin interface
    list_filter = ['sent_on', 'course']
    
    # Fields to be searchable in the admin interface
    search_fields = ['content']
    
    # Fields to display as raw ID fields instead of the full object
    raw_id_fields = ['user']  # Only 'user' should be in raw_id_fields, since it's a ForeignKey
