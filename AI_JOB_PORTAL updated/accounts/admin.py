from django.contrib import admin
from .models import UserProfile, Education, Skill, Resume, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'city', 'state', 'mobile')
    list_filter = ('role', 'state', 'gender')
    search_fields = ('full_name', 'user__username', 'mobile')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'college', 'passing_year')
    list_filter = ('qualification',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'skill_type', 'proficiency')
    list_filter = ('skill_type',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'resume_score', 'is_active')
    list_filter = ('is_active',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
