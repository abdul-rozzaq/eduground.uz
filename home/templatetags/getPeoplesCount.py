from django import template
from django.conf import settings
import os

from home.models import EducationCenter, People

register = template.Library()

@register.filter(name='getPeoplesCount')
def getPeoplesCount(ec: EducationCenter):
    
    peoples = People.objects.filter(ec=ec)

    return peoples.count
