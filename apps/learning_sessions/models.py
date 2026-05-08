from django.db import models
from django.contrib.auth.models import User
from content.models import Topic, Story
from activities.models import ActivityQuestion
from mainapp.models import Topic as MainTopic, Class
# Note: Using mainapp.Class to match teacher dashboard

class LowerClassSession(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, blank=True)
    class_group = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    current_panel_index = models.IntegerField(default=0)
    # Track which panel is currently displayed
    
    content_sequence = models.JSONField(default=list)
    # [{"type":"panel","id":1},{"type":"activity","id":5}]
    # Built from story panels + linked activities
    
    stars_earned = models.IntegerField(default=0)
    # Calculated at session end based on responses
    
    notes = models.TextField(blank=True)
    # Teacher's post-session notes

    def __str__(self):
        return f"Session: {self.topic.title} by {self.teacher.username} on {self.started_at.date()}"


class SessionResponse(models.Model):
    LEVELS = [
        ('good', 'Most Got It'),
        ('mixed', 'Mixed Response'),
        ('struggled', 'Most Struggled')
    ]
    
    session = models.ForeignKey(LowerClassSession, on_delete=models.CASCADE, related_name='session_responses')
    activity_question = models.ForeignKey(ActivityQuestion, on_delete=models.CASCADE)
    response_level = models.CharField(choices=LEVELS, max_length=10)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.id} - {self.activity_question.id} - {self.response_level}"
