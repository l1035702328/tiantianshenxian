# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 11:06
# @Author  : LZZ
# @FileName: mixin.py
# @Software: PyCharm
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
