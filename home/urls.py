from django.urls import path
from .views import *



urlpatterns = [
    path('', home_page, name='home-page'),
    path('lids/', lids, name='lids'),
    path('peoples/', peoples, name='peoples'),
    path('teachers/', teachers, name='teachers'),
    path('courses/', course, name='course'),
    path('group/', group, name='group'),
    path('finance/', finance, name='finance'),
    path('settings/', settings, name='settings'),

    # Detail

    path('group/<int:pk>/', group_detail, name='group-detail'),
    path('course/<int:pk>/', course_detail, name='course-detail'),
    path('teacher/<int:pk>/', teacher_detail, name='teacher-detail'),
]

