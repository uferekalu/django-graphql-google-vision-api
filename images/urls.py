from django.urls import path
from django.contrib import admin

from .views import test_api, index

urlpatterns = [
    path('', index, name='index'),
    path('test/', test_api, name='index'),
]