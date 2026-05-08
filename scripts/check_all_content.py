import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial

topics_to_check = ['Fort Kochi', 'Padmanabhapuram Palace', 'Kathakali', 'Kalaripayattu', 'Onam', 'Vishu']

for name in topics_to_check:
    topic = Topic.objects.filter(name__icontains=name).first()
    if topic:
        print(f"--- {topic.name} (ID: {topic.id}) ---")
        for m in topic.study_materials.all().order_by('order'):
            print(f"Material: {m.title}")
            print(f"Content Start: {m.content_text[:200]}")
    else:
        print(f"Topic {name} not found.")
