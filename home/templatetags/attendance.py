from django import template
from home.models import *
from attendance.models import Attendance

import datetime as dt
import datetime


register = template.Library()


@register.simple_tag
def attendance(group: Group, people, day):
    date = datetime.date(datetime.date.today().year, datetime.date.today().month, day)  

    try:
        at = Attendance.objects.get(
            ec=group.course.ec,
            date=date,
            group=group
        )
        
        if people in at.peoples.all():
            return 'checked'    
    
    except Exception as e:
        at = Attendance.objects.create(
            ec=group.course.ec,
            date=date,
            group=group,
        )

        
    
    