from django.contrib import admin
from .models import Job, Category, Company, JobApplication
from django.utils.html import format_html



class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'nrc_number', 'age', 'experience', 'applied_at')
    list_filter = ('job', 'applicant', 'applied_at')
    search_fields = ('applicant__username', 'job__title', 'nrc_number')
    readonly_fields = ('created_at',)
    
    def applicant_email(self, obj):
        return obj.applicant.email

    applicant_email.short_description = 'Applicant Email'

    def nrc_copy_display(self, obj):
        if obj.nrc_copy:
            return format_html('<a href="{}">View NRC Copy</a>', obj.nrc_copy.url)
        return "No NRC Copy"

    nrc_copy_display.short_description = 'NRC Copy'

    def resume_display(self, obj):
        if obj.resume:
            return format_html('<a href="{}">View Resume</a>', obj.resume.url)
        return "No Resume"

    resume_display.short_description = 'Resume'

    def school_institution_display(self, obj):
        return obj.school_institution or "N/A"

    school_institution_display.short_description = 'School/Institution'

    def apply_documents(self, obj):
        return f"NRC Copy: {obj.nrc_copy_display}, Resume: {obj.resume_display}"

    apply_documents.short_description = 'Documents'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('applicant', 'job')

admin.site.register(JobApplication, JobApplicationAdmin)
class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0

class JobInline(admin.TabularInline):
    model = Job
    extra = 0

# class CertificateInline(admin.TabularInline):
#     model = Certificate
#     extra = 0

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
    inlines = [JobInline]  # Keeping this to allow adding jobs for companies

# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'agency', 'location', 'created_at', 'vacancy', 'job_nature')
#     list_filter = ('category', 'agency', 'job_nature', 'created_at')
#     search_fields = ('title', 'location', 'description', 'knowledge_requirements', 'education_experience')
#     prepopulated_fields = {'slug': ('title',)}

# @admin.register(JobApplication)
# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ('job', 'applicant', 'applied_at', 'nrc_number', 'age', 'school_institution', 'resume')
#     list_filter = ('job', 'applicant', 'applied_at')
#     search_fields = ('applicant__username', 'job__title')# If you want to prevent editing the applied_at field

admin.site.site_header = "Your Company Admin"
admin.site.site_title = "Your Company Admin Portal"
admin.site.index_title = "Welcome to Your Company Admin Portal"
