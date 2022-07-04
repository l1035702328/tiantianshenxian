import re

from django.conf import settings
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from apps.user.models import User


# def register(request):
#     print(request.method)
#     if request.method == "GET":
#         '''显示注册'''
#         print("hello")
#         return render(request, 'register.html')
#     else:
#         '''注册处理'''
#         # 接收数据
#         username = request.POST.get('username')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#         print(username,password,email)
#         # 进行数据校验
#         if not all([username, password, email]):
#             # 数据不完整
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#         # 校验邮箱
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#         # 进行业务处理:用户注册
#         if User.objects.filter(username=username):
#             return render(request, 'register.html', {'errmsg': '用户已存在'})
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#
#         # 返回应答
#         return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        '''显示注册'''
        print("hello")
        return render(request, 'register.html')

    def post(self, request):
        '''注册处理'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        print(username, password, email)
        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 进行业务处理:用户注册
        if User.objects.filter(username=username):
            return render(request, 'register.html', {'errmsg': '用户已存在'})
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 发送激活邮件，包含激活链接 /user/active/id
        # 加密用户的身份信息,生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info).decode("utf8")
        # 发邮件
        # 返回应答
        return redirect(reverse('goods:index'))
