# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 15:21
# @Author  : LZZ
# @FileName: tasks.py
# @Software: PyCharm
import django
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiantianshenxian.settings")
django.setup()
app = Celery('celery_tasks.tasks', broker='redis://119.91.55.183:6379/8')

from django.template import loader, RequestContext
from apps.goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner



@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    subject = '天天生鲜欢迎信息'
    message = '邮件正文'
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员' \
                   '</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s' \
                   '</a>' % (username, token, token)
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)


@app.task
def generate_static_index_html():
    ''' 产生首页静态页面 '''
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
    # 获取首页分类商品展示信息
    for type in types:  # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)
        # 动态给type增加属性,分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners


    # 组织模板上下文
    context = {'types': types,
               'goods_banners': goods_banners,
               'promotion_banners': promotion_banners,
               }

    # 使用模板
    # 1.加载模板文件,返回模板对象
    temp = loader.get_template('static_index.html')
    # context = RequestContext(request, context)
    # 3.渲染模板
    static_index_html = temp.render(context)
    # 生成首页对应静态页面
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(static_index_html)
