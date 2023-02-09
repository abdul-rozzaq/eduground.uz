from django.urls import path
from django.http import HttpResponse

import json

from .models import *


def people_serializer(p):
    return {'pk': p.pk, 'full-name': p.full_name}


def group_serializer(p):
    return {'pk': p.pk, 'name': p.name}


def peoples(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)

    q = request.GET.get('q')

    qs = People.objects.filter(ec=ec, full_name__icontains=q)

    response = [people_serializer(i) for i in qs]

    return HttpResponse(json.dumps(response))


def groups(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)

    pk = request.GET.get('id')
    if pk:
        qs = Group.objects.filter(course__ec=ec, peoples__pk=pk)
    else:
        qs = Group.objects.filter(course__ec=ec)

    response = [group_serializer(i) for i in qs]
    return HttpResponse(json.dumps(response))


urlpatterns = [
    path('peoples/', peoples),
    path('groups/', groups),
]
