from django import template
import datetime

register = template.Library()


@register.simple_tag
def input_domain(domain):
    return domain


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
