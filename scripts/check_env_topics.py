import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Section, Topic

env_section = Section.objects.filter(name='Environment').first()
if env_section:
    topics = Topic.objects.filter(section=env_section).order_by('order')
    for t in topics:
        print(f"ID: {t.id}, Name: {t.name}, Order: {t.order}, Materials: {t.study_materials.count()}")
