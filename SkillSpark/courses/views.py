from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Course


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


class OwnerCourseMixin(OwnerMixin):
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


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    View to create a new course.
    """
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    View to update an existing course.
    """
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    View to delete an existing course.
    """
    template_name = 'courses/manage/course/delete.html'
