from django.contrib import admin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from django.contrib import messages
from .models import Job, Category, Company, JobApplication

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'job', 'applicant', 'nrc_number', 'age', 'experience', 
        'applied_at', 'selected_for_interview', 'canceled', 
        'nrc_copy_display', 'resume_display'
    )
    list_filter = ('job', 'applicant', 'applied_at', 'selected_for_interview', 'canceled')
    search_fields = ('applicant__username', 'job__title', 'nrc_number')
    actions = ['send_email_notifications']

    def nrc_copy_display(self, obj):
        """Display NRC Copy link."""
        if obj.nrc_copy:
            return format_html('<a href="{}" target="_blank">View NRC Copy</a>', obj.nrc_copy.url)
        return "No NRC Copy"

    nrc_copy_display.short_description = 'NRC Copy'

    def resume_display(self, obj):
        """Display Resume link."""
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "No Resume"

    resume_display.short_description = 'Resume'

    @admin.action(description='Send Email Notifications')
    def send_email_notifications(self, request, queryset):
        """Send acceptance or rejection emails to selected applicants."""
        accepted = queryset.filter(selected_for_interview=True)
        rejected = queryset.filter(canceled=True)

        # Sending acceptance emails
        for application in accepted:
            subject = f"Congratulations, {application.first_name} {application.last_name}!"
            message = (
                f"Dear {application.first_name},\n\n"
                f"Congratulations! You've been selected for the job '{application.job.title}'. "
                "We look forward to seeing you at the interview.\n\n"
                "Best Regards,\nYour Company"
            )
            try:
                send_mail(
                    subject,
                    message,
                    'resgreentech@gmail.com',  # Your EMAIL_HOST_USER
                    [application.email or application.applicant.email],  # Fallback to applicant's email
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f"Failed to send email to {application.first_name} {application.last_name}: {str(e)}")

        # Sending rejection emails
        for application in rejected:
            subject = f"Job Application Update for {application.first_name} {application.last_name}"
            message = (
                f"Dear {application.first_name},\n\n"
                f"We regret to inform you that your application for '{application.job.title}' has not been successful.\n"
                "Thank you for your interest.\n\n"
                "Best Regards,\nYour Company"
            )
            try:
                send_mail(
                    subject,
                    message,
                    'resgreentech@gmail.com',  # Your EMAIL_HOST_USER
                    [application.email or application.applicant.email],  # Fallback to applicant's email
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f"Failed to send email to {application.first_name} {application.last_name}: {str(e)}")

        messages.success(request, "Emails sent successfully!")

    def get_urls(self):
        """Add custom URL for email sending."""
        urls = super().get_urls()
        custom_urls = [
            path('send-email/', self.admin_site.admin_view(self.send_email_view), name='send-email'),
        ]
        return custom_urls + urls

    def send_email_view(self, request):
        """Handle sending emails."""
        if request.method == "POST":
            # Handle form submission here if needed
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

admin.site.register(JobApplication, JobApplicationAdmin)

class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0

class JobInline(admin.TabularInline):
    model = Job
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name', 'presentation')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [JobInline]

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'agency', 'location', 'created_at', 'vacancy', 'job_nature')
    list_filter = ('category', 'agency', 'job_nature', 'created_at')
    search_fields = ('title', 'location', 'description', 'knowledge_requirements', 'education_experience')
    prepopulated_fields = {'slug': ('title',)}

admin.site.site_header = "Your Company Admin"
admin.site.site_title = "Your Company Admin Portal"
admin.site.index_title = "Welcome to Your Company Admin Portal"
