from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter(name='sub')
def subtract(value, arg):
    """
    Return the difference between value and arg
    """
    return value - arg

@register.filter(name='div')
def subtract(value, arg):
    """
    Return the result of value / arg
    """
    return floatformat((value / arg * 100.0) - 100, 2)
