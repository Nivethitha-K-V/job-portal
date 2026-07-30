from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    recruiter = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=150, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.company_name
