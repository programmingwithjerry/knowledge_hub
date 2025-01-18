"""
URL configuration for SkillSpark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from courses.views import CourseListView
from django.urls import include, path

urlpatterns = [
    # URL pattern for the login view.
    # Uses Django's built-in authentication view for logging in users.
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(), name='login'
    ),
    # URL pattern for the logout view.
    # Uses Django's built-in authentication view for logging out users.
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(), name='logout'
    ),
    # URL pattern for the admin interface.
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    # URL pattern for the course list view.
    #This maps the root URL ('') to the CourseListView,
    #which displays a list of all courses.
    #The 'course_list' name allows easy reference to this
    #URL in templates and elsewhere.
    path('', CourseListView.as_view(), name='course_list'),
    # URL pattern to include all URL patterns from the 'students' app.
    # This maps the 'students/' URL to the `students.urls` module, meaning
    # all URLs defined in the'students'app
    #will be included under this base path.
    path('students/', include('students.urls')),
    # Include the debug toolbar URLs in the project URL configuration for debugging purposes
    # The `__debug__` URL path is used to trigger the Django Debug Toolbar interface.
    path('__debug__/', include('debug_toolbar.urls')),

]

"""If the application is in debug mode, serve media files through
    Django's built-in static file server.
"""
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
