from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Topic(models.Model):
    LEVELS = [('lower', 'Lower'), ('higher', 'Higher'), ('both', 'Both')]
    CATEGORIES = [
        ('artforms', 'Artforms'),
        ('wildlife', 'Wildlife'),
        ('festivals', 'Festivals'),
        ('environment', 'Environment'),
        ('heritage', 'Heritage'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(choices=CATEGORIES, max_length=20)
    class_level = models.CharField(
        choices=LEVELS, 
        max_length=10,
        help_text=("Lower: shown in teacher projection sessions. "
                  "Higher: shown in student academic study view. "
                  "Both: available in both contexts.")
    )
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='topics/')
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sections = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title

class Story(models.Model):
    STORY_TYPES = [
        ('admin_original', 'Admin Original'),
        ('teacher_created', 'Teacher Created')
    ]
    STATUS = [('draft', 'Draft'), ('published', 'Published')]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=200)
    # e.g., "Ravi Sees His First Theyyam"
    
    tagline = models.CharField(max_length=300, blank=True)
    # e.g., "A magical night in Kannur where gods come to dance"
    
    cover_image = models.ImageField(upload_to='stories/covers/')
    
    character_name = models.CharField(max_length=50)
    character_age = models.IntegerField()
    character_avatar = models.CharField(max_length=10)  # emoji
    character_description = models.CharField(max_length=200)
    # e.g., "Ravi lives in Kannur with his grandparents"
    
    story_type = models.CharField(choices=STORY_TYPES, max_length=20, default='admin_original')
    status = models.CharField(choices=STATUS, max_length=10, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_stories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.title


class StoryPanel(models.Model):
    PANEL_TYPES = [
        ('narration', 'Narration'),    # Main story text
        ('question', 'Question'),       # Pause for discussion
        ('fact', 'Fun Fact'),          # Kerala-specific fact
        ('activity', 'Activity Cue')    # Links to ActivityQuestion
    ]
    
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='panels', null=True)
    order = models.PositiveIntegerField()
    panel_type = models.CharField(choices=PANEL_TYPES, max_length=20, default='narration', null=True)
    
    title = models.CharField(max_length=100, null=True)
    # e.g., "The special night", "Getting ready"
    
    image = models.ImageField(upload_to='stories/panels/', null=True)
    
    text = models.TextField(validators=[MaxLengthValidator(250)], null=True)
    # Max 250 chars = ~2 sentences for Class 1-4
    
    audio_file = models.FileField(upload_to='stories/audio/', blank=True)
    # Optional Malayalam TTS or recorded narration
    
    linked_activity = models.ForeignKey(
        'activities.ActivityQuestion',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    # Only used when panel_type = 'activity'
    
    class Meta:
        ordering = ['order']
        unique_together = ['story', 'order']

    def __str__(self):
        return f"{self.story.title} - Panel {self.order} ({self.panel_type})"



