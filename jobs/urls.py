from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    JobList, JobDetail, JobCreate, JobUpdate, JobDelete, JobDeleteConfirm, 
    CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete, 
    CompanyList, CompanyDetail, CompanyCreate, CompanyUpdate, CompanyDelete
)
from .api import JobListAPI, JobDetailAPI, CompanyListAPI, CompanyDetailAPI
from .views import apply_for_job


urlpatterns = [
    # Job URLs
    path('', JobList.as_view(), name='job_list'),
    path('add/', JobCreate.as_view(), name='add_job'),
    path('<slug:slug>/', JobDetail.as_view(), name='job_detail'),
    path('<slug:slug>/edit/', JobUpdate.as_view(), name='edit_job'),
    path('<slug:slug>/delete/', JobDelete.as_view(), name='delete_job'),
    path('<slug:slug>/delete/confirm/', JobDeleteConfirm.as_view(), name='delete_job_confirm'),

    # Category URLs
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/add/', CategoryCreate.as_view(), name='category_add'),
    path('categories/<slug:slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/<slug:slug>/edit/', CategoryUpdate.as_view(), name='category_edit'),
    path('categories/<slug:slug>/delete/', CategoryDelete.as_view(), name='category_delete'),

    # Company URLs
    path('companies/', CompanyList.as_view(), name='company_list'),
    path('companies/add/', CompanyCreate.as_view(), name='company_add'),
    path('companies/<slug:slug>/', CompanyDetail.as_view(), name='company_detail'),
    path('companies/<slug:slug>/edit/', CompanyUpdate.as_view(), name='company_edit'),
    path('companies/<slug:slug>/delete/', CompanyDelete.as_view(), name='company_delete'),

    # API URLs
    path('api/jobs/', JobListAPI.as_view(), name='api_job_list'),
    path('api/jobs/<int:pk>/', JobDetailAPI.as_view(), name='api_job_detail'),
    path('api/companies/', CompanyListAPI.as_view(), name='api_company_list'),
    path('api/companies/<int:pk>/', CompanyDetailAPI.as_view(), name='api_company_detail'),

    path('jobs/<slug:job_slug>/apply/', apply_for_job, name='apply_for_job'),
    path('job/<int:pk>/', JobDetail.as_view(), name='job_detail')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
