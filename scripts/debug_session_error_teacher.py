import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from django.contrib.auth.models import User
from content.models import Topic, Story
from learning_sessions.models import LowerClassSession

def test_create_session_teacher():
    teacher = User.objects.get(id=25) # A normal teacher
    topic_id = 37
    story_id = 3
    
    print(f"Teacher: {teacher.id} ({teacher.username})")
    print(f"Topic 37 exists: {Topic.objects.filter(id=topic_id).exists()}")
    print(f"Story 3 exists: {Story.objects.filter(id=story_id).exists()}")
    
    try:
        session = LowerClassSession.objects.create(
            teacher=teacher,
            topic_id=topic_id,
            story_id=story_id,
            class_group=None
        )
        print(f"Session created successfully with ID: {session.id}")
    except Exception as e:
        print(f"Error creating session: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_create_session_teacher()
