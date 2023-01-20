from django.urls import path
from .views import *



urlpatterns = [
    path('', home_page, name='home-page'),
    path('peoples/', peoples, name='peoples'),
    path("teachers/", teachers, name='teachers'),
    path('courses/', course, name='course'),
    path('group', group, name='group'),
    path('moliya/', moliya, name='moliya'),
    path('settings', settings, name='settings'),
    path('peoples/', peoples_page, name='peoples-page'),
    path('people/<int:pk>/', people_page, name='people-page'),
]

