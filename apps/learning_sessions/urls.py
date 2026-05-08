from django.urls import path
from . import views

app_name = 'learning_sessions'

urlpatterns = [
    path('history/', views.session_history, name='session_history'),
    path('start/<int:topic_id>/', views.start_session, name='start_session'),
    # Use explicit path segments to avoid ambiguity between story_id and class_id
    path('start/<int:topic_id>/story/<int:story_id>/', views.start_session, name='start_session_with_story'),
    path('start/<int:topic_id>/class/<int:class_id>/', views.start_session, name='start_session_with_class'),
    path('start/<int:topic_id>/story/<int:story_id>/class/<int:class_id>/', views.start_session, name='start_session_with_story_and_class'),
    path('<int:session_id>/projection/', views.projection_view, name='projection_view'),
    path('<int:session_id>/next/', views.next_item, name='next_item'),
    path('<int:session_id>/response/', views.record_response, name='record_response'),
    path('<int:session_id>/end/', views.end_session, name='end_session'),
    path('<int:session_id>/evaluate/', views.submit_evaluations, name='submit_evaluations'),
    path('analytics/', views.lower_class_analytics, name='lower_class_analytics'),
    path('analytics/export/', views.export_lower_class_data, name='export_lower_class_data'),
]
