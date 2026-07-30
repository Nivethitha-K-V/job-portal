from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_details, name='job_details'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/save/', views.save_job, name='save_job'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('applied/', views.applied_jobs, name='applied_jobs'),
]
