from django import template
from home.models import *
import datetime as dt

register = template.Library()

@register.simple_tag
def safetime(x):
    hour = x.split(':')[0]
    min = x.split(':')[1]
    time = f'{hour}:{min}'

    return time
    