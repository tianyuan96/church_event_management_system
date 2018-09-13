from django import template

register = template.Library()

@register.filter(name="keyvalue")
def keyvalue(dict, key):
    return dict[str(key)]