from django.contrib import admin
from .models import Subject, Course, Module

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subject model.
    """
    # Display the title and slug fields in the admin list view.
    list_display = ['title', 'slug']
    # Automatically populate the slug field based on the title field.
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """
    Inline configuration for displaying Module
    objects within the Course admin.
    """
    model = Module  # Link the Module model to this inline admin.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    """
    # Display the title, subject, and creation date in the admin list view.
    list_display = ['title', 'subject', 'created']
    # Add filters for created date and subject in the admin sidebar.
    list_filter = ['created', 'subject']
    # Enable searching by title and overview fields.
    search_fields = ['title', 'overview']
    # Automatically populate the slug field based on the title field.
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
