from django import template

register = template.Library()


@register.filter
def remove_dirs(path):
    path = path.split('/')[-1]

    return "" if path is None else path
