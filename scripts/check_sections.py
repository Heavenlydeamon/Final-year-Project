import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, Section

topics = Topic.objects.filter(name__icontains='Western Ghats')
for topic in topics:
    print(f"ID: {topic.id}, Name: {topic.name}, Section: {topic.section.name if topic.section else 'None'}")
