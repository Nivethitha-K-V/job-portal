from django.db import models
from django.contrib.auth.models import User


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_analyses')
    resume = models.ForeignKey('accounts.Resume', on_delete=models.CASCADE, related_name='analyses')
    score = models.PositiveSmallIntegerField(default=0)
    skills_detected = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"Analysis for {self.user.username} - score {self.score}"


class SkillGapReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_gap_reports')
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='skill_gap_reports')
    match_percentage = models.PositiveSmallIntegerField(default=0)
    missing_skills = models.TextField(blank=True)
    recommended_courses = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Skill gap: {self.user.username} vs {self.job.title}"
