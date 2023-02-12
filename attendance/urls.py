from django.urls import path
from .views import *
urlpatterns = [
    path('add-day/', add_day, name='add-day'),


]