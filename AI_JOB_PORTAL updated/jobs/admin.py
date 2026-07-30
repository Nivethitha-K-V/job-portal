from django.contrib import admin
from .models import Job, SavedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'experience', 'is_active', 'posted_at')
    list_filter = ('job_type', 'experience', 'is_active')
    search_fields = ('title', 'company', 'skills_required')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
