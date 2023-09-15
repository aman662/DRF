from django.conf import settings
import os
import pdfkit
import tempfile

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from django.urls import reverse

from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework import generics, status, filters
from django.views import View
from drf_yasg.utils import swagger_auto_schema

from . models import *
from . serializers import StudentSerializer

from project1.response import render_html_response
from .templatetags.hashid_filters import hashids




# Create your views here.

class StudentListView(generics.ListAPIView):
    """
    View to get the listing of all students.
    Supports both HTML and JSON response formats.
    """
    serializer_class = StudentSerializer
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    template_name = 'student_list.html'
    
    def get_queryset(self):
       queryset = Student.objects.all()
       return queryset
    

    def get(self, request, *args, **kwargs):
        """
        Handle both AJAX (JSON) and HTML requests.
        """
        queryset = self.get_queryset()
        if request.accepted_renderer.format == 'html':
            context = {'students': queryset}
            return render_html_response(context, self.template_name)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(
                status_code=status.HTTP_200_OK,
                message="Data retrieved",
                data=serializer.data
            )
    
    

class StudentaddView(generics.ListAPIView):
    """
    View to get the listing of all contacts.
    Supports both HTML and JSON response formats.
    """
    serializer_class = StudentSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'student_form.html'

    @swagger_auto_schema(operation_id='Get Student Form')
    def get(self, request, *args, **kwargs):
        queryset = Student.objects.all()

        if request.accepted_renderer.format == 'html':
            serializer = self.serializer_class()  # Create an instance of the serializer
            context = {'students': queryset, 'serializer': serializer}
            return render_html_response(context, self.template_name)
        else:
            # Return a JSON response if the format is not HTML
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        
    @swagger_auto_schema(operation_id='Post Student Form')   
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add or update a contact.
        """
        message = "Congratulations! your contact has been added successfully."
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            if request.accepted_renderer.format == 'html':
                messages.success(request, message)
                return redirect('student_list')

            else:
                # Return JSON response with success message and serialized data
                return Response(status_code=status.HTTP_201_CREATED,
                                    message=message,
                                    data=serializer.data
                                    )
        else:
            # Invalid serializer data
            if request.accepted_renderer.format == 'html':
                # Render the HTML template with invalid serializer data
                context = {'serializer':serializer}
                return render_html_response(context,self.template_name)
            else:   
                # Return JSON response with error message
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                    message="We apologize for the inconvenience, but please review the below information.",
                                    data=(serializer.errors))
            
        
class StudentUpdateView(generics.UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'student_form.html'
    serializer_class = StudentSerializer

    
    def get_student_instance(self, encoded_id):
        try:
            # Decode the encoded_id using Hashids
            id = hashids.decode(encoded_id)[0]
            # Fetch the student instance by the decoded ID
            instance = Student.objects.get(pk=id)
            return instance
        except (IndexError, Student.DoesNotExist):
            return None

    def get(self, request, encoded_id, *args, **kwargs):
        # Fetch the student instance
        instance = self.get_student_instance(encoded_id)

        if instance:
            # If the student instance exists, proceed with rendering the form
            serializer = self.serializer_class(instance=instance, context={'request': request})
            context = {'serializer': serializer, 'instance': instance}
            return render(request, self.template_name, context)
        else:
            # Handle the case where the student instance does not exist
            messages.error(request, "You are not authorized to perform this action")
            return redirect(reverse('student_list'))



    def post(self, request, encoded_id, *args, **kwargs):
        data = request.data

        # Fetch the student instance
        instance = self.get_student_instance(encoded_id)

        if instance:
            # Initialize the serializer with the instance and provided data
            serializer = self.serializer_class(instance=instance, data=data)

            if serializer.is_valid():
                # If the serializer data is valid, save the updated student instance
                serializer.save()
                message = "Your student has been updated successfully!"

                if request.accepted_renderer.format == 'html':
                    # For HTML requests, display a success message and redirect to student_list
                    messages.success(request, message)
                    return redirect('student_list')
                else:
                    # For API requests, return a success response with serialized data
                    return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                if request.accepted_renderer.format == 'html':
                    # For HTML requests with invalid data, render the template with error messages
                    context = {'serializer': serializer, 'instance': instance}
                    return render(request, self.template_name, context)
                else:
                    # For API requests with invalid data, return an error response with serializer errors
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = "You are not authorized to perform this action"
            if request.accepted_renderer.format == 'html':
                # For HTML requests with no instance, display an error message and redirect to student_list
                messages.error(request, error_message)
                return redirect('student_list')
            else:
                # For API requests with no instance, return an error response with an error message
                return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)



class StudentDetailView(View):
    template_name = 'student_view.html'

    def get(self, request, student_id, *args, **kwargs):
        try:
            # Fetch the student based on the provided student_id
            student = Student.objects.get(pk=student_id)
            
            # Retrieve projects and academic info related to this student
            projects = project.objects.filter(student_id=student)
            academic_info = AcedemicInfo.objects.filter(student_id=student)

            # Create a context dictionary with data specific to this student
            context = {
                'student_data': student,
                'projects': projects,
                'academic_info': academic_info,
            }

            return render(request, self.template_name, context)
        except Student.DoesNotExist:
            # Handle the case where the student does not exist
            messages.error(request, "Student not found")
            return redirect(reverse('student_list'))
        

class GeneratePDFView(View):
    def get(self, request, student_id, *args, **kwargs):
        try:
            # Fetch the student based on the provided student_id
            student = Student.objects.get(pk=student_id)

            # Retrieve projects and academic info related to this student
            projects = project.objects.filter(student_id=student)
            academic_info = AcedemicInfo.objects.filter(student_id=student)

            # Create a context dictionary with data specific to this student
            context = {
                'student_data': student,
                'projects': projects,
                'academic_info': academic_info,
            }

            # Specify the path to the wkhtmltopdf executable
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

            # Render the HTML template to a string
            template = get_template('student_view.html')
            html = template.render(context)

            # Define the options for PDF generation
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
            }

            # Construct the filename based on student data
            filename = f"{student.first_name}-data.pdf"

            # Generate the PDF using pdfkit and save it to a temporary file
            pdf_file_path = tempfile.mktemp(suffix='.pdf')
            pdfkit.from_string(html, pdf_file_path, options=options)

            # Prepare the response to serve the PDF for download
            with open(pdf_file_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Remove the temporary PDF file
            os.remove(pdf_file_path)

            return response
        except Student.DoesNotExist:
            # Handle the case where the student does not exist
            messages.error(request, "Student not found")
            return redirect(reverse('student_list'))