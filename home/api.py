from django.urls import path
from django.http import HttpResponse

import json

from .models import *

people_serializer = lambda p: {'pk' : p.pk, 'full-name' : p.full_name}

def peoples(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
        
    q = request.GET.get('q')

    qs = People.objects.filter(ec=ec, full_name__icontains=q)

    response = [people_serializer(i) for i in qs]

    return HttpResponse(json.dumps(response))


urlpatterns = [
    path('peoples/', peoples),
]