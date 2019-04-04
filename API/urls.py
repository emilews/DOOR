from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('login/', views.LogIn, name='login'),
    path('get_code/', views.GetCode, name='getcode'),
    path('set_password/', views.SetPassword, name='password'),
    path('signup/', views.SignUp, name="signup"),
]