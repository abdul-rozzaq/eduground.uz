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
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full-name')
            phone =  request.POST.get('phone')
            birthday =  request.POST.get('birthday')

            # new_teacher
            new_teacher = Teacher.objects.create(
                ec=ec,
                full_name=full_name,
                phone=phone,
                birthday=birthday
            )
 
        except Exception as e:
            print('Error', str(e).strip())


    context = {
        'ec': ec,
        'page_name' : 'O\'qituvchi',
        'teachers' : Teacher.objects.filter(ec=ec)
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


def group(request: WSGIRequest):
    if request.method == 'POST':
        try:
            days = request.POST.getlist('days')
            group_name = request.POST.get('group-name')
            course_id = request.POST.get('course')
            teacher_id = request.POST.get('teacher')
            start_time = request.POST.get('start-time')
            teacher = Teacher.objects.get(pk=teacher_id)
            course = Course.objects.get(pk=course_id)
             
            print(request.POST)

            new_group = Group.objects.create(
                name=group_name,
                course=course,
                teacher=teacher,
                start_time=start_time
            )

            for i in days:
                print(i)
                new_group.days.add(Day.objects.get(pk=int(i)))

        except Exception as e:
            print('Error', str(e).strip())


    
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    courses = Course.objects.filter(ec=ec)
    teachers = Teacher.objects.filter(ec=ec)
    days = Day.objects.all()
    groups = Group.objects.filter(course__ec=ec)

    context = {
        'ec': ec,
        'page_name' : 'Guruh',
        'courses': courses,
        'teachers': teachers,
        'groups': groups,
        'days': days,
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
