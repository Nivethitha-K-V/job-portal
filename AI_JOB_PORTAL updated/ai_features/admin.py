from django.contrib import admin
from .models import ResumeAnalysis, SkillGapReport


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'analyzed_at')


@admin.register(SkillGapReport)
class SkillGapReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'match_percentage', 'generated_at')
