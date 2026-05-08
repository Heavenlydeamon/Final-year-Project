import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial

all_materials = StudyMaterial.objects.filter(content_text__contains='*')
for m in all_materials:
    print(f"Topic: {m.topic.name} (ID: {m.topic.id}), Material: {m.title}")
