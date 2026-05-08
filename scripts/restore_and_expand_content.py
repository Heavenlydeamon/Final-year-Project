import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial, CollectibleItem
from content.models import Topic as ContentTopic
from activities.models import ActivityQuestion
from quiz.models import Quiz, MCQQuestion

def seed_full_topic_content(topic_name, academic_data, timeline_data, artifacts_data):
    # 1. Update/Create Main Topic & Study Materials
    topics = Topic.objects.filter(name__icontains=topic_name)
    for topic in topics:
        print(f"--- Seeding Topic: {topic.name} (ID: {topic.id}) ---")
        topic.study_materials.all().delete()
        for i, mod in enumerate(academic_data):
            StudyMaterial.objects.create(
                topic=topic,
                title=mod['title'],
                content_text=mod['content'],
                order=i,
                difficulty='advanced'
            )
            print(f"   Added Study Material: {mod['title']}")
        
        # 2. Seed Collectible Artifacts
        topic.collectibleitem_set.all().delete()
        for art in artifacts_data:
            CollectibleItem.objects.create(
                associated_topic=topic,
                name=art['name'],
                description=art['description'],
                category=art['category'],
                rarity=art['rarity']
            )
            print(f"   Added Collectible: {art['name']}")

    # 3. Update Content Topic (LMS View) & Timeline Activity
    c_topics = ContentTopic.objects.filter(title__icontains=topic_name)
    for ct in c_topics:
        print(f"--- Seeding LMS Content: {ct.title} (ID: {ct.id}) ---")
        
        # Update Sections
        new_sections = []
        for i, mod in enumerate(academic_data):
            new_sections.append({"id": f"mod_{i}", "label": mod['title'], "content": mod['content']})
        ct.sections = new_sections
        ct.save()

        # Seed Timeline Activity
        ActivityQuestion.objects.filter(topic=ct, question_type='sequence').delete()
        ActivityQuestion.objects.create(
            topic=ct,
            question_text=timeline_data['question'],
            question_type='sequence',
            items=timeline_data['items'],
            answer=timeline_data['answer']
        )
        print(f"   Added Timeline Challenge: {timeline_data['question']}")

# --- DATA FOR WESTERN GHATS ---

WESTERN_GHATS_ACADEMIC = [
    {
        'title': 'The Geological Escapement: Breakup of Gondwana',
        'content': """### The Geological Escapement\n\nThe Western Ghats are an ancient "escapement" formed during the rifting of the supercontinent **Gondwana** nearly 150 million years ago. Unlike the Himalayas, which rose from a collision, the Ghats were created as the Indian plate pulled away from Africa.\n\n**The Deccan Traps:** This geological trauma is etched into the Deccan Traps, where massive volcanic eruptions 66 million years ago laid down basalt layers that created the iconic "stepped" profile of the northern range."""
    },
    {
        'title': 'The Hydrological Engine: Orography and the Monsoon',
        'content': """### The Hydrological Engine\n\nThe range serves as a critical **orographic barrier**, intercepting the moisture-laden Southwest Monsoon winds. This forced ascent leads to torrential rains that birth the Godavari, Krishna, and Kaveri rivers.\n\n**The Shola Sponge:** High-altitude **Shola forests** and grasslands act as a "giant sponge," absorbing monsoon water and releasing it slowly during the dry months."""
    },
    {
        'title': 'Socio-Political Landscape: Resistance and Change',
        'content': """### Socio-Political Landscape\n\nHistorically, the Ghats have been a natural fortress, allowing for independent kingdoms. However, the 19th-century colonial shift toward plantation economies fundamentally altered the landscape, disrupting the "sponge effect" and leading to modern environmental challenges."""
    }
]

WESTERN_GHATS_TIMELINE = {
    'question': 'Sequence the Geological and Historical Evolution of the Sahyadri',
    'items': [
        {'id': 1, 'text': 'Supercontinent Gondwana begins to rift (150 Mya)'},
        {'id': 2, 'text': 'Deccan Trap volcanic eruptions create basalt steps (66 Mya)'},
        {'id': 3, 'text': 'Establishment of the Southwest Monsoon cycle (20 Mya)'},
        {'id': 4, 'text': 'Colonial expansion of plantation economies (19th Century)'}
    ],
    'answer': [1, 2, 3, 4]
}

WESTERN_GHATS_ARTIFACTS = [
    {
        'name': 'Neelakurinji Bloom',
        'description': 'The rare flower that blooms once every 12 years, turning the hills blue.',
        'category': 'flora',
        'rarity': 'epic'
    },
    {
        'name': 'Lion-Tailed Macaque',
        'description': 'An endemic primate species found only in the evergreen forests of the Western Ghats.',
        'category': 'fauna',
        'rarity': 'rare'
    }
]

# --- EXECUTION ---

print("Expanding Western Ghats with Full Academic Implementation...")
seed_full_topic_content('Western Ghats', WESTERN_GHATS_ACADEMIC, WESTERN_GHATS_TIMELINE, WESTERN_GHATS_ARTIFACTS)
seed_full_topic_content('Highlands', WESTERN_GHATS_ACADEMIC, WESTERN_GHATS_TIMELINE, WESTERN_GHATS_ARTIFACTS)

print("\nSUCCESS: Western Ghats now features Lore, Timeline Challenges, and Codex Artifacts.")
