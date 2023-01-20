from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from home.models import *


def home_page(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    if ec_id:
        ec = EducationCenter.objects.get(pk=ec_id)
        if request.user.is_authenticated:

            return render(request, 'tabs/index.html', {'ec': ec})

        else:
            return redirect('user-login')
    else:
        return redirect('ec-login')


def peoples(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    peoples = People.objects.filter(ec__id=ec_id)

    context = {
        'peoples': peoples,
        'ec': ec,
        'page_name' : 'Talaba',
    }

    return render(request, 'tabs/peoples.html', context)


def teachers(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
        'page_name' : 'O\'qituvchi',
    }
    return render(request, 'tabs/teachers.html', context)


def course(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
        'page_name' : 'Kurs',
    }
    return render(request, 'tabs/course.html', context)


def group(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
        'page_name' : 'Guruh',
    }
    return render(request, 'tabs/group.html', context)


def finance(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
    }
    return render(request, 'tabs/finance.html', context)


def settings(request):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
    }
    return render(request, 'tabs/settings.html', context)
