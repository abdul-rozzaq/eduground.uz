from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login as lgn, logout as lgt
from home.models import EducationCenter


def ec_login(request: WSGIRequest):
    lgt(request)
    context = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            ec = EducationCenter.objects.get(name=name, password=password)

            request.session['ec-id'] = ec.pk

            


            return redirect('user-login')
        except EducationCenter.DoesNotExist:
            context['error'] = 'Education center not found'
        except Exception as e:
            print('Error', e)

    template = 'accounts/login-ec.html'
    return render(request, template, context)

def user_login(request: WSGIRequest):
    context = {}

    ec_id = request.session.get('ec-id')
    if ec_id:        
        ec = EducationCenter.objects.get(pk=ec_id)
        context['ec'] = ec
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(request.POST)
            try:
                user = authenticate(request=request, username=username, password=password)

                if user:
                    if user in ec.admins.all():
                        lgn(user=user, request=request)

                        return redirect('home-page')
                    else:
                        context['error'] = f'There is no such user in the admin list of {ec.name}'
                else:
                    context['error'] = f'There is no such user in the admin list of {ec.name}'

            except Exception as e:
                context['error'] = str(e).split()



        template = 'accounts/login-user.html'
        return render(request, template, context)

    else:
        return redirect('ec-login')






def ec_logout(request: WSGIRequest):
    
    if request.session.get('ec-id'):
        request.session.pop('ec-id')
    if request.user.is_authenticated:
        lgt(request)
    return redirect('ec-login')