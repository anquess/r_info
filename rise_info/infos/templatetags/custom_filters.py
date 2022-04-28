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
