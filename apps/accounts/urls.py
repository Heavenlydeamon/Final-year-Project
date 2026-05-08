from django.urls import path
from . import views

urlpatterns = [
    path('teacher/dashboard/', views.teacher_dashboard, name='accounts_teacher_dashboard'),
]
