from django.db import models
from django.contrib.auth.models import User
from learning_sessions.models import LowerClassSession
from activities.models import ActivityQuestion

class StudyProgress(models.Model):
    student    = models.ForeignKey(User, on_delete=models.CASCADE)
    topic      = models.ForeignKey('mainapp.Topic', on_delete=models.CASCADE)
    section_id = models.CharField(max_length=50) # matches section slug e.g. "formation-history"
    read_at    = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'topic', 'section_id']
        verbose_name_plural = "Study Progress"

    def __str__(self):
        topic_name = getattr(self.topic, 'name', getattr(self.topic, 'title', 'Unknown'))
        return f"{self.student.username} - {topic_name} - {self.section_id}"
