from django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form):
    """
    Form used for enrolling a user in a course.
    It includes a hidden field for the selected course.
    """
    # Hidden field to store the selected course
    course = forms.ModelChoiceField(
        # Initially no courses are available in the queryset
        queryset=Course.objects.none(),
        widget=forms.HiddenInput  # The field will not be visible tothe user
    )

    def __init__(self, *args, **kwargs):
        """
        Override the form's constructor to dynamically set the queryset
        for the course field, allowing the user to select from all
        available courses.
        """
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        # Set the queryset to include all courses in the database
        self.fields['course'].queryset = Course.objects.all()
