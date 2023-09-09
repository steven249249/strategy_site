from django import template

register = template.Library()

@register.filter
def replace_enter(value):
    return value.replace("&nbsp;","   ")