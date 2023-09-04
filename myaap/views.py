from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse

from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.response import Response

from . models import Student
from project1.response import render_html_response
from . serializers import StudentSerializer

# Create your views here.
class StudentaddView(generics.ListAPIView):
    """
    View to get the listing of all contacts.
    Supports both HTML and JSON response formats.
    """
    serializer_class = StudentSerializer
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'student_form.html'
   
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
                return redirect('student_add')

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