from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for student registration page
    # This maps the 'register/' URL to the StudentRegistrationView,
    # which handles the registration form
    # The 'student_registration' name is used to easily reference
    # this URL in templates and views
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration'
    ),
    # URL pattern for enrolling a student in a course.
    # This maps the 'enroll-course/' URL to the StudentEnrollCourseView,
    # which allows the logged-in user to select a course and enroll in it.
    # The 'student_enroll_course' name is used to easily reference this URL
    # in templates and views.
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'
    ),
    # URL pattern for listing all courses a student is enrolled in.
    # This maps the 'courses/' URL to the StudentCourseListView, which displays a list of the student's courses.
    # The 'student_course_list' name is used to reference this URL in templates and views.
    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'
    ),

    # URL pattern for displaying the details of a specific course.
    # This maps the 'course/<pk>/' URL to the StudentCourseDetailView, which shows details of a particular course.
    # The 'pk' (primary key) is passed to identify the specific course.
    # The 'student_course_detail' name is used to reference this URL in templates and views.
    path(
        'course/<pk>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail'
    ),

    # URL pattern for displaying the details of a specific course with an additional module ID.
    # This maps the 'course/<pk>/<module_id>/' URL to the StudentCourseDetailView, which shows a specific course along with the selected module.
    # The 'module_id' is passed to identify a particular module in the course.
    # The 'student_course_detail_module' name is used to reference this URL in templates and views.
    path(
        'course/<pk>/<module_id>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'
    ),


]
