from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """
    A custom PositiveIntegerField that automatically assigns an order value
    based on the specified fields (`for_fields`) within the same model.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        # Initialize the for_fields attribute to specify grouping criteria
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Automatically set the order value before saving the model instance.
        """
        # Check if the field value is unset (None)
        current_value = getattr(model_instance, self.attname)

        if current_value is None:
            try:
                # Query all objects of the same model
                queryset = self.model.objects.all()

                # Apply filtering based on `for_fields` if specified
                if self.for_fields:
                    filter_conditions = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    queryset = queryset.filter(**filter_conditions)

                # Get the latest item by order field
                last_item = queryset.latest(self.attname)
                new_value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                # If no matching objects exist, set value to 0
                new_value = 0

            # Assign the calculated order value
            setattr(model_instance, self.attname, new_value)

            return new_value

        # If a value already exists, use it as is
        return super().pre_save(model_instance, add)
