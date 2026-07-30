from django.urls import path
from . import views

urlpatterns = [
    path('resume-analyzer/', views.resume_analyzer, name='resume_analyzer'),
    path('skill-gap/', views.skill_gap_analyzer, name='skill_gap_analyzer'),
]
