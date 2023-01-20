from django.urls import path
from .views import *


urlpatterns = [
    path('ec-login/', ec_login, name='ec-login'),
    path('user-login/', user_login, name='user-login'),
    path('logout/', ec_logout, name='logout'),
    
]

