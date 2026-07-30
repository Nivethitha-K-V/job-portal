from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .forms import SignUpForm, ProfileForm, EducationForm, SkillForm, ResumeUploadForm, StyledLoginForm
from .models import UserProfile, Education, Skill, Resume, Notification
from applications.models import Application
from jobs.models import Job, SavedJob


def home(request):
    latest_jobs = Job.objects.filter(is_active=True).order_by('-posted_at')[:6]
    return render(request, 'home.html', {'latest_jobs': latest_jobs})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            if user.profile.role == 'recruiter':
                return redirect('recruiter_dashboard')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StyledLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                if hasattr(user, 'profile') and user.profile.role == 'recruiter':
                    return redirect('recruiter_dashboard')
                return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    else:
        form = StyledLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(user=request.user).select_related('job')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]

    status_counts = applications.values('status').annotate(total=Count('status'))

    context = {
        'profile': profile,
        'applications': applications[:5],
        'applications_total': applications.count(),
        'saved_jobs_total': saved_jobs.count(),
        'notifications': notifications,
        'status_counts': {s['status']: s['total'] for s in status_counts},
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    education = Education.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    resume = Resume.objects.filter(user=request.user, is_active=True).first()
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'education': education,
        'skills': skills,
        'resume': resume,
    })


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    education = Education.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    edu_form = EducationForm()
    skill_form = SkillForm()

    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'education': education,
        'skills': skills,
        'edu_form': edu_form,
        'skill_form': skill_form,
    })


@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            messages.success(request, "Education added.")
    return redirect('edit_profile')


@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    edu.delete()
    messages.info(request, "Education entry removed.")
    return redirect('edit_profile')


@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, "Skill added.")
    return redirect('edit_profile')


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    skill.delete()
    messages.info(request, "Skill removed.")
    return redirect('edit_profile')


@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Resume.objects.filter(user=request.user).update(is_active=False)
            resume = form.save(commit=False)
            resume.user = request.user
            resume.is_active = True
            resume.save()
            messages.success(request, "Resume uploaded successfully. Run the analyzer for insights.")
            return redirect('profile')
    else:
        form = ResumeUploadForm()
    return render(request, 'accounts/upload_resume.html', {'form': form})


@login_required
def notifications_view(request):
    notes = Notification.objects.filter(user=request.user)
    notes.filter(is_read=False).update(is_read=True)
    return render(request, 'dashboard/notifications.html', {'notifications': notes})


@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')
