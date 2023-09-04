from rest_framework import serializers
from django.conf import settings
from .models import *
import re



class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        label=('First Name* '),  # Label for the field
        required=True, # Field is required
        max_length=100,
        style={
            "input_type": "text",
            "autofocus": False,
            "autocomplete": "off",
            "required": True,
        },
        error_messages={
            "required": "This field is required.",
            "blank": "First Name is required.",
        }, 
    )
    
    last_name = serializers.CharField(
        label=('Last Name* '), # Label for the field
        required=True,  # Field is required
        max_length=100,
        style={
            "input_type": "text",
            "autofocus": False,
            "autocomplete": "off",
            "required": True,   # HTML5 required attribute
        },
        error_messages={
            "required": "This field is required.",
            "blank": "Last Name is required.",
            "invalid": "Last Name can only contain characters.",
        },
    )
    
    email = serializers.EmailField(
        label=('Email* '), # Label for the field
        required=True,  # Field is required
        max_length=100,
        style={
            "input_type": "email",
            "autofocus": False,
            "autocomplete": "off",
            "required": True,   # HTML5 required attribute
            }, 
       
        error_messages={
            "required": "This field is required.",
            "blank": "Email is required.",
        },
    )
    phone_number = serializers.CharField(
        label='Phone Number* ', # Label for the field
        max_length=14, 
        min_length=10,
        required=True,   # Field is required
        error_messages={
            "required": "This field is required.",
            "blank": "Phone number is required.",
        }, 
    )
    class Meta:
        model = Student
        fields = ['first_name' ,'last_name','email', 'phone_number']

def validate_first_name(value):
    # Check if the first name contains only characters or letters with spaces
    if not re.match("^[a-zA-Z ]*$", value):
        raise serializers.ValidationError("First Name can only contain letters and spaces.")

def validate_last_name(value):
    # Check if the first name contains only characters
    if not re.match("^[a-zA-Z ]*$", value):
        raise serializers.ValidationError("Last Name can only contain letters and spaces.")