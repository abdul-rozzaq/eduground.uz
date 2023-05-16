from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from django.http import HttpResponse

from home.models import EducationCenter


def asd(request):
    ec = EducationCenter.objects.get(name='test')
    qarz = 0

    

    return HttpResponse('<h1>Lorem ipsum</h1>')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('day/', include('attendance.urls')),
    path('', include('home.urls')),

    path('api/', include('home.api')),

    path('asd/', asd)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



