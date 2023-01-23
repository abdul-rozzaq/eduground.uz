from django.contrib import admin
from .models import *
def reg(model, madmin=None):
    if madmin:
        admin.site.register(model, madmin)
    else:
        admin.site.register(model)



reg(EducationCenter)
reg(People)
reg(Teacher)
reg(Course)
reg(Group)
reg(Lid)