from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Job, SavedJob
from .forms import JobSearchForm
from applications.models import Application


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    form = JobSearchForm(request.GET or None)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        job_type = form.cleaned_data.get('job_type')
        experience = form.cleaned_data.get('experience')

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(company__icontains=keyword) |
                Q(skills_required__icontains=keyword)
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if experience:
            jobs = jobs.filter(experience=experience)

    saved_ids = set()
    applied_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))
        applied_ids = set(Application.objects.filter(user=request.user).values_list('job_id', flat=True))

    return render(request, 'jobs/jobs.html', {
        'jobs': jobs,
        'form': form,
        'saved_ids': saved_ids,
        'applied_ids': applied_ids,
    })


def job_details(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    already_saved = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(user=request.user, job=job).exists()
        already_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    return render(request, 'jobs/job_details.html', {
        'job': job,
        'already_applied': already_applied,
        'already_saved': already_saved,
    })


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if hasattr(request.user, 'profile') and request.user.profile.role == 'recruiter':
        messages.error(request, "Recruiters cannot apply for jobs.")
        return redirect('job_details', pk=pk)

    application, created = Application.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, f"Applied to {job.title} at {job.company}!")
    else:
        messages.info(request, "You have already applied to this job.")
    return redirect('job_details', pk=pk)


@login_required
def save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, "Job saved.")
    else:
        saved.delete()
        messages.info(request, "Job removed from saved list.")
    return redirect(request.META.get('HTTP_REFERER', 'job_list'))


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/saved_jobs.html', {'saved': saved})


@login_required
def applied_jobs(request):
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/applied_jobs.html', {'applications': applications})
