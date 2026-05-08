from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('generate/', views.generate_quiz_view, name='generate_quiz'),
    path('<int:quiz_id>/take/', views.take_quiz_view, name='take_quiz'),
    path('<int:quiz_id>/results/', views.quiz_results_view, name='quiz_results'),
    path('section-check/', views.section_check_api, name='section_check_api'),
    path('section/<int:topic_id>/<str:section_id>/', views.mini_quiz_view, name='mini_quiz_view'),
    path('admin-sections/', views.admin_sections_api, name='admin_sections_api'),
]
