from django.contrib import admin
# Register your models here.
from . models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name' ,'last_name' ,'email' ,'phone_number' ,'created_at' ,'updated_at']

admin.site.register(Student,StudentAdmin)
