from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('education/add/', views.add_education, name='add_education'),
    path('education/<int:pk>/delete/', views.delete_education, name='delete_education'),

    path('skill/add/', views.add_skill, name='add_skill'),
    path('skill/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    path('resume/upload/', views.upload_resume, name='upload_resume'),

    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
]
