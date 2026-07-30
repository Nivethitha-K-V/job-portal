from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404

from .models import Company
from .forms import CompanyForm
from jobs.models import Job
from jobs.forms import JobForm
from applications.models import Application
from accounts.models import Notification


def is_recruiter(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'recruiter'


@login_required
@user_passes_test(is_recruiter, login_url='login')
def recruiter_dashboard(request):
    jobs = Job.objects.filter(recruiter=request.user)
    total_applicants = Application.objects.filter(job__recruiter=request.user).count()
    return render(request, 'recruiter/recruiter_dashboard.html', {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'total_applicants': total_applicants,
        'active_jobs': jobs.filter(is_active=True).count(),
    })


@login_required
@user_passes_test(is_recruiter, login_url='login')
def company_profile(request):
    company, _ = Company.objects.get_or_create(
        recruiter=request.user,
        defaults={'company_name': request.user.username}
    )
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated.")
            return redirect('company_profile')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'recruiter/company_profile.html', {'form': form, 'company': company})


@login_required
@user_passes_test(is_recruiter, login_url='login')
def post_job(request):
    company = Company.objects.filter(recruiter=request.user).first()
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            if not job.company and company:
                job.company = company.company_name
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('manage_jobs')
    else:
        initial = {'company': company.company_name} if company else {}
        form = JobForm(initial=initial)
    return render(request, 'recruiter/post_job.html', {'form': form})


@login_required
@user_passes_test(is_recruiter, login_url='login')
def manage_jobs(request):
    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'recruiter/manage_jobs.html', {'jobs': jobs})


@login_required
@user_passes_test(is_recruiter, login_url='login')
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated.")
            return redirect('manage_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'recruiter/post_job.html', {'form': form, 'editing': True})


@login_required
@user_passes_test(is_recruiter, login_url='login')
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    job.delete()
    messages.info(request, "Job deleted.")
    return redirect('manage_jobs')


@login_required
@user_passes_test(is_recruiter, login_url='login')
def toggle_job_status(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    job.is_active = not job.is_active
    job.save()
    return redirect('manage_jobs')


@login_required
@user_passes_test(is_recruiter, login_url='login')
def applicants_list(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    applications = Application.objects.filter(job=job).select_related('user', 'user__profile')
    return render(request, 'recruiter/applicants.html', {'job': job, 'applications': applications})


@login_required
@user_passes_test(is_recruiter, login_url='login')
def update_application_status(request, app_id):
    application = get_object_or_404(Application, pk=app_id, job__recruiter=request.user)
    new_status = request.POST.get('status')
    if new_status in dict(Application.STATUS_CHOICES):
        application.status = new_status
        application.save()
        Notification.objects.create(
            user=application.user,
            message=f"Your application for {application.job.title} is now '{application.get_status_display()}'."
        )
        messages.success(request, "Application status updated.")
    return redirect('applicants_list', pk=application.job.pk)


@login_required
@user_passes_test(is_recruiter, login_url='login')
def download_resume(request, app_id):
    application = get_object_or_404(Application, pk=app_id, job__recruiter=request.user)
    resume = application.user.resumes.filter(is_active=True).first()
    if not resume:
        raise Http404("No resume found for this candidate.")
    return FileResponse(resume.file.open('rb'), as_attachment=True, filename=resume.file.name.split('/')[-1])
