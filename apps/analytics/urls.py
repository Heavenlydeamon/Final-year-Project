from django.urls import path
from . import views

urlpatterns = [
    path('mark/', views.mark_section_read, name='mark_section_read'),
]
