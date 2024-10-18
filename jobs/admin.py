from django.contrib import admin
from .models import Job, Category, Company

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
    # Removed JobInline since Category no longer has a ForeignKey to Job
    # inlines = [JobInline]  # Commented out or removed

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name', 'presentation')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [JobInline]  # Keeping this to allow adding jobs for companies

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'agency', 'location', 'created_at', 'vacancy', 'job_nature')
    list_filter = ('category', 'agency', 'job_nature', 'created_at')
    search_fields = ('title', 'location', 'description', 'knowledge_requirements', 'education_experience')
    prepopulated_fields = {'slug': ('title',)}
    # Removed CategoryInline since Job no longer has a ForeignKey to Category
    # inlines = [CategoryInline]  # Commented out or removed

admin.site.site_header = "Your Company Admin"
admin.site.site_title = "Your Company Admin Portal"
admin.site.index_title = "Welcome to Your Company Admin Portal"
