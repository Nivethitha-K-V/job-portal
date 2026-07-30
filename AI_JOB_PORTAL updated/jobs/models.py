from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    )
    EXPERIENCE_CHOICES = (
        ('fresher', 'Fresher'),
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5+', '5+ years'),
    )

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.CharField(
        max_length=500,
        help_text="Comma-separated, e.g. Python, Django, SQL"
    )
    location = models.CharField(max_length=150)
    salary = models.CharField(max_length=100, blank=True, help_text="e.g. 6-8 LPA")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.title} @ {self.company}"

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
