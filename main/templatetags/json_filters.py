from django import template
import json

register = template.Library()

@register.filter
def load_json(value):
    """Load JSON string into Python object"""
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []