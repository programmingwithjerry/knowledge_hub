from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class OrderField(models.PositiveIntegerField):
    """
    A custom model field for automatically managing the order of items.

    This field assigns an incremental order value to items in a queryset,
    optionally scoped to a set of fields (`for_fields`). It ensures that the
    order is unique and consistent for each scope.

    Attributes:
        for_fields (list[str]):
            A list of field names used to filter the queryset
            when determining the order. If `None`, the order
            is determined across all items in the model.
    """
    def __init__(self, for_fields=None, *args, **kwargs):
        """
        Initialize the OrderField.

        Args:
            for_fields (list[str], optional): Fields to scope the order.Defaults to None.
            *args: Additional positional arguments for PositiveIntegerField.
            **kwargs: Additional keyword arguments for PositiveIntegerField.
        """
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Calculate and assign the order value before saving the model instance.

        If the current field value is `None`, a new order value is assigned.
        The value is determined by finding the maximum value in the relevant
        queryset and incrementing it.

        Args:
            model_instance (models.Model): The instance being saved.
            add (bool): Whether this is a new instance being added.

        Return:
            int: The assigned or existing value for the field.
        """
        if getattr(model_instance, self.attname) is None:
            # No current value, assign a new order value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # Filter the queryset by the specified fields
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # Get the order of the last item
                last_item = qs.latest(self.attname)
                value = getattr(last_item, self.attname) + 1
            except ObjectDoesNotExist:
                # If no items exist, start with order 0
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            # Use the existing value
            return super().pre_save(model_instance, add)
