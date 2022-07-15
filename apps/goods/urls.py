# -*-coding:utf-8-*-
from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),  # 首页
    path('', views.IndexView.as_view(), name='index'),  # 首页
    path('goods/<str:goods_id>', views.DetailView.as_view(), name='detail'),  # 详情页
    path('list/<type_id>/<page>', views.ListView.as_view(), name='list')  # 列表页
]
