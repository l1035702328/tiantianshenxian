# -*-coding:utf-8-*-
from django.conf.urls import url
from django.urls import path

from . import views



urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    # path('register_handle', views.register_handle, name='register_handle')
]
