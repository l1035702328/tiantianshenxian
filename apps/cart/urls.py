# -*-coding:utf-8-*-
from django.contrib import admin
from django.urls import path, include

from apps.cart.views import CartInfoView, CartAddView, CartUpdateView, CartDeleteView

urlpatterns = [
    path("", CartInfoView.as_view(), name="show"),  # 购物车页面显示
    path("add", CartAddView.as_view(), name="add"),  # 购物车记录添加
    path("update", CartUpdateView.as_view(), name="update"),  # 购物车记录更新
    path("delete", CartDeleteView.as_view(), name="delete"),  # 购物车记录更新
]
