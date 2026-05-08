import os
import django
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic

names = [t.name for t in Topic.objects.all()]
counts = Counter(names)
duplicates = [name for name, count in counts.items() if count > 1]

for name in duplicates:
    topics = Topic.objects.filter(name=name)
    print(f"Duplicate Topic Name: {name}")
    for t in topics:
        print(f"  ID: {t.id}, Section: {t.section.name if t.section else 'None'}, Materials Count: {t.study_materials.count()}")
