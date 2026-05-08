from django.db import models
from django.contrib.auth.models import User
from content.models import Topic

class Class(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_classes_new') # avoid clash
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)  # e.g. "Class 7"
    subject = models.CharField(max_length=100, blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_classes_new', blank=True)
    is_lower_class = models.BooleanField(default=False)
    projection_only = models.BooleanField(default=False)
    projection_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_classes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.grade})"

class ManualStudent(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    class_group = models.ForeignKey('mainapp.Class', on_delete=models.CASCADE, related_name='manual_students')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ManualStudentEvaluation(models.Model):
    RATINGS = [
        ('good', 'Good'),
        ('mixed', 'Mixed'),
        ('struggled', 'Struggled'),
    ]
    student = models.ForeignKey(ManualStudent, on_delete=models.CASCADE, related_name='evaluations')
    class_group = models.ForeignKey('mainapp.Class', on_delete=models.CASCADE, related_name='manual_evaluations')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.CharField(max_length=20, choices=RATINGS)
    remarks = models.TextField(blank=True)
    date_assigned = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_assigned']

    def __str__(self):
        return f"Eval for {self.student.name} - {self.rating} ({self.date_assigned.date()})"

class StudyMaterial(models.Model):
    class_group = models.ForeignKey('mainapp.Class', on_delete=models.CASCADE, related_name='materials')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    content_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.title} Material for {self.class_group.name}"
