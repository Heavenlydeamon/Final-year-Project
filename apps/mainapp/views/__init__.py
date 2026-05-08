# Import all views from base module to maintain backward compatibility
from .base import *

# Import AI quiz generator views - Teacher only (no admin quiz)
from .ai_quiz_generator_views import (
    teacher_ai_quiz_generator,
    teacher_generate_quiz,
    teacher_generate_quiz_from_material,
    teacher_preview_quiz,
    teacher_save_quiz,
    teacher_update_question,
    teacher_delete_quiz,
    teacher_my_quizzes,
    teacher_manual_quiz,
    teacher_create_manual_quiz,
    teacher_quiz_approval,
    process_teacher_quiz_approval,
    convert_quiz_to_questions,
    get_study_materials_ajax,
    get_topics_ajax,
    check_model_status,
    preload_model,
    promote_to_daily_challenge,
)

# Import teacher AI assistance views
from .teacher_ai_views import (
    teacher_suggest_topics_api,
    teacher_generate_lesson_api,
)

# Heritage Admin views
from .admin_heritage import (
    admin_manage_stories, admin_create_story, admin_edit_story,
    admin_add_story_panel, admin_delete_story_panel, admin_manage_activities,
)

# Note: Admin quiz review views have been removed

# Import from revisions and updates if needed
# from .revisions import *
# from .updates import *
