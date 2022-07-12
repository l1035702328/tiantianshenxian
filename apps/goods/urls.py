# -*-coding:utf-8-*-
from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('index', views.IndexView.as_view(), name='index') # 首页
]
