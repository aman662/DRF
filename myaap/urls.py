from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    
     path('list/',StudentListView .as_view(), name='student_list'),
     path('add/',StudentaddView .as_view(), name='student_add'),
     path('info/<int:student_id>/', StudentDetailView.as_view(), name='student_details'),
     path('edit/<str:encoded_id>/',StudentUpdateView .as_view(),name='student_edit'),
     path('generate_pdf/<int:student_id>/', GeneratePDFView.as_view(), name='generate_pdf'),

]