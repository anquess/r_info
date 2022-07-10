from django import template

register = template.Library()


@register.filter
def keyword(querydict):
    keyword = querydict.get('keyword')

    return "" if keyword is None else keyword


@register.filter
def eqtype(querydict):
    eqtype = querydict.get('eqtype')

    return "" if eqtype is None else eqtype


@register.filter
def is_all(querydict):
    is_all = querydict.get('is_all')

    return "" if is_all is None else 'checked'


@register.filter
def remove_dirs(path):
    path = path.split('/')[-1]

    return "" if path is None else path
