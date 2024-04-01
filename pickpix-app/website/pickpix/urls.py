from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('voucher/', views.voucher, name='voucher'),
    path('token_price/', views.token_price, name='token_price'),
]
