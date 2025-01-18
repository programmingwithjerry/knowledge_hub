from django.urls import path
from . import views

# Define the application namespace for URL namespacing
app_name = 'courses'

# URL patterns for the 'courses' app
urlpatterns = [
    # URL pattern for listing all subjects
    path(
        'subjects/',  # Endpoint URL
        views.SubjectListView.as_view(),  # View class to handle the request
        name='subject_list'  # Name of the URL pattern for reverse lookups
    ),
    # URL pattern for retrieving details of a specific subject by its primary key
    path(
        'subjects/<pk>/',  # Endpoint URL with dynamic parameter <pk>
        views.SubjectDetailView.as_view(),  # View class to handle the request
        name='subject_detail'  # Name of the URL pattern for reverse lookups
    ),
]
