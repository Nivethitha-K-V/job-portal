from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Application


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/applied_jobs.html', {'applications': applications})
