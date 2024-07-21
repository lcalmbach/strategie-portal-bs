from django import template

register = template.Library()

@register.simple_tag
def example_tag():
    return "This is an example custom tag."