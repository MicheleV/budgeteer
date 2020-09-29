from django import template

register = template.Library()

# TODO: handle 0 and None
@register.filter(name='sub')
def subtract(value, arg):
    """Return the difference between value and arg """
    return value - arg


# Credits https://stackoverflow.com/a/8000078
@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]
