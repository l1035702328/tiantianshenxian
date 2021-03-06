# -*-coding:utf-8-*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views



urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    # path('register_handle', views.register_handle, name='register_handle')
    path('active/<str:token>', views.ActiveView.as_view(), name='active'),
    path('login', views.LoginView.as_view(), name='login'),

    # path('', login_required(views.UserInfoView.as_view()), name='user'),
    # path('order', views.UserOrderView.as_view(), name='order'),
    # path('address', views.AddressView.as_view(), name='address'),
    # path('logout', views.LogoutView.as_view(), name='logout')
    # 利用多继承实现
    path('', login_required(views.UserInfoView.as_view()), name='user'),
    path('order/<str:page>', views.UserOrderView.as_view(), name='order'),
    path('address', views.AddressView.as_view(), name='address'),
    path('logout', views.LogoutView.as_view(), name='logout')
]
