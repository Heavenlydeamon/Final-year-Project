from django.contrib import admin
from django import forms
from .models import Quiz, MCQQuestion, QuizAttempt

class MCQQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = MCQQuestion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [('', 'All sections')]
        if self.instance and hasattr(self.instance, 'quiz') and self.instance.quiz:
            sections = self.instance.quiz.topic.sections
            if isinstance(sections, list):
                for s in sections:
                    if isinstance(s, dict) and 'id' in s and 'label' in s:
                        choices.append((s['id'], s['label']))
        
        # When validation fails, 'quiz' might be in data instead of instance
        if 'quiz' in self.data and self.data['quiz']:
            try:
                quiz = Quiz.objects.get(id=self.data['quiz'])
                sections = quiz.topic.sections
                if isinstance(sections, list):
                    # reset choices to avoid duplicate appends
                    choices = [('', 'All sections')]
                    for s in sections:
                        if isinstance(s, dict) and 'id' in s and 'label' in s:
                            choices.append((s['id'], s['label']))
            except Quiz.DoesNotExist:
                pass
                
        self.fields['section_tag'] = forms.ChoiceField(
            choices=choices,
            required=False,
            help_text="Tag this question to a specific section for targeted mini-quizzes after reading"
        )

class MCQQuestionAdmin(admin.ModelAdmin):
    form = MCQQuestionAdminForm
    list_display = ('question_text', 'quiz', 'section_tag')
    list_filter = ('quiz', 'section_tag')
    
    class Media:
        js = ('js/admin_section_dropdown.js',)

# Register your models here.
admin.site.register(Quiz)
admin.site.register(MCQQuestion, MCQQuestionAdmin)
admin.site.register(QuizAttempt)
