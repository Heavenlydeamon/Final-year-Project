from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
]
