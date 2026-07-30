from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    recruiter_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.user.username} -> {self.job.title} ({self.status})"
