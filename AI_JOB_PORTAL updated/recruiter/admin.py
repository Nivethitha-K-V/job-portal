from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'recruiter', 'industry', 'location')
    search_fields = ('company_name', 'recruiter__username')
