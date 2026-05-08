from django.db import models
from django.contrib.auth.models import User
from content.models import Topic

HELP_TEXTS = {
    'drag_drop': 'items: {"draggables": [{"id": "id1", "label": "Label", "image": "url"}], "containers": [{"id": "c1", "label": "Label", "icon": "emoji"}]}. answer: {"id1": "c1"}',
    'sequence': 'items: {"items": [{"id": "s1", "label": "Label", "image": "url"}]}. answer: ["s1", "s2"]',
    'tap_match': 'items: {"left_items": [{"id": "l1", "label": "Label"}], "right_items": [{"id": "r1", "label": "Label"}]}. answer: {"l1": "r1"}',
    'image_pick': 'items: {"options": [{"id": "correct", "image": "url", "label": "Label"}]}. answer: "correct"'
}

class ActivityQuestion(models.Model):
    TYPES = [
        ('drag_drop', 'Drag and Drop'),
        ('sequence', 'Put in Order'),
        ('tap_match', 'Match the Pairs'),
        ('image_pick', 'Pick the Image')
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='activities')
    question_type = models.CharField(choices=TYPES, max_length=20)
    question_text = models.TextField()
    
    items = models.JSONField(help_text="Structure varies by type. See examples in the admin.")
    answer = models.JSONField(help_text="Correct solution. Structure varies by type.")
    
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.get_question_type_display()} - {self.order}"
