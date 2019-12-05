from django import template

register = template.Library()


@register.filter(name='sub')
def subtract(value, arg):
    """
    Return the difference between value and arg
    """
    return value - arg
