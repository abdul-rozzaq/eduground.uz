from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

from home.models import *


def home_page(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    if ec_id:        
        ec = EducationCenter.objects.get(pk=ec_id)
        if request.user.is_authenticated:

            return render(request, 'index.html', {'ec': ec})

        else:
            return redirect('user-login')    
    else:
        return redirect('ec-login')


def peoples_page(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    peoples = People.objects.filter(ec__id=ec_id)
    
    context = {'peoples' : peoples, 'ec' : ec}

    return render(request, 'peoples.html', context)


def people_page(request: WSGIRequest, pk: int):
    if 'edit' in request.GET:
        pass
    elif 'delete' in request.GET:
        pass


    return redirect('home-page')




def peoples(request):
    peoples = People.objects.all()
    return render(request, 'peoples.html',{
        'peoples':peoples
    })



def teachers(request):
    
    return render(request, 'teachers.html',{})


def course(request):
    return render(request, 'course.html',{})



def group(request):
    return render(request,'group.html')


def moliya(request):
    return render(request,'moliya.html',{})


def settings(request):
    return render(request, 'settings.html',{})
