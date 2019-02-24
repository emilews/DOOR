from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('door_code/', views.LogIn, name='get-code'),
    path('getpass/', views.GetPassword, name='password'),
]