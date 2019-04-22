from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('first/', views.First, name='login1'),
    path('second/', views.Second, name='login2'),
    path('get_code/', views.GetCode, name='getcode'),
    path('set_password/', views.SetPassword, name='password'),
    path('signup/', views.SignUp, name="signup"),
]