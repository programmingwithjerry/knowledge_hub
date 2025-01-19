from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """
    Custom permission class to check if the user is enrolled in the course.
    This permission ensures that the user making the request is listed as a student
    in the specific course (i.e., they are enrolled in the course). If the user is
    not enrolled, the request will be denied.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is enrolled in the given course object.
        This method checks whether the authenticated user is part of the students
        enrolled in the specified course (obj). It is typically used in the context
        of checking access to a specific course object.

        Args:
            request: The HTTP request made by the user.
            view: The view that is processing the request.
            obj: The course object to which access is being requested.

        Returns:
            bool: True if the user is enrolled in the course, False otherwise.
        """
        # Check if the current authenticated user (request.user)
        # is in the list of students for the course
        return obj.students.filter(id=request.user.id).exists()
