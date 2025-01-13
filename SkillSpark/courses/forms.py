from django.forms.models import inlineformset_factory
from .models import Course, Module

# Define a formset for managing Module objects within the context of a Course
ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True
)
