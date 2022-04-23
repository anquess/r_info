from django import template

register = template.Library()


@register.filter
def keyword(querydict):
    keyword = querydict.get('keyword')

    return "" if keyword is None else keyword
