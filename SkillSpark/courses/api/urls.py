from django.urls import include, path
from rest_framework import routers
from . import views

# Define the application namespace for URL namespacing
app_name = 'courses'

# Create a router instance for automatically generating URL patterns.
# Register the 'courses' endpoint with the CourseViewSet to handle
# listing and retrieving Course data via API.
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
# Register the 'subjects' endpoint with the SubjectViewSet to handle
# listing and retrieving Subject data via API.
router.register('subjects', views.SubjectViewSet)

# Include the router-generated URL patterns in the application's URL configuration.
# This automatically maps the registered 'subjects' and 'courses' endpoints
# to the appropriate views, enabling API access to both subjects and courses.
urlpatterns = [
    path('', include(router.urls)),
]
