from django.db import models
from django.contrib.auth.models import User
from content.models import Topic
from quiz.models import Quiz

class Badge(models.Model):
    CATEGORIES = [('artform', 'Artform'), ('wildlife', 'Wildlife'),
                  ('festival', 'Festival'), ('environment', 'Environment')]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    icon = models.ImageField(upload_to='badges/')
    category = models.CharField(choices=CATEGORIES, max_length=20)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL,
        null=True, blank=True  # optional — badge tied to a topic
    )

    def __str__(self):
        return self.name

class ChallengeSession(models.Model):
    STATUS = [('waiting', 'Waiting'), ('active', 'Active'), ('completed', 'Completed')]
    player_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_as_p1')
    player_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_as_p2', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=10, default='waiting')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_challenges')
    
    # Ghost Matchmaking Fields
    is_ghost = models.BooleanField(default=False)
    ghost_accuracy = models.FloatField(default=0.7) # 70% accuracy by default
    ghost_name = models.CharField(max_length=50, default="EcoBot")
    
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challenge {self.id}: {self.player_one.username} vs {self.player_two.username if self.player_two else '?'}"
