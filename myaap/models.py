from django.db import models
from ckeditor.fields import RichTextField

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


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ]

class project(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description  = RichTextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
DEPART_CHOICES =  [
    ('engineering', 'Engineering'),
    ('mechincal', 'Mechincal'),
    ('electrical', 'Electrical'),
    ('arts', 'Arts'),
    ('commerce', 'Commerce'),

    ]

class AcedemicInfo(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=50)
    course = models.CharField(max_length=255)
    department = models.CharField(max_length=20, choices=DEPART_CHOICES, default='engineering')
    batch = models.CharField(max_length = 255)
    enroll_rate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course
    

