from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from students.forms import CourseEnrollForm
from .models import Course
from django.core.cache import cache
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from django.apps import apps
from django.forms.models import modelform_factory
from .models import Module, Content
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


class OwnerMixin:
    """
    Mixin to restrict queryset to objects owned by the logged-in user.
    """
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OwnerEditMixin:
    """
    Mixin to automatically assign the logged-in user as the owner when creating or editing objects.
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Base mixin for course-related views with common attributes.
    """
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Mixin for editing courses with a predefined template.
    """
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    View to display a list of courses owned by the logged-in user.
    """
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    View to create a new course.
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    View to update an existing course.
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    View to delete an existing course.
    """
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    View to manage the modules of a specific course using a formset.
    Allows updating, adding, and deleting modules inline.
    """
    template_name = 'courses/manage/module/formset.html'  # Template to render the formset
    course = None  # Placeholder for the course object

    def get_formset(self, data=None):
        """
        Create and return a ModuleFormSet instance.
        Args:
            data (dict, optional): Form data for binding. Defaults to None.
        Return:
            ModuleFormSet: A formset instance for managing course modules.
        """
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """
        Handle the incoming request and fetch the course object.
        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): Primary key of the course to be fetched.
        Return:
            HttpResponse: The response to the request.
        """
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user  # Ensure the course belongs to the logged-in user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to display the formset.
        Args:
            request (HttpRequest): The HTTP request object.
        Return:
            HttpResponse: Renders the template with the course and formset context.
        """
        formset = self.get_formset()  # Initialize an unbound formset
        return self.render_to_response(
            {'course': self.course, 'formset': formset}  # Pass context to the template
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to process the submitted formset.
        Args:
            request (HttpRequest): The HTTP request object.
        Return
            HttpResponse: Redirects on success or re-renders the template with errors.
        """
        formset = self.get_formset(data=request.POST)  # Bind the formset with POST data
        if formset.is_valid():
            formset.save()  # Save valid data
            return redirect('manage_course_list')  # Redirect to course management list
        return self.render_to_response(
            {'course': self.course, 'formset': formset}  # Re-render with formset errors
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """
    Handles the creation and update of content for a course module.
    """

    module = None  # The module associated with the content.
    model = None   # The content model (e.g., text, video, image, file).
    obj = None     # The specific content object being updated (if applicable).
    template_name = 'courses/manage/content/form.html'  # Template for the form.

    def get_model(self, model_name):
        """
        Retrieves the model class for the given model name.

        Args:
            model_name (str): The name of the model (e.g., 'text', 'video').

        Returns:
            Model: The Django model class, or None if the name is invalid.
        """
        if model_name in ['text', 'video', 'image', 'file']:
            # Dynamically fetch the model class from the 'courses' app.
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """
        Creates a model form for the specified model.

        Args:
            model (Model): The model class for which the form is created.
            *args: Positional arguments for the form.
            **kwargs: Keyword arguments for the form.

        Returns:
            Form: A Django ModelForm instance.
        """
        # Exclude specific fields from the generated form.
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        Processes the request and prepares the context for the view.

        Args:
            request (HttpRequest): The HTTP request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content object (for updates).

        Returns:
            HttpResponse: The response generated by the view.
        """
        # Fetch the module for the course owned by the current user.
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            # Fetch the specific content object if updating.
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)


    def get(self, request, module_id, model_name, id=None):
        """
        Displays the form for content creation or editing.

        Args:
            request (HttpRequest): The HTTP request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content object (for editing).

        Returns:
            HttpResponse: The response containing the form for the content.
        """
        # Initialize the form based on the current object or an empty form for new content.
        form = self.get_form(self.model, instance=self.obj)
        context = {'form': form}
        if self.obj:
            context['object'] = self.obj  # Add the object to context if it's being edited.

        return self.render_to_response(context)

    def post(self, request, module_id, model_name, id=None):
        """
        Processes the form submission for creating or updating content.

        Args:
            request (HttpRequest): The HTTP request object.
            module_id (int): The ID of the module.
            model_name (str): The name of the content model.
            id (int, optional): The ID of the content object (for editing).

        Returns:
            HttpResponse: A redirect to the module content list or re-rendering the form with errors.
        """
        # Construct the form with data from the request (POST and FILES).
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user  # Assign the current user as the owner of the content.
            obj.save()

            # If creating new content, link it to the module.
            if not id:
                Content.objects.create(module=self.module, item=obj)

            # Redirect to the module content list after saving the content.
            return redirect('module_content_list', self.module.id)

        # If the form is invalid, re-render the form with errors.
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    """
    A view to handle the deletion of content from a course module.

    This view allows the deletion of a specific content item associated with
    a course module. It ensures that only the course owner (user) can delete
    content within their course.

    Methods:
        post(request, id):
            Handles the POST request to delete a specific content item.
            The content item is deleted, along with its associated content (e.g., file).
            The user is redirected to the module content list page after deletion.
    """
    def post(self, request, id):
        """
        Deletes a content item from a course module.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the content item to delete.

        Returns:
            HttpResponse: A redirect to the module content list page after deletion.
        """
        # Retrieve the content object, ensuring the user is the owner of the course.
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module  # Get the module associated with the content.

        # Delete the content item (e.g., file) and the content object itself.
        content.item.delete()
        content.delete()

        # Redirect the user to the module content list page.
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """
    A view to display a list of content for a specific course module.

    This view retrieves the module associated with the given `module_id` and
    renders a list of content items within that module. It ensures that only
    the course owner (user) can view the content of their own course module.

    Attributes:
        template_name (str): The template used to render the content list.
    Methods:
        get(request, module_id):
            Handles the GET request to retrieve the module and render its content list.
    """
    # Template for displaying the content list
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        """
        Retrieves and displays the content list for the specified module.

        Args:
            request (HttpRequest): The HTTP request object.
            module_id (int): The ID of the module for which content is being listed.

        Return:
            HttpResponse: A response rendering the module content list page.
        """
        # Retrieve the module object, ensuring the user is the owner of the course.
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        # Render the content list page with the module data.
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    Handles the reordering of modules via a JSON request.
    This view allows users to update the order of modules in a course.
    It processes a JSON payload containing module IDs and their new order,
    ensuring that only modules owned by the requesting user are updat
    Methods:
        post(request):
            Processes the POST request to reorder modules.
    """

    def post(self, request):
        """
        Updates the order of modules based on the JSON payload.
        Args:
            request (HttpRequest): The HTTP request containing the
            JSON payload with module IDs and their new order.
        Return:
            JsonResponse: A JSON response indicating the status of the operation.
        """
        # Iterate over the JSON payload to extract module IDs and their corresponding order.
        for id, order in self.request_json.items():
            # Update the order of the module if it belongs to the requesting user.
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        # Return a JSON response confirming the successful update.
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    Handles the reordering of content items within a module via a JSON request.

    This view processes a JSON payload containing content item IDs and their
    new order. It ensures that only content items owned by the requesting
    user and associated with their course are updated.

    Methods:
        post(request):
            Processes the POST request to reorder content items.
    """

    def post(self, request):
        """
        Updates the order of content items based on the JSON payload.

        Args:
            request (HttpRequest): The HTTP request containing the JSON
            payload with content item IDs and their new order.

        Return:
            JsonResponse: A JSON response indicating the status of the operation.
        """
        # Iterate over the JSON payload to extract content item IDs and their corresponding order.
        for id, order in self.request_json.items():
            # Update the order of the content item if it belongs to the requesting user and their course.
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)

        # Return a JSON response confirming the successful update of content item order.
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    """
    A class-based view that handles the display of a list of courses.
    It supports caching of subjects and courses to improve performance.
    """
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        """
        Handles GET requests to display a list of courses, either filtered by a specific subject
        or showing all courses. Caches subjects and courses to avoid repeated database queries.
        Arguments:
        - request: The HTTP request object.
        - subject: An optional subject slug used to filter courses by subject.
        Returns:
        - A rendered template with the context containing subjects, the selected subject, and courses.
        """
        # Attempt to fetch all subjects from the cache
        subjects = cache.get('all_subjects')

        # If subjects are not found in the cache (cache miss), query the database
        if not subjects:
            # Annotate subjects with the count of related courses
            subjects = Subject.objects.annotate(
                total_courses=Count('courses')
            )
            # Store the subjects in the cache for future requests
            cache.set('all_subjects', subjects)

        # Query all courses, annotate them with the count of related modules
        all_courses = Course.objects.annotate(
            total_modules=Count('modules')
        )

        # If a subject is provided in the URL, filter courses by that subject
        if subject:
            # Retrieve the subject object from the database, or return a 404 error if not found
            subject = get_object_or_404(Subject, slug=subject)

            # Cache key for courses related to a specific subject
            key = f'subject_{subject.id}_courses'
            # Attempt to fetch the courses for the specific subject from the cache
            courses = cache.get(key)

            # If courses for this subject are not in the cache (cache miss), query the database
            if not courses:
                # Filter courses by the given subject
                courses = all_courses.filter(subject=subject)
                # Store the filtered courses in the cache for future requests
                cache.set(key, courses)
        else:
            # If no specific subject is provided, fetch all courses
            courses = cache.get('all_courses')

            # If courses are not found in the cache (cache miss), query the database
            if not courses:
                # Retrieve all courses
                courses = all_courses
                # Store the courses in the cache for future requests
                cache.set('all_courses', courses)

        # Render the response with the context including subjects, selected subject, and courses
        return self.render_to_response(
            {
                'subjects': subjects,  # List of all subjects
                'subject': subject,    # The selected subject, if any
                'courses': courses     # List of courses (either all or filtered by subject)
            }
        )


class CourseDetailView(DetailView):
    """
    View to display the detailed information of a specific course.
    This view fetches a single course instance based on the primary key
    and renders its details in the specified template.
    """
    model = Course
    template_name = 'courses/course/detail.html'


def get_context_data(self, **kwargs):
    """
    Method to get the context data for rendering the template.
    It adds the enrollment form pre-populated with the selected course.
    """
    # Call the parent class's get_context_data method to get the existing context
    context = super().get_context_data(**kwargs)

    # Add the enrollment form to the context, pre-populated with the current course
    context['enroll_form'] = CourseEnrollForm(
        # Set the initial value of the 'course'field to the current course object
        initial={'course': self.object}
    )

    # Return the updated context to be used in the template
    return context
