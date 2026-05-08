import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial

topics = Topic.objects.filter(name__icontains='Western Ghats')
for topic in topics:
    print(f"Topic: {topic.name} (ID: {topic.id})")
    materials = topic.study_materials.all().order_by('order')
    print(f"Number of materials: {materials.count()}")
    for m in materials:
        print(f"  - {m.title}: {m.content_text[:100]}...")
