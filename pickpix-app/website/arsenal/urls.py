from django.urls import path

from . import arsenal

urlpatterns = [
    path('', arsenal.index, name='index'),
    path('generate_content/', arsenal.generate_content, name='generate_content'),
