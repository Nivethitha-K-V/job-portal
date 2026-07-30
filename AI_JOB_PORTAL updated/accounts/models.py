from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')

    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    experience_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name or self.user.username

    @property
    def is_complete(self):
        required = [self.full_name, self.mobile, self.state, self.city]
        return all(required)


class Education(models.Model):
    QUALIFICATION_CHOICES = (
        ('10th', '10th'),
        ('12th', '12th'),
        ('diploma', 'Diploma'),
        ('ug', 'Undergraduate'),
        ('pg', 'Postgraduate'),
        ('phd', 'PhD'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education_set')
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    college = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=150, blank=True)
    branch = models.CharField(max_length=150, blank=True)
    passing_year = models.PositiveIntegerField(blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.qualification} - {self.college}"


class Skill(models.Model):
    SKILL_TYPE_CHOICES = (
        ('technical', 'Technical'),
        ('soft', 'Soft Skill'),
        ('language', 'Language'),
        ('certification', 'Certification'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_set')
    name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPE_CHOICES, default='technical')
    proficiency = models.PositiveSmallIntegerField(default=50)  # 0-100

    def __str__(self):
        return f"{self.name} ({self.get_skill_type_display()})"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resume_score = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume - {self.user.username} ({self.uploaded_at.date()})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:40]}"
