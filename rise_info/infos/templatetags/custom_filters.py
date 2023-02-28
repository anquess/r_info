from django import template

register = template.Library()


@register.filter
def keyword(querydict):
    keyword = querydict.get('keyword')

    return "" if keyword is None else keyword

@register.filter
def date_min(querydict):
    date_min = querydict.get('date_min')

    return "" if date_min is None else date_min

@register.filter
def date_max(querydict):
    date_max = querydict.get('date_max')

    return "" if date_max is None else date_max


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
