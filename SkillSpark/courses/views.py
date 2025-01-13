from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Course
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
