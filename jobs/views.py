from django.shortcuts import render , redirect
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from .models import Job, Category, Company
from .forms import JobForm, CategoryForm, CompanyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication
from .forms import JobApplicationForm, Certificate
from io import BytesIO
# from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.core.mail import send_mail
from django.http import HttpResponse

@login_required
def apply_for_job(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            # Handle multiple certificate uploads
            if 'certificates' in request.FILES:
                for certificate in request.FILES.getlist('certificates'):
                    Certificate.objects.create(application=application, file=certificate)

            return redirect('job_list')  # Redirect to a success page or job list

    else:
        form = JobApplicationForm()

    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job})

class JobList(ListView):
    model = Job
    template_name = 'jobs/job_list.html'

class JobDetail(DetailView):
    model = Job  
    template_name = 'jobs/job_detail.html'

class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/add_job.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/edit_job.html'
    success_url = reverse_lazy('job_list')

class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/delete.html'
    success_url = reverse_lazy('job_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])
    
class JobDeleteConfirm(DeleteView):
    model = Job
    template_name = 'jobs/delete_confirm.html'
    success_url = reverse_lazy('job_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Job, slug=self.kwargs['job_slug'])

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        job.delete()
        return HttpResponseRedirect(self.success_url)

# Category Views
class CategoryList(ListView):
    model = Category
    template_name = 'jobs/category_list.html'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'jobs/category_detail.html'

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'jobs/add_category.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'jobs/edit_category.html'
    success_url = reverse_lazy('category_list')

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'jobs/delete_category.html'
    success_url = reverse_lazy('category_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs['slug'])

# Company Views
class CompanyList(ListView):
    model = Company
    template_name = 'jobs/company_list.html'

class CompanyDetail(DetailView):
    model = Company
    template_name = 'jobs/company_detail.html'

class CompanyCreate(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'jobs/add_company.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'jobs/edit_company.html'
    success_url = reverse_lazy('company_list')

class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'jobs/delete_company.html'
    success_url = reverse_lazy('company_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Company, slug=self.kwargs['slug'])


def test_email(request):
    subject = "Test Email"
    message = "This is a test email from your Django application."
    recipient_list = ["davidmwape376@gmail.com"]  # Replace with your actual email

    try:
        send_mail(
            subject,
            message,
            'resgreentech@gmail.com',  # Your EMAIL_HOST_USER
            recipient_list,
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {e}")