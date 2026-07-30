from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_applications, name='my_applications'),
]
