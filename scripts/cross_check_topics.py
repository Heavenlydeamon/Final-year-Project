import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic as MainTopic
from content.models import Topic as ContentTopic

search_names = ['Western Ghats', 'Fort Kochi', 'Padmanabhapuram Palace', 'Kathakali', 'Kalaripayattu', 'Onam', 'Vishu']

for name in search_names:
    print(f"--- {name} ---")
    mt = MainTopic.objects.filter(name__icontains=name)
    for t in mt:
        print(f"MainTopic: ID={t.id}, Name={t.name}, Materials={t.study_materials.count()}")
    
    ct = ContentTopic.objects.filter(title__icontains=name)
    for t in ct:
        print(f"ContentTopic: ID={t.id}, Title={t.title}, SectionsLen={len(t.sections)}")
