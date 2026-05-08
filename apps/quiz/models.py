from django.db import models
from django.contrib.auth.models import User
from content.models import Topic

class Quiz(models.Model):
    SOURCES = [('admin', 'Admin Created'), ('ai', 'AI Generated')]
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(choices=SOURCES, max_length=10)
    assigned_class = models.ForeignKey(
        'classes.Class', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_challenge_eligible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_source_display()})"

class MCQQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=1)  # 'A','B','C','D'
    explanation = models.TextField(blank=True)
    section_tag = models.CharField(max_length=50, blank=True, help_text="Tag this question to a specific section for targeted mini-quizzes after reading")

    def __str__(self):
        return self.question_text[:50]

class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    answers = models.JSONField()  # {"q_id": "chosen_option"}
    attempt_metadata = models.JSONField(default=dict, blank=True, null=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}"
