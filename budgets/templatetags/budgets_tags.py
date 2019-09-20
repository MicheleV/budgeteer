from django import template

register = template.Library()


@register.filter(name='sub')
def subtract(value, arg):
    return value - arg