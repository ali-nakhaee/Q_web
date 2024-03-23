"""Defines URL patterns for users"""

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('login_api/', obtain_auth_token),
    path('logout_api/', views.logout_api),
]
