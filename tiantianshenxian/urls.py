# -*-coding:utf-8-*-
from django.contrib import admin
from django.urls import path, include


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
#     path('search/', include('haystack.urls')),  # 全文检索框架
#     path('user/', include('user.urls', namespace='user')),  # 用户模块
#     path('cart/', include('cart.urls', namespace='cart')),  # 购物车模块
#     path('order/', include('order.urls', namespace='order')),  # 订单模块
#     path('', include('goods.urls', namespace='goods')),  # 商品模块
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include(("tinymce.urls", "tinymce"))),  # the routing of tinymce
    path("search/", include(("haystack.urls", "haystack"))),
    path("user/", include(("user.urls", "user"), namespace="user")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("order/", include(("order.urls", "order"), namespace="order")),
    path("", include(("goods.urls", "goods"), namespace="goods")),
]
