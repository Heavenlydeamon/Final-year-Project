import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from django.contrib.auth.models import User
from mainapp.models import Section, Topic as MainTopic, StudyMaterial, CollectibleItem
from content.models import Topic as ContentTopic
from quiz.models import Quiz, MCQQuestion
from activities.models import ActivityQuestion

def seed_western_ghats():
    print("Starting Western Ghats Content Seeding...")
    
    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    # 1. Create/Get Section
    section, _ = Section.objects.get_or_create(
        name="Environment", 
        defaults={'description': "The natural heritage and ecological systems of India.", 'is_general': True}
    )

    # 2. Create Topic (Main and Content)
    topic_title = "The Western Ghats"
    topic_desc = "A deep-dive into the geology, hydrology, and biodiversity of the Sahyadri range."
    
    c_topic, created = ContentTopic.objects.get_or_create(
        title=topic_title,
        defaults={
            'category': 'environment',
            'class_level': 'higher',
            'description': topic_desc,
            'is_published': True,
            'created_by': admin_user,
            'thumbnail': 'topics/western_ghats.jpg'
        }
    )
    
    m_topic, _ = MainTopic.objects.get_or_create(
        name=topic_title,
        section=section,
        defaults={'description': topic_desc, 'is_general': True}
    )

    # 3. Add Lore (StudyMaterial and Content Sections)
    lore_modules = [
        {
            'title': 'The Geological Escapement',
            'content': """### The Geological Escapement: Breakup of Gondwana

The Western Ghats are not merely a mountain range; they are an ancient "escapement" formed during the rifting of the supercontinent **Gondwana** nearly 150 million years ago. Unlike the Himalayas, which rose from a collision, the Ghats were created as the Indian plate pulled away from Africa. 

**The Deccan Traps:**
This geological trauma is etched into the **Deccan Traps**, where massive volcanic eruptions 66 million years ago laid down basalt layers that created the iconic "stepped" profile of the northern range. This volcanic activity coincided with the K-Pg extinction event, making the Ghats a window into one of Earth's most volatile periods."""
        },
        {
            'title': 'The Hydrological Engine',
            'content': """### The Hydrological Engine: Orography and the Monsoon

The range serves as a critical **orographic barrier**, intercepting the moisture-laden Southwest Monsoon winds. This forced ascent leads to torrential rains that birth the Godavari, Krishna, and Kaveri rivers. 

**The Shola Sponge:**
This hydrological engine is the lifeblood of South India, supporting over 250 million people. The high-altitude **Shola forests** and grasslands act as a "giant sponge," absorbing monsoon water and releasing it slowly during the dry months, ensuring perennial river flow even when the rains stop."""
        },
        {
            'title': 'Socio-Political Landscape',
            'content': """### The Socio-Political Landscape: Resistance and Change

Socio-politically, the Ghats have historically been a natural fortress, allowing for the rise of independent kingdoms and specialized guerilla warfare. 

**The Plantation Shift:**
However, the 19th-century colonial shift toward plantation economies (tea, coffee, and rubber) fundamentally altered the landscape. Replacing ancient evergreen forests with monocultures disrupted the "sponge effect," leading to the modern cycle of floods and droughts—a heritage of environmental management that students must now navigate."""
        }
    ]

    # Update ContentTopic sections
    c_topic.sections = [
        {"id": f"wg_{i}", "label": mod['title'], "content": mod['content']} 
        for i, mod in enumerate(lore_modules)
    ]
    c_topic.save()

    # Update StudyMaterials
    StudyMaterial.objects.filter(topic=m_topic).delete()
    for i, mod in enumerate(lore_modules):
        StudyMaterial.objects.create(
            topic=m_topic,
            title=mod['title'],
            content_text=mod['content'],
            order=i,
            difficulty='advanced',
            estimated_time='long'
        )

    # 4. Timeline Challenge (ActivityQuestion)
    timeline_items = [
        {"id": 1, "text": "150 Million Years Ago: Breakup of Gondwana creates the western escapement."},
        {"id": 2, "text": "66 Million Years Ago: Massive volcanic eruptions create the Deccan Traps."},
        {"id": 3, "text": "1882: The Indian Forest Act centralizes control over timber resources."},
        {"id": 4, "text": "2012: UNESCO designates 39 sites in the Western Ghats as World Heritage sites."}
    ]
    
    # We'll store them shuffled but define the answer as the correct order of IDs
    ActivityQuestion.objects.get_or_create(
        topic=c_topic,
        question_type='sequence',
        defaults={
            'question_text': "Sort these key events in the history of the Western Ghats into their correct chronological order.",
            'items': timeline_items,
            'answer': [1, 2, 3, 4],
            'explanation': "The Ghats formed via continental rifting (150mya), followed by volcanism (66mya), colonial legislation (1882), and finally global conservation recognition (2012)."
        }
    )

    # 5. Scenario-Based Quizzes
    quiz, _ = Quiz.objects.get_or_create(
        title="Western Ghats: Systems & Ethics",
        topic=c_topic,
        defaults={'created_by': admin_user, 'source': 'admin', 'is_challenge_eligible': True}
    )

    scenarios = [
        {
            'question_text': "Scenario: The Silent Valley Dilemma. A hydroelectric project promises power to thousands but requires flooding a pristine rainforest home to the Lion-tailed Macaque. What is the most sustainable approach?",
            'option_a': "Deny the dam and implement decentralized solar micro-grids with eco-tourism revenue.",
            'option_b': "Build a 'Run-of-the-River' dam with fish ladders and replant trees elsewhere.",
            'option_c': "Proceed with the dam to ensure rapid industrial growth and local jobs.",
            'option_d': "None of the above.",
            'correct_option': 'A',
            'explanation': "Option A preserves the 'hydrological sponge' and prevents extinction. Option B is flawed because primary forests can't be 'replanted' easily. Option C ignores ecological tipping points."
        },
        {
            'question_text': "Scenario: The Invasive Thirst. Colonial-era Eucalyptus plantations are drying up Shola grasslands, causing downstream springs to vanish. How do you resolve this?",
            'option_a': "Systematically uproot invasives and use active restoration for native Shola-grassland mosaics.",
            'option_b': "Leave the trees but build concrete check-dams to catch the remaining water.",
            'option_c': "Plant more Eucalyptus to create a 'green wall' against climate change.",
            'option_d': "None of the above.",
            'correct_option': 'A',
            'explanation': "Option A restores the natural water-holding capacity. Check-dams (B) are temporary band-aids. Planting more (C) would accelerate groundwater depletion."
        }
    ]

    for s in scenarios:
        MCQQuestion.objects.get_or_create(
            quiz=quiz,
            question_text=s['question_text'],
            defaults={
                'option_a': s['option_a'],
                'option_b': s['option_b'],
                'option_c': s['option_c'],
                'option_d': s['option_d'],
                'correct_option': s['correct_option'],
                'explanation': s['explanation']
            }
        )

    # 6. Codex Artifacts (CollectibleItem)
    collectibles = [
        {
            'name': 'The Neelakurinji Bloom',
            'category': 'flora',
            'description': "A digital herbarium entry for Strobilanthes kunthiana, which blooms once every 12 years, turning the hills blue.",
            'rarity': 'rare',
            'xp_value': 150
        },
        {
            'name': 'The Malabar Gliding Frog',
            'category': 'fauna',
            'description': "A rare specimen record of Rhacophorus malabaricus, known for using webbed feet to parachute between canopies.",
            'rarity': 'epic',
            'xp_value': 300
        }
    ]

    for c in collectibles:
        CollectibleItem.objects.get_or_create(
            name=c['name'],
            defaults={
                'category': c['category'],
                'description': c['description'],
                'rarity': c['rarity'],
                'xp_value': c['xp_value'],
                'associated_topic': m_topic
            }
        )

    print("Western Ghats Seeding Complete!")

if __name__ == "__main__":
    seed_western_ghats()
