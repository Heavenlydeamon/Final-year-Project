from django.contrib import admin
from .models import (
    Section, Topic, StudyMaterial, ConceptTag, MaterialView, MaterialAttempt, 
    Question, Choice, QuizAttempt, Enrollment, Institution, Class, UserProfile, 
    StudentMarks, ChallengeAttempt, ChallengeQuestion, ClassJoinRequest,
    AIGeneratedQuiz, AIGeneratedQuestion, AIGeneratedChoice,
    StoryScene, District, Teacher
)

# Register Section
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_general', 'class_obj']
    list_filter = ['is_general']

# Register Topic
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'order', 'is_general']
    list_filter = ['section', 'is_general']

# Register ConceptTag
@admin.register(ConceptTag)
class ConceptTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

# Register StudyMaterial
@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty', 'estimated_time', 'order']
    list_filter = ['difficulty', 'estimated_time', 'topic__section']
    filter_horizontal = ['concept_tags']
    search_fields = ['title', 'content_text']

# Register MaterialView
@admin.register(MaterialView)
class MaterialViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'time_spent', 'completion_status', 'viewed_at']
    list_filter = ['completion_status', 'viewed_at']
    search_fields = ['user__username', 'material__title']

# Register MaterialAttempt
@admin.register(MaterialAttempt)
class MaterialAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'before_score', 'after_score', 'impact_score', 'studied_at']
    list_filter = ['studied_at']
    search_fields = ['user__username', 'material__title']

# Register Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'section', 'topic', 'difficulty']
    list_filter = ['difficulty', 'section']
    search_fields = ['question_text']

# Register Choice
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice_text', 'is_correct']
    list_filter = ['is_correct']

# Register QuizAttempt
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user_identifier', 'section', 'topic', 'score', 'total_questions', 'date_attempted']
    list_filter = ['date_attempted', 'section']
    search_fields = ['user_identifier']

# Register Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'is_active', 'joined_at']
    list_filter = ['is_active']

# Register Institution
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

# Register Class
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'institution', 'teacher', 'is_active']
    list_filter = ['institution', 'is_active']
    search_fields = ['name']

# Register UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'institution']
    list_filter = ['role', 'institution']
    search_fields = ['user__username']

# Register StudentMarks
@admin.register(StudentMarks)
class StudentMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'section', 'topic', 'marks', 'max_marks', 'date_assigned']
    list_filter = ['section', 'date_assigned']

# Register ChallengeAttempt
@admin.register(ChallengeAttempt)
class ChallengeAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge_type', 'score', 'is_completed', 'start_time']
    list_filter = ['challenge_type', 'is_completed']

# Register ChallengeQuestion
@admin.register(ChallengeQuestion)
class ChallengeQuestionAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'question', 'question_order', 'is_correct']
    list_filter = ['is_correct']

# Register ClassJoinRequest
@admin.register(ClassJoinRequest)
class ClassJoinRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'status', 'request_date']
    list_filter = ['status', 'request_date']


# Register AI Generated Quiz Models
@admin.register(AIGeneratedQuiz)
class AIGeneratedQuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'status', 'generated_by', 'generated_at']
    list_filter = ['status', 'content_type', 'generated_at']
    search_fields = ['title', 'description']
    readonly_fields = ['generated_at', 'submitted_at', 'reviewed_at']


@admin.register(AIGeneratedQuestion)
class AIGeneratedQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'difficulty', 'order']
    list_filter = ['difficulty']
    search_fields = ['question_text']


@admin.register(AIGeneratedChoice)
class AIGeneratedChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice_text', 'is_correct', 'order']
    list_filter = ['is_correct']


# Register Story Scene
@admin.register(StoryScene)
class StorySceneAdmin(admin.ModelAdmin):
    list_display = ['topic', 'scene_number', 'text_preview']
    list_filter = ['topic']
    search_fields = ['text']

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'




# Register District
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic']
    search_fields = ['name']

# Register Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_card_number', 'is_approved', 'class_level']
    list_filter = ['is_approved', 'class_level']
    search_fields = ['user__username', 'id_card_number']
    list_editable = ['is_approved'] # Allow quick approval from the list view
