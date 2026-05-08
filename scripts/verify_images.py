import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial

t = Topic.objects.get(id=138)
print(f"Topic: {t.name}, Image: {t.image_url}")
for m in t.study_materials.all():
    print(f"  Material: {m.title}, ImageField: {m.image}")
