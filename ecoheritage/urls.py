from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import (
    home, profile, class_view,
    register, teacher_register, student_register, login_view, logout_view, dashboard,
    forgot_password,
    environment, environment_topics, environment_quiz,
    topic_study, topic_quiz, quiz_result, mark_general_topic_studied,
    heritage, heritage_topics, heritage_quiz,
    cultural, cultural_topics, cultural_quiz,
    folklore,
    leaderboard,
    # Teacher dashboard views
    teacher_dashboard, teacher_manage_sections, teacher_manage_topics,
    teacher_manage_study_materials, teacher_add_quiz_question,
    teacher_view_students, teacher_view_student_performance, teacher_assign_marks, teacher_topic_analytics,
    teacher_manage_classes, teacher_add_student_to_class, teacher_class_detail, teacher_class_creation_wizard,
    # Student dashboard views
    student_dashboard, student_view_topics, student_study_topic,
    student_mark_topic_studied,
    student_take_quiz, student_quiz_result, student_view_marks, student_performance,
    study_material_detail,
    # Student profile views
    student_profile, edit_student_profile,
    # NEW: Student Codex and Activities
    student_codex, activity_timeline,
    # AJAX Mastery
    award_xp_ajax, mark_mastery_complete, mark_activity_complete_ajax,
    student_mastery_arena,
    # League notification views
    dismiss_league_notification,
    # Challenge mode views
    challenge_mode, start_challenge, challenge_question, submit_challenge_answer, challenge_results,
    # AJAX views
    get_topics_by_section, get_study_materials,
    # Class join request views
    student_join_class, student_my_requests, teacher_view_join_requests, teacher_process_join_request,
    # Admin dashboard views
    admin_dashboard, admin_manage_institutions, admin_manage_teachers, admin_manage_students,
    admin_manage_classes, admin_manage_general_content, admin_analytics, admin_view_join_requests,
    admin_system_settings,
    # Heritage Admin views
    admin_manage_stories, admin_create_story, admin_edit_story,
    admin_add_story_panel, admin_delete_story_panel, admin_manage_activities,
    # AI Quiz Generator views - Teacher only (admin AI quiz removed)
    teacher_ai_quiz_generator, teacher_generate_quiz, teacher_generate_quiz_from_material, teacher_preview_quiz,
    teacher_save_quiz, teacher_update_question, teacher_delete_quiz, teacher_my_quizzes,
    teacher_manual_quiz, teacher_create_manual_quiz, teacher_quiz_approval,
    process_teacher_quiz_approval, convert_quiz_to_questions, get_study_materials_ajax, get_topics_ajax, check_model_status,
    preload_model, promote_to_daily_challenge,
    remove_sample_quiz_data, remove_sample_quiz_for_topic,
    delete_ai_quiz_for_topic,
    teacher_suggest_topics_api, teacher_generate_lesson_api,
)

from mainapp.views.base import topic_leaderboard, teacher_publish_valuation, teacher_class_topic_leaderboard



from mainapp.views.activity_quiz import match_quiz_view
from mainapp.views.learning_modes import story_mode, kerala_map_view, district_view
from mainapp.views.knowledge_graph import knowledge_graph_view, knowledge_graph_data
from mainapp.views.story_views import (
    story_list, story_detail, next_story_node, story_companion_api
)
from learning_sessions import views as session_views
from gamification.views import find_challenge_opponent, complete_challenge_session, challenge_arena
from mainapp.views.daily_challenges import daily_challenge_view, submit_daily_challenge


urlpatterns = [
    # Admin Dashboard URLs - must come BEFORE admin.site.urls
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/institutions/', admin_manage_institutions, name='admin_manage_institutions'),
    path('admin/teachers/', admin_manage_teachers, name='admin_manage_teachers'),
    path('admin/students/', admin_manage_students, name='admin_manage_students'),
    path('admin/classes/', admin_manage_classes, name='admin_manage_classes'),
    path('admin/general-content/', admin_manage_general_content, name='admin_manage_general_content'),
    path('admin/analytics/', admin_analytics, name='admin_analytics'),
    path('admin/join-requests/', admin_view_join_requests, name='admin_view_join_requests'),
    path('admin/settings/', admin_system_settings, name='admin_system_settings'),
    
    # Custom Heritage Admin
    path('admin/heritage/stories/', admin_manage_stories, name='admin_manage_stories'),
    path('admin/heritage/stories/create/', admin_create_story, name='admin_create_story'),
    path('admin/heritage/stories/<int:story_id>/edit/', admin_edit_story, name='admin_edit_story'),
    path('admin/heritage/stories/<int:story_id>/panels/add/', admin_add_story_panel, name='admin_add_story_panel'),
    path('admin/heritage/stories/panels/<int:panel_id>/delete/', admin_delete_story_panel, name='admin_delete_story_panel'),
    path('admin/heritage/activities/', admin_manage_activities, name='admin_manage_activities'),
    
    path('admin/', admin.site.urls),

    # NEW RESTRUCTURED ROUTES
    path('auth/', include('accounts.urls')),
    path('content/', include('content.urls')),
    path('quiz/', include('quiz.urls')),
    path('teacher/lower/session/', include('learning_sessions.urls')),
    path('teacher/lower/analytics/', session_views.lower_class_analytics, name='lower_class_analytics'),
    path('teacher/lower/analytics/export/', session_views.export_lower_class_data, name='export_lower_class_data'),
    path('student/progress/', include('analytics.urls')),

    path('', home, name='home'),
    
    # Profile and Class views
    path('profile/', profile, name='profile'),
    path('class/', class_view, name='class_view'),

    path('register/', register, name='register'),
    path('register/teacher/', teacher_register, name='teacher_register'),
    path('register/student/', student_register, name='student_register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot_password'),

    path('dashboard/', dashboard, name='dashboard'),

    path('environment/', environment, name='environment'),
    path('environment/topics/', environment_topics, name='environment_topics'),
    
    # Quizzes
    path('quiz/environment/', environment_quiz, name='environment_quiz'),
    path('quiz/heritage/', heritage_quiz, name='heritage_quiz'),
    path('quiz/cultural/', cultural_quiz, name='cultural_quiz'),
    path('topic/<int:topic_id>/quiz/', topic_quiz, name='topic_quiz'),
    path('topic/<int:topic_id>/match-quiz/', match_quiz_view, name='match_quiz'),
    path('quiz-result/', quiz_result, name='quiz_result'),

    path('topic/<int:topic_id>/study/', topic_study, name='topic_study'),
    path('topic/<int:topic_id>/mark-studied/', mark_general_topic_studied, name='mark_general_topic_studied'),

    path('heritage/', heritage, name='heritage'),
    path('heritage/topics/', heritage_topics, name='heritage_topics'),

    path('cultural/', cultural, name='cultural'),
    path('cultural/topics/', cultural_topics, name='cultural_topics'),

    path('folklore/', folklore, name='folklore'),

    path('leaderboard/', leaderboard, name='leaderboard'),
    path('leaderboard/topic/<int:topic_id>/', topic_leaderboard, name='topic_leaderboard'),
    
    # Teacher Dashboard URLs
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/sections/', teacher_manage_sections, name='teacher_manage_sections'),
    path('teacher/topics/', teacher_manage_topics, name='teacher_manage_topics'),
    path('teacher/topics/<int:section_id>/', teacher_manage_topics, name='teacher_manage_topics_by_section'),
    path('teacher/study-materials/', teacher_manage_study_materials, name='teacher_manage_study_materials'),
    path('teacher/study-materials/<int:topic_id>/', teacher_manage_study_materials, name='teacher_manage_study_materials_topic'),
    path('teacher/add-quiz/', teacher_add_quiz_question, name='teacher_add_quiz_question'),
    path('teacher/students/', teacher_view_students, name='teacher_view_students'),
    path('teacher/student/<int:student_id>/performance/', teacher_view_student_performance, name='teacher_view_student_performance'),
    path('teacher/class/<int:class_id>/student/<int:student_id>/performance/', teacher_view_student_performance, name='teacher_view_student_performance_class'),
    path('teacher/class/<int:class_id>/topic/<int:topic_id>/analytics/', teacher_topic_analytics, name='teacher_topic_analytics'),
    path('teacher/class/<int:class_id>/topic/<int:topic_id>/publish/', teacher_publish_valuation, name='teacher_publish_valuation'),
    path('teacher/class/<int:class_id>/topic/<int:topic_id>/leaderboard/', teacher_class_topic_leaderboard, name='teacher_class_topic_leaderboard'),
    path('teacher/classes/', teacher_manage_classes, name='teacher_manage_classes'),
    path('teacher/class/<int:class_id>/', teacher_class_detail, name='teacher_class_detail'),
    path('teacher/create-wizard/', teacher_class_creation_wizard, name='teacher_class_creation_wizard'),
    path('teacher/add-student/', teacher_add_student_to_class, name='teacher_add_student_to_class'),
    path('teacher/class/<int:class_id>/add-student/', teacher_add_student_to_class, name='teacher_add_students'),

    
    # Student Dashboard URLs
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/profile/', student_profile, name='student_profile'),
    path('student/profile/edit/', edit_student_profile, name='edit_student_profile'),
    path('student/topics/', student_view_topics, name='student_view_topics'),
    path('student/topic/<int:topic_id>/study/', student_study_topic, name='student_study_topic'),
    path('student/material/<int:material_id>/', study_material_detail, name='study_material_detail'),
    path('student/topic/<int:topic_id>/mark-studied/', student_mark_topic_studied, name='student_mark_topic_studied'),
    path('student/topic/<int:topic_id>/quiz/', student_take_quiz, name='student_take_quiz'),
    path('student/quiz/result/', student_quiz_result, name='student_quiz_result'),
    path('student/marks/', student_view_marks, name='student_view_marks'),
    path('student/performance/', student_performance, name='student_performance'),
    path('student/codex/', student_codex, name='student_codex'),
    path('student/activity/timeline/<int:topic_id>/', activity_timeline, name='activity_timeline'),
    # AJAX Mastery
    path('ajax/award-xp/', award_xp_ajax, name='award_xp_ajax'),
    path('ajax/mark-mastery/<int:topic_id>/', mark_mastery_complete, name='mark_mastery_complete'),
    path('ajax/mark-activity/<int:topic_id>/', mark_activity_complete_ajax, name='mark_activity_complete_ajax'),
    path('student/mastery-arena/<int:topic_id>/', student_mastery_arena, name='student_mastery_arena'),

    path('student/league/dismiss-notification/<int:notification_id>/', dismiss_league_notification, name='dismiss_league_notification'),
    
    # Challenge Mode URLs
    path('student/challenge/', challenge_mode, name='challenge_mode'),
    path('student/challenge/find-opponent/', find_challenge_opponent, name='find_challenge_opponent'),
    path('student/challenge/arena/<int:session_id>/', challenge_arena, name='challenge_arena'),
    path('student/challenge/pvp-complete/<int:session_id>/', complete_challenge_session, name='complete_challenge_session'),
    path('student/challenge/start/', start_challenge, name='start_challenge'),
    path('student/challenge/question/', challenge_question, name='challenge_question'),
    path('student/challenge/submit/', submit_challenge_answer, name='submit_challenge_answer'),
    path('student/challenge/results/', challenge_results, name='challenge_results'),
    
    # AJAX URLs
    path('ajax/topics-by-section/', get_topics_by_section, name='get_topics_by_section'),
    path('ajax/study-materials/', get_study_materials, name='get_study_materials'),
    
    # Class Join Request URLs
    path('student/join-class/', student_join_class, name='student_join_class'),
    path('student/my-requests/', student_my_requests, name='student_my_requests'),
    path('teacher/join-requests/', teacher_view_join_requests, name='teacher_view_join_requests'),
    path('teacher/join-requests/<int:request_id>/', teacher_process_join_request, name='teacher_process_join_request'),
    
    # AI Quiz Generator URLs - Teacher only (NO admin quiz approval)
    path('teacher/ai-quiz/', teacher_ai_quiz_generator, name='teacher_ai_quiz_generator'),
    path('teacher/ai-quiz/generate/', teacher_generate_quiz, name='teacher_generate_quiz'),
    path('teacher/ai-quiz/generate-from-material/<int:material_id>/', teacher_generate_quiz_from_material, name='teacher_generate_quiz_from_material'),
    path('teacher/ai-quiz/preview/<int:quiz_id>/', teacher_preview_quiz, name='teacher_preview_quiz'),
    path('teacher/ai-quiz/save/<int:quiz_id>/', teacher_save_quiz, name='teacher_save_quiz'),
    path('teacher/ai-quiz/update-question/<int:question_id>/', teacher_update_question, name='teacher_update_question'),
    path('teacher/ai-quiz/delete/<int:quiz_id>/', teacher_delete_quiz, name='teacher_delete_quiz'),
    path('teacher/ai-quiz/my-quizzes/', teacher_my_quizzes, name='teacher_my_quizzes'),
    path('teacher/ai-quiz/manual/', teacher_manual_quiz, name='teacher_manual_quiz'),
    path('teacher/ai-quiz/manual/create/', teacher_create_manual_quiz, name='teacher_create_manual_quiz'),
    path('teacher/ai-quiz/approval/', teacher_quiz_approval, name='teacher_quiz_approval'),
    path('teacher/ai-quiz/approval/<int:quiz_id>/', process_teacher_quiz_approval, name='process_teacher_quiz_approval'),
    path('teacher/ai-quiz/convert/<int:quiz_id>/', convert_quiz_to_questions, name='convert_quiz_to_questions'),
    path('teacher/ai-quiz/promote-challenge/<int:question_id>/', promote_to_daily_challenge, name='promote_to_daily_challenge'),
    
    # AJAX URLs for AI Quiz
    path('ajax/ai-quiz/materials/', get_study_materials_ajax, name='get_study_materials_ajax'),
    path('ajax/ai-quiz/topics/', get_topics_ajax, name='get_topics_ajax'),
    path('ajax/ai-quiz/model-status/', check_model_status, name='check_model_status'),
    path('ajax/ai-quiz/preload-model/', preload_model, name='preload_model'),
    
    # Teacher AI Assistance Helpers
    path('ajax/teacher/suggest-topics/', teacher_suggest_topics_api, name='teacher_suggest_topics_api'),
    path('ajax/teacher/generate-lesson/', teacher_generate_lesson_api, name='teacher_generate_lesson_api'),
    
    # Quiz Data Management URLs
    path('admin/remove-quiz-data/', remove_sample_quiz_data, name='remove_sample_quiz_data'),
    path('admin/topic/<int:topic_id>/remove-quiz/', remove_sample_quiz_for_topic, name='remove_sample_quiz_for_topic'),
    path('admin/topic/<int:topic_id>/delete-ai-quiz/', delete_ai_quiz_for_topic, name='delete_ai_quiz_for_topic'),
    


    # Narrative Story Companion URLs
    path('stories/', story_list, name='story_list'),
    path('story/<int:story_id>/', story_detail, name='story_detail'),
    path('story/<int:story_id>/next/', next_story_node, name='next_story_node'),
    path('api/story-companion/', story_companion_api, name='story_companion_api'),

    # Interactive Learning Modes
    path('modes/story/<int:topic_id>/', story_mode, name='story_mode'),
    
    # Knowledge Graph
    path('knowledge-graph/', knowledge_graph_view, name='knowledge_graph'),
    path('api/knowledge-graph-data/', knowledge_graph_data, name='knowledge_graph_data'),
    
    # Interactive Map
    path('map/', kerala_map_view, name='kerala_map'),
    path('district/<int:id>/', district_view, name='district_view'),

    # Daily Topic Challenge
    path('topic/<int:topic_id>/daily-challenge/', daily_challenge_view, name='daily_challenge'),
    path('daily-challenge/<int:challenge_id>/submit/', submit_daily_challenge, name='submit_daily_challenge'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

