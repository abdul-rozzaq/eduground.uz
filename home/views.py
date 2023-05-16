import datetime
import openpyxl

from attendance.models import *
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from fuzzywuzzy import process, fuzz

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

def wuzzy(ec: EducationCenter, name):
    peoples = People.objects.filter(ec=ec)
    names = [x.full_name for x in peoples]

    return process.extract(name, names, limit=10)


def get_clean_name(name):
    try:
        ec = EducationCenter.objects.get(name=name)

        return False
    except EducationCenter.DoesNotExist:
        print('Name is DoesNotExist')
        return True


def sorter(x:dict):
    def get(l:list, s:str):
        for i in l:
            if i['day'] == s:
                return True, i

        return False, None


    resp = []

    for i in x.keys():
        splited = str(i).split('x')

        if not get(resp, splited[1])[0]:
            resp.append({
                'day' : splited[1],
                'peoples' : []
            })

        z = get(resp, splited[1])[1]

        z['peoples'].append(splited[0])

    return resp


def group_days_list(group):
    day = 1
    x = []

    while True:
        try:
            date = datetime.date(datetime.date.today().year, datetime.date.today().month, day)   
            day += 1
            if Day.objects.get(name=days[str(date.strftime('%A'))]) in group.days.all():
                x.append(int(date.day))

        except Exception as e:
            break

    return x


def calc_all_days(year, month, group):
    day = 1
    x = 0
    while True:
        try:
            date = datetime.date(year, month, day)
            day += 1   

            if Day.objects.get(name=days[str(date.strftime('%A'))]) in group.days.all():
                x += 1

        except Exception as e:
            break
    return x


def calc_couse_price(date, group:Group):
    
    lessons = 0

    year, month, day = map(int, str(date).split('-'))

    while True:
        try:
            date = datetime.date(year, month, day)
            day += 1   

            if Day.objects.get(name=days[str(date.strftime('%A'))]) in group.days.all():
                lessons += 1

        except Exception as e:
            break

    return group.course.price / calc_all_days(year, month, group) * lessons


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
    ec = EducationCenter.objects.get(pk=ec_id)

    print(wuzzy(ec))

    if ec:
        if request.user.is_authenticated:

            today = Day.objects.get(name=days[datetime.date.today().strftime('%A')])
        

            context = {
                'ec': ec,
                'lids' : Lid.objects.filter(ec=ec),
                'teachers' : Teacher.objects.filter(ec=ec),
                'peoples' : People.objects.filter(ec=ec),
                'courses' : Course.objects.filter(ec=ec),
                'today_groups' : Group.objects.filter(days=today, course__ec=ec), 
                'groups' : Group.objects.filter(course__ec=ec), 
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
            lid.data = _data
            lid.full_name = full_name
            lid.phone = phone
            lid.save()

        elif command == 'add-group':
            group_id = request.POST.get('group-id')
            lid_id = request.POST.get('lid-id')
        

            group = Group.objects.get(pk=group_id)
            lid = Lid.objects.get(pk=lid_id)

            people = People.objects.create(full_name=lid.full_name, phone=lid.phone, ec=ec)

            group.peoples.add(people)

            lid.delete()            
            

    lids = Lid.objects.filter(ec=ec)

    context = {
        'ec': ec,
        'page_name': 'Lid',
        'groups': Group.objects.filter(course__ec=ec),
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
                

                people = People.objects.create(
                    ec=ec,
                    full_name=full_name,
                    phone=phone,
                )

            except Exception as e:
                print('Error', str(e).strip())
        elif command == 'excel':
            try:
                file = request.FILES['file']
                array = excel_reader(file)

                for i in array:
                    if i[0] and i[1]:
                        full_name = i[0].strip()
                        phone = i[1]

                        People.objects.create(
                            ec=ec,
                            full_name=full_name,
                            phone=phone,
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

            # new_teacher
            new_teacher = Teacher.objects.create(
                ec=ec,
                full_name=full_name,
                phone=phone,
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
            is_active = True # request.POST.get('is_active')

            new_group = Group.objects.create(
                name=group_name,
                course=course,
                teacher=teacher,
                start_time=start_time,
                end_time=end_time,
                is_active=is_active
            )

            for i in days:
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



def exp(request: WSGIRequest):
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
        'page_name': "Chegirma",
        'payment_logs': PaymentLog.objects.filter(ec=ec),
        'groups': groups,
        'peoples': peoples,
    }

    return render(request, 'tabs/exp.html', context)



def settings(request: WSGIRequest):
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    context = {
        'ec': ec,
    }


    if request.method == 'POST':
        ec.color = request.POST['color']
        
        print(ec.name != request.POST['ec-name'] and request.POST['ec-name'] != '' and get_clean_name(request.POST['ec-name']))

        if ec.name != request.POST['ec-name'] and request.POST['ec-name'] != '' and get_clean_name(request.POST['ec-name']):
            ec.name = request.POST['ec-name']

        print(request.FILES)
        ec.logo = request.FILES['logo'] if request.FILES.get('logo') else ec.logo

        ec.save()

        return redirect('settings')


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
                    group.days.add(Day.objects.get(pk=int(i)))

                group.save()

            except Exception as e:
                print('Error', str(e).strip())
        elif command == 'add-people' and request.POST.get('people'):
            try:
                id = request.POST.get('people')
                people = People.objects.get(pk=id)
                added_date = request.POST.get('added-date')
                group.peoples.add(people)
                people.balans -= calc_couse_price(added_date, group)
            
                people.save()

            except Exception as e:
                print('Error', str(e).strip())
        elif command == 'attendance':
            attendance_list = request.POST.copy()
            attendance_list.pop('csrfmiddlewaretoken')
            attendance_list.pop('command')

            data = sorter(attendance_list) 
            print(data)
            
            for w in Attendance.objects.filter(date__year=datetime.date.today().year, date__month=datetime.date.today().month, group=group):
                w.peoples.clear()
            
            
            for y in data:
                at = Attendance.objects.get(
                    group=group,
                    date=datetime.date(datetime.date.today().year, datetime.date.today().month, int(y['day']))
                )
                print('Name:', at.group.name)
                print('Peoples:',at.peoples.all())
                at.peoples.clear()
                print('Peoples:',at.peoples.all())

                for i in y['peoples']:
                    at.peoples.add(People.objects.get(pk=int(i)))
            
            

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
        'group_days': group_days_list(group),
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


def delete_lid(request):
    pk = request.GET.get('pk')
    ec_id = request.session.get('ec-id')
    ec = EducationCenter.objects.get(pk=ec_id)
    lid = Lid.objects.get(pk=pk)

    if lid.ec == ec:
        lid.delete()

    return redirect('lids')
