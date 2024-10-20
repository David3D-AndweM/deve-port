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



from django.http import JsonResponse
from .utils import generate_content


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

from .utils import generate_content

# def ai_chatbot(request):
#     response_text = None
#     language = 'en'  # Default to English

#     if request.method == 'POST':
#         prompt = request.POST.get('prompt')
#         language = request.POST.get('language', 'en')
#         response_text = generate_content(prompt, language)

#     return render(request, 'ai_chatbot.html', {'response': response_text, 'language': language})

#     from django.http import JsonResponse
# from django.conf import settings

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

@require_POST
def chat_with_gemini(request, job_id):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if not user_message:
            return JsonResponse({'response': 'Please enter a message.'}, status=400)

        # Generate AI response using the Gemini API, passing the job ID
        ai_response = generate_content(user_message, job_id, language='en')
        return JsonResponse({'response': ai_response})

    return JsonResponse({'response': 'Invalid request method.'}, status=405)

# def ai_chat(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('message')
#         api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={settings.GEMINI_API_KEY}"
        
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "contents": [{"parts": [{"text": user_message}]}]
#         }

#         response = requests.post(api_url, json=data, headers=headers)
#         ai_response = response.json().get('contents', [{}])[0].get('parts', [{}])[0].get('text', 'Sorry, I couldn’t understand that.')

#         return JsonResponse({'response': ai_response})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests


# @csrf_exempt
# def chat_with_gemini(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()

        if not user_message:
            return JsonResponse({'reply': 'Please enter a message.'}, status=400)

        # Gemini API interaction
        gemini_api_url = (
            'https://generativelanguage.googleapis.com/v1beta/models/'
            'gemini-1.5-flash-latest:generateContent'
        )
        api_key = 'AIzaSyD2m9GuILFiOOO7fTVfojklo2MUAyA2Xd4'

        if not api_key:
            return JsonResponse({'reply': 'API key not found.'}, status=500)

        headers = {'Content-Type': 'application/json'}
        payload = {
            'prompt': {'text': user_message},
            'temperature': 0.7
        }

        try:
            response = requests.post(
                f'{gemini_api_url}?key={api_key}',
                json=payload,
                headers=headers,
                timeout=10  # Add timeout to avoid long waits
            )

            if response.status_code == 200:
                data = response.json()
                ai_reply = (
                    data.get('candidates', [{}])[0].get('output', 
                    'Sorry, I did not understand that.')
                )
                return JsonResponse({'reply': ai_reply})
            else:
                return JsonResponse(
                    {'reply': 'Error communicating with AI service.'},
                    status=response.status_code
                )

        except requests.exceptions.RequestException as e:
            return JsonResponse({'reply': f'Request failed: {str(e)}'}, status=500)

    return JsonResponse({'reply': 'Invalid request method.'}, status=405)

    from django.http import HttpResponse

# def test_post(request):
#     if request.method == 'POST':
#         return HttpResponse('POST method allowed')
#     return HttpResponse('Invalid request', status=405)


