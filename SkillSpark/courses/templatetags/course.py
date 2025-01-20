from django import template

# Registering the custom template filter to make it available in templates.
register = template.Library()

@register.filter
def model_name(obj):
    """
    Returns the model name of a given Django model instance.

    Args:
        obj: The Django model instance whose model name is to be retrieved.

    Return:
        str: The model name if the object has a `_meta` attribute.
        None: If the object does not have a `_meta` attribute (e.g., invalid object).
    """
    try:
        # Access the model name from the object's metadata.
        return obj._meta.model_name
    except AttributeError:
        # Return None if the object doesn't have the `_meta` attribute.
        return None
