import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from celery_tasks.tasks import send_register_active_email

# Create your views here.
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
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
        # # 利用celery异步发邮件经过task装饰有了delay
        send_register_active_email.delay(email, username, token)
        # subject = '天天生鲜欢迎信息'
        # message = '邮件正文'
        # html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员' \
        #                    '</h1>请点击下面链接激活您的账户<br/>' \
        #                '<a href="http://127.0.0.1:8000/user/active/%s">' \
        #                'http://127.0.0.1:8000/user/active/%s' \
        #                '</a>' % (username, token, token)
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # send_mail(subject, message, sender, receiver,html_message=html_message)
        # 返回应答
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密,获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse("激活链接已过期")

class LoginView(View):
    '''登录'''
    def get(self, request):
        #判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self,request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        print(username)
        print(password)
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': "数据不完整"})
        # 业务处理
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                # print("User is valid, active and authenticated")
                login(request, user)  # 登录并记录用户的登录状态
                response = redirect(reverse('goods:index'))
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response


            else:
                # print("The passwoed is valid, but the account has been disabled!")
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# /user
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self, request):
        return render(request, 'user_center_info.html')


# /user/order
class UserOrderView(View):
    def get(self,request):
        '''用户中心-订单页'''
        return render(request, 'user_center_order.html')


# /user/address
class AddressView(View):
    def get(self,request):
        '''用户中心-地址页'''
        return render(request, 'user_center_site.html')


# /user/logout
class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))