import datetime
import openpyxl

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from openpyxl.reader.excel import ExcelReader

from home.models import *

days = {
    'Monday' : 'Dushanba',
    'Tuesday' : 'Seshanba',
    'Wednesday' : 'Chorshanba',
    'Thursday' : 'Payshanba',
    'Friday' : 'Juma',
    'Saturday' : 'Shanba',
    'Sunday' : 'Yakshanba',
}

def excel_reader(file):
    wb = openpyxl.load_workbook(file)

    worksheet = wb.worksheets[0]

    excel_data = list()

    for row in worksheet.iter_rows():
        row_data = list()
        for cell in row:
            row_data.append(cell.value)

        excel_data.append(row_data)

    return excel_data[1:]


def home_page(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    if ec_id:
        ec = EducationCenter.objects.get(pk=ec_id)
        if request.user.is_authenticated:

            today = Day.objects.get(name=days[datetime.date.today().strftime('%A')])
        

            context = {
                'ec': ec,
                'lids' : Lid.objects.filter(ec=ec),
                'teachers' : Teacher.objects.filter(ec=ec),
                'peoples' : People.objects.filter(ec=ec),
                'courses' : Course.objects.filter(ec=ec),
                'groups' : Group.objects.filter(days=today, course__ec=ec), 
            }
            return render(request, 'tabs/index.html', context)

        else:
            return redirect('user-login')
    else:
        return redirect('ec-login')


def lids(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)

    command = request.POST.get('command')
    if request.method == 'POST' and command:
        if command == 'create':
            data = request.POST
            full_name = data.get('full-name')
            phone = data.get('phone')
            _data = data.get('data')

            Lid.objects.create(
                ec=ec,
                full_name=full_name,
                phone=phone,
                data=_data
            )
        elif command == 'update':
            id = request.POST.get('id')
            data = request.POST
            full_name = data.get('full-name')
            phone = data.get('phone')
            _data = data.get('data')

            lid = Lid.objects.get(pk=id)
            lid.data = data
            lid.full_name = full_name
            lid.phone = phone
            lid.save()


    lids = Lid.objects.filter(ec=ec)

    context = {
        'ec': ec,
        'page_name': 'Lid',
        'lids': lids
    }

    return render(request, 'tabs/lids.html', context)


def peoples(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)

    command = request.POST.get('command')
    if request.method == 'POST' and command and command !='':
        if command == 'create':
            try:
                full_name = request.POST.get('full-name')
                phone = request.POST.get('phone')
                birthday = request.POST.get('birthday')

                people = People.objects.create(
                    ec=ec,
                    full_name=full_name,
                    phone=phone,
                    birthday=birthday
                )

            except Exception as e:
                print('Error', str(e).strip())
        elif command == 'excel':
            try:
                file = request.FILES['file']
                array = excel_reader(file)

                for i in array:
                    if i[0] and i[1] and i[2]:
                        full_name = i[0].strip()
                        phone = i[1]
                        year, month, day = i[2].split('.')
                        birthday = datetime.date(
                            int(year), 
                            int(month), 
                            int(day)
                        )

                        print(full_name, phone, birthday)
                        People.objects.create(
                            ec=ec,
                            full_name=full_name,
                            phone=phone,
                            birthday=birthday
                        )

            except Exception as e:
                print('Error', str(e).strip())

    peoples_list = People.objects.filter(ec__id=ec_id)
    context = {
        'peoples': peoples_list,
        'ec': ec,
        'page_name': 'Talaba',
    }

    return render(request, 'tabs/peoples.html', context)


def teachers(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full-name')
            phone = request.POST.get('phone')
            birthday = request.POST.get('birthday')

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
        'page_name': 'O\'qituvchi',
        'teachers': Teacher.objects.filter(ec=ec)
    }
    return render(request, 'tabs/teachers.html', context)


def course(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)

    if request.method == 'POST':
        data = request.POST

        name = data.get('name')
        duration = data.get('duration')
        price = data.get('price')

        new_course = Course.objects.create(
            ec=ec,
            name=name,
            duration=duration,
            price=price,
        )

    courses = Course.objects.filter(ec=ec)
    context = {
        'ec': ec,
        'page_name': 'Kurs',
        'courses': courses
    }
    return render(request, 'tabs/course.html', context)


def group(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    if request.method == 'POST':
        try:
            days = request.POST.getlist('days')
            group_name = request.POST.get('group-name')
            course_id = request.POST.get('course')
            teacher_id = request.POST.get('teacher')
            start_time = request.POST.get('start-time')
            hour = int(start_time.split(':')[0]) + 2
            min = int(start_time.split(':')[1])
            end_time = f'{hour}:{min}'
            teacher = Teacher.objects.get(pk=teacher_id)
            course = Course.objects.get(pk=course_id)
            is_active = request.POST.get('is_active')

            new_group = Group.objects.create(
                name=group_name,
                course=course,
                teacher=teacher,
                start_time=start_time,
                end_time=end_time,
                is_active=is_active
            )

            for i in days:
                print(i)
                new_group.days.add(Day.objects.get(pk=int(i)))

        except Exception as e:
            print('Error', str(e).strip())

    courses = Course.objects.filter(ec=ec)
    teachers = Teacher.objects.filter(ec=ec)
    days = Day.objects.all()
    groups = Group.objects.filter(course__ec=ec)

    context = {
        'ec': ec,
        'page_name': 'Guruh',
        'courses': courses,
        'teachers': teachers,
        'groups': groups,
        'days': days,
    }
    return render(request, 'tabs/group.html', context)


def finance(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    groups = Group.objects.filter(course__ec=ec)
    peoples = People.objects.filter(ec=ec)

    if request.method == 'POST':
        ds = request.POST

        month = ds.get('month').split('-')
        people_id = ds.get('people')
        summa = ds.get('summa')
        group_id = ds.get('group')

        month = datetime.date(int(month[0]), int(month[1]), 1)
        group = Group.objects.get(pk=group_id)
        people = People.objects.get(pk=people_id)

        PaymentLog.objects.create(
            ec=ec,
            money=summa,
            by=request.user,
            group=group,
            month=month,
            people=people
        )

        people.balans += int(summa)
        people.save()

    context = {
        'ec': ec,
        'page_name': "To'lov",
        'payment_logs': PaymentLog.objects.filter(ec=ec),
        'groups': groups,
        'peoples': peoples,
    }

    return render(request, 'tabs/finance.html', context)


def settings(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
    }
    return render(request, 'tabs/settings.html', context)


# Detail


def group_detail(request: WSGIRequest, pk):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    group = Group.objects.get(pk=pk)

    if request.method == 'POST' and request.POST.get('command'):
        command = request.POST.get('command')

        if command == 'update':
            try:
                days = request.POST.getlist('days')
                group_name = request.POST.get('group-name')
                teacher_id = request.POST.get('teacher')
                start_time = request.POST.get('start-time')
                teacher = Teacher.objects.get(pk=teacher_id)
                hour = int(start_time.split(':')[0]) + 2
                min = int(start_time.split(':')[1])
                end_time = f'{hour}:{min}'
                
                group.name = group_name
                group.start_time = start_time
                group.end_time = end_time
                group.teacher = teacher

                group.days.clear()

                for i in days:
                    print(i)
                    group.days.add(Day.objects.get(pk=int(i)))

                group.save()

            except Exception as e:
                print('Error', str(e).strip())
        elif command == 'add-people' and request.POST.get('people'):
            try:
                id = request.POST.get('people')
                people = People.objects.get(pk=id)

                group.peoples.add(people)

                people.balans -= int(group.course.price)
                people.save()

            except Exception as e:
                print('Error', str(e).strip())

    courses = Course.objects.filter(ec=ec)
    teachers = Teacher.objects.filter(ec=ec)
    days = Day.objects.all()
    groups = Group.objects.filter(course__ec=ec)
    peoples = People.objects.filter(ec=ec).exclude(group=group)

    context = {
        'ec': ec,
        'group': group,
        'courses': courses,
        'teachers': teachers,
        'groups': groups,
        'days': days,
        'peoples': peoples,
    }

    return render(request, 'details/group-detail.html', context)


def course_detail(request: WSGIRequest, pk):
    course = Course.objects.get(pk=pk)
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    groups = Group.objects.filter(course=course)

    if request.method == 'POST' and request.POST.get('put'):
        try:
            data = request.POST

            name = data.get('name')
            duration = data.get('duration')
            price = data.get('price')

            print(pk, name)

            course.name = name
            course.duration = duration
            course.price = price

            course.save()

        except Exception as e:
            print('Error', str(e).strip())

    context = {
        'ec': ec,
        'course': course,
        'groups': groups,

    }

    return render(request, 'details/course-detail.html', context)


def teacher_detail(request: WSGIRequest, pk):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    teacher = Teacher.objects.get(pk=pk)
    groups = Group.objects.filter(course__ec=ec, teacher=teacher)

    context = {
        'ec': ec,
        'teacher': teacher,
        'groups': groups,
    }

    return render(request, 'details/teacher-detail.html', context)
