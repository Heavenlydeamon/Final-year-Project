import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from content.models import Topic as ContentTopic

# Look at Western Ghats (Highlands)
topic = ContentTopic.objects.filter(title__icontains='Western Ghats').first()
if topic:
    print(f"Title: {topic.title}")
    print(json.dumps(topic.sections, indent=2))
