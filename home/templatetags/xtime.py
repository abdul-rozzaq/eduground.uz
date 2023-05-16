from django import template
from home.models import *
import datetime as dt

register = template.Library()

@register.simple_tag
def interval(x: Group):
    if x.start_time < dt.datetime.now().time() < x.end_time:
        return True
    else:
        return False
    