from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('company/', views.company_profile, name='company_profile'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:pk>/toggle/', views.toggle_job_status, name='toggle_job_status'),
    path('jobs/<int:pk>/applicants/', views.applicants_list, name='applicants_list'),
    path('applications/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
    path('applications/<int:app_id>/resume/', views.download_resume, name='download_resume'),
]
