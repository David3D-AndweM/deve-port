from django.contrib import admin
from .models import Job, Category, Company, JobApplication



@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'get_applicant', 'applied_at')  # Update to use the correct field
    list_filter = ('job', 'applied_at')  # Ensure 'applicant' is not included if it is not valid
    readonly_fields = ('applied_at',)

    def get_applicant(self, obj):
        return obj.applicant.username  # Return the username for display in the admin
    get_applicant.short_description = 'Applicant'
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
