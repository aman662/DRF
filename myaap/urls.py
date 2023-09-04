from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
     path('add/',StudentaddView .as_view(), name='student_add'),
]