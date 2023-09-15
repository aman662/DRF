from django.contrib import admin
from . models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags  # To strip HTML tags from the HTML message
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from import_export.admin import ImportExportModelAdmin



class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name' ,'last_name' ,'email' ,'phone_number' ,'created_at' ,'updated_at']
    list_per_page = 20



class projectAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['name' ,'description' ,'status' ,'start_date' ,'created_at' ,'updated_at']
    actions = ['mark_as_completed','mark_as_in_progress','delete_project_with_notification','export_selected_to_csv']


    def mark_as_completed(self, request, queryset):
        # Your custom action logic here
        queryset.update(status='completed')
    
    mark_as_completed.short_description = "Mark selected projects as completed"

    def mark_as_in_progress(self, request, queryset):
        # Your custom action logic to mark selected projects as in progress here
        queryset.update(status='in_progress')
    
    mark_as_in_progress.short_description = "Mark selected projects as in progress"


    def delete_project_with_notification(self, request, queryset):
        for project_obj in queryset:
            student = project_obj.student_id
            student_email = student.email
            student_name = student.first_name
            project_name = project_obj.name

            # Send an email notification to the student
            subject = 'Project Deleted'
            message = f"Your project '{project_name}' has been deleted."
            from_email = settings.EMAIL_HOST_USER  # Update with your email

            # Get a list of all superadmins
            superadmins = User.objects.filter(is_superuser=True).values_list('email', flat=True)

            # Combine the student's email and superadmin emails
            recipient_list = [student_email] + list(superadmins)
           

             # Render the HTML email template with context
            html_message = render_to_string('project_deleted_email.html', {
                'student_name': student_name,
                'project_name': project_name,
            })

            # Send the email with HTML content
            send_mail(
                subject,
                f"Your project '{project_name}' has been deleted.",
                from_email,
                recipient_list,  # Wrap recipient_email in a list
                html_message=html_message,  # HTML version
                fail_silently=True
)

            # Delete the project
            project_obj.delete()

    delete_project_with_notification.short_description = "Delete selected projects with notification"

    #export as a action
    def export_selected_to_csv(modeladmin, request, queryset):

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projects.csv"'

        # Create a CSV writer and write the header row
        csv_writer = csv.writer(response)
        csv_writer.writerow(['Name', 'Description', 'Status', 'Start Date', 'Created At', 'Updated At'])

        # Write data rows for selected projects
        for project_obj in queryset:
            csv_writer.writerow([
                project_obj.name,
                project_obj.description,
                project_obj.status,
                project_obj.start_date,
                project_obj.created_at,
                project_obj.updated_at,
            ])

        return response

    export_selected_to_csv.short_description = 'Export selected projects to CSV'



class AcedemicInfoAdmin(admin.ModelAdmin):
    list_display=['roll_no' ,'course' ,'department' ,'batch' ,'enroll_rate','created_at' ,'updated_at']

    
admin.site.register(Student,StudentAdmin)
admin.site.register(project,projectAdmin)
admin.site.register(AcedemicInfo,AcedemicInfoAdmin)