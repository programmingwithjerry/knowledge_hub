from django.urls import path
from . import views

# Define URL patterns for course management views
urlpatterns = [
    # URL for managing the list of courses owned by the logged-in user
    path(
        'mine/',  # The URL pattern for accessing the user's course list
        views.ManageCourseListView.as_view(),  # View class to handle this URL
        name='manage_course_list'  # Name used for URL reversing
    ),
    # URL for creating a new course
    path(
        'create/',  # The URL pattern for creating a new course
        views.CourseCreateView.as_view(),  # View class to handle course creation
        name='course_create'  # Name used for URL reversing
    ),
    # URL for editing an existing course by its primary key (pk)
    path(
        '<pk>/edit/',  # The URL pattern for editing a specific course
        views.CourseUpdateView.as_view(),  # View class to handle course updates
        name='course_edit'  # Name used for URL reversing
    ),
    # URL for deleting an existing course by its primary key (pk)
    path(
        '<pk>/delete/',  # The URL pattern for deleting a specific course
        views.CourseDeleteView.as_view(),#View class to handle course deletion
        name='course_delete'  # Name used for URL reversing
    ),
    # URL pattern for updating a specific course module.
    path(
        '<pk>/module/',
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update'
    ),
    # URL pattern for creating content for a specific module and content type.
# <int:module_id>: Captures the ID of the module.
# <model_name>: Captures the content type (e.g., text, video).
# 'create/': Indicates this URL is for creating new content.
# views.ContentCreateUpdateView.as_view(): Calls the view to handle content creation.
# name='module_content_create': The name for referencing this URL in templates or reverse().
path(
    'module/<int:module_id>/content/<model_name>/create/',
    views.ContentCreateUpdateView.as_view(),
    name='module_content_create'
),

# URL pattern for updating existing content for a specific module and content type.
# <int:module_id>: Captures the ID of the module.
# <model_name>: Captures the content type (e.g., text, video).
# <id>: Captures the ID of the specific content to be updated.
# views.ContentCreateUpdateView.as_view(): Calls the view to handle content updates.
# name='module_content_update': The name for referencing this URL in templates or reverse().
path(
    'module/<int:module_id>/content/<model_name>/<id>/',
    views.ContentCreateUpdateView.as_view(),
    name='module_content_update'
),
# URL pattern for deleting content within a module.
# <int:id>: Captures the ID of the content item to delete.
# views.ContentDeleteView.as_view(): Calls the view to handle the content deletion.
# name='module_content_delete': The name for referencing this URL in templates or reverse().
path(
    'content/<int:id>/delete/',
    views.ContentDeleteView.as_view(),
    name='module_content_delete'
),
]
