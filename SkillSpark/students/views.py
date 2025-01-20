from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
from .forms import CourseEnrollForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class StudentRegistrationView(CreateView):
    """
    View for handling student registration.
    It renders a registration form and authenticates
    the user upon successful submission.
    """
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm  # Use Django's built-in user creation form
    # Redirect to the course list upon successful registration
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        """
        This method is called when the form is valid.
        It authenticates the user and logs them in after registration.
        """
        # Call the parent class's form_valid method to save the user
        result = super().form_valid(form)

        # Get the cleaned data from the form
        cd = form.cleaned_data

        # Authenticate the user using the provided username and password
        user = authenticate(username=cd['username'], password=cd['password1'])

        # Log the user in if authentication is successful
        if user is not None:
            login(self.request, user)

        # Return the result of the parent class's form_valid method
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """
    View for enrolling a student in a course. This view requires
    the user to be logged in.
    The form allows the user to select a course to enroll in.
    """
    course = None  # Placeholder for the course the student will enroll in
    form_class = CourseEnrollForm  # Form used for course enrollment

    def form_valid(self, form):
        """
        Called when the submitted form is valid. This method adds
        the logged-in user
        to the students of the selected course.
        """
        # Get the course object from the cleaned data of the form
        self.course = form.cleaned_data['course']

        # Add the logged-in user to the students enrolled in the selected course
        self.course.students.add(self.request.user)

        # Call the parent class's form_valid method to handle
        # redirection and form processing
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after the form is successfully submitted.
        It redirects the user to the course detail page.
        """
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of courses that the currently logged-in student is enrolled in.
    Only authenticated users can access this view.
    """
    model = Course  # The model to query (Course model)
    template_name = 'students/course/list.html'  # The template used to render the list of courses

    def get_queryset(self):
        """
        Overriding the default queryset to filter courses and return only those that
        the currently logged-in student is enrolled in.
        """
        # Get the original queryset
        qs = super().get_queryset()

        # Filter the queryset to return only courses where the logged-in user is a student
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """
        Override the default queryset to filter the courses by the logged-in student.
        This ensures that only courses the student is enrolled in are accessible.
        """
        return Course.objects.filter(students=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Override the context data to add course and module information to the template context.
        It checks if a 'module_id' is passed and fetches the corresponding module; otherwise, 
        it fetches the first module of the course.
        """
        context = super().get_context_data(**kwargs)
        course = self.get_object()  # Get the current course object
        module_id = self.kwargs.get('module_id')

        # Fetch the module based on the 'module_id' or default to the first module
        context['module'] = course.modules.filter(id=module_id).first() or course.modules.first()

        return context
