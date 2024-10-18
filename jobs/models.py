from django.db import models
from collections.abc import Iterable
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now




NATURE_TYPES = (
    ('Full Time','Full Time'),
    ('Part Time','Part Time'),
    ('Remote','Remote'),
    ('Freelance','Freelance'),
    ('Internship','internship'),
    )
TOWNS_IN_ZAMBIA = {
    'Chingola': 'Chingola',
    'Lusaka': 'Lusaka',
    'Kitwe': 'Kitwe',
    'Ndola': 'Ndola',
    'Livingstone': 'Livingstone',
    'Luanshya': 'Luanshya',
    'Mufulira': 'Mufulira',
    'Kabwe': 'Kabwe',
    'Solwezi': 'Solwezi',
    'Chipata': 'Chipata',
    'Kabwe': 'Kabwe',
    'Choma': 'Choma',
    'Siavonga': 'Siavonga',
    'Mansa': 'Mansa',
    'Kasama': 'Kasama',
    # Add other towns as necessary
}

class Job(models.Model):
    title = models.CharField(_('Title'),max_length=150)
    category = models.ForeignKey('Category',verbose_name=_('Category'),related_name='job_category',on_delete=models.SET_NULL,null=True,blank=True)
    agency = models.ForeignKey('Company',verbose_name=_('Company'),related_name='job_company',on_delete=models.SET_NULL,null=True,blank=True)
    location = models.CharField(_('Location'), max_length=150, choices=[(key, value) for key, value in TOWNS_IN_ZAMBIA.items()], default='Chingola')
    salary = models.FloatField(_('Salary (ZMW)'), help_text=_('Salary in Zambian Kwacha'))
    created_at = models.DateTimeField(_('Created at'),default=timezone.now)
    vacancy = models.IntegerField(_('Vacancy'),)
    job_nature = models.CharField(_('Job Nature'),max_length=20,choices=NATURE_TYPES) 
    application_date = models.DateField(_('Application Date'),)
    description = models.TextField(_('Description'),max_length=50000)
    knowledge_requirements = models.TextField(_('Knowledge & Requirements'),max_length=10000)
    education_experience = models.TextField(_('Education & Experience'),max_length=10000)
    slug = models.SlugField(null=True,blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Job.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def applications_count(self):
        return self.job_applications.count()


class Category(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    name = models.CharField(_('Name'),max_length=150)
    image = models.ImageField(_('Image'),upload_to='categories')
    job_count = models.IntegerField(_('Job Count'),)
    slug = models.SlugField(null=True,blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def total_jobs(self):
        return self.jobs.count()

class Company(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='companies')
    name = models.CharField(_('Name'),max_length=150)
    logo = models.ImageField(_('Logo'),upload_to='company')
    presentation = models.TextField(_('Presentation'),max_length=10000)
    website = models.TextField(_('Website'),max_length=300)
    email = models.TextField(_('Email'),max_length=300)
    slug = models.SlugField(null=True,blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def total_jobs(self):
        return self.jobs.count()


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    nrc_number = models.CharField(max_length=20)
    nrc_copy = models.FileField(upload_to='nrc/', null=True, blank=True)
    school_institution = models.CharField(max_length=255, blank=True, null=True)

    linkedIn_profile = models.URLField(blank=True)
    age = models.PositiveIntegerField()
    experience = models.PositiveIntegerField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)  # Add this line
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Application for {self.job.title} by {self.applicant.username}"

class Certificate(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='applications/certificates/')

    def __str__(self):
        return f"Certificate for {self.application.applicant.username}"