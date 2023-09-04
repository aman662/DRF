from django.db import models


# model for student
class Student(models.Model): 
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127) 
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=127)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
