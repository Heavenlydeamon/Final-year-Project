import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial, Section
from content.models import Topic as ContentTopic

def update_topic_content(names, description, modules, image_rel_path):
    # Update mainapp Topics
    for name in names:
        topics = Topic.objects.filter(name__icontains=name)
        for topic in topics:
            print(f"Updating mainapp Topic: {topic.name} (ID: {topic.id})")
            topic.description = description
            topic.image_url = f"/media/study_materials/images/{image_rel_path}"
            topic.save()
            
            # Clear old materials
            topic.study_materials.all().delete()
            
            # Add new materials
            for i, mod in enumerate(modules):
                StudyMaterial.objects.create(
                    topic=topic,
                    title=mod['title'],
                    content_text=mod['content'],
                    order=i,
                    difficulty='intermediate',
                    estimated_time='medium',
                    image=f"study_materials/images/{image_rel_path}" if i == 0 else None
                )

    # Update content.Topic (if exists)
    for name in names:
        c_topics = ContentTopic.objects.filter(title__icontains=name)
        for ct in c_topics:
            print(f"Updating content Topic: {ct.title} (ID: {ct.id})")
            ct.description = description
            new_sections = []
            for i, mod in enumerate(modules):
                new_sections.append({
                    "id": f"mod_{i}",
                    "label": mod['title'],
                    "content": mod['content']
                })
            ct.sections = new_sections
            ct.thumbnail = f"study_materials/images/{image_rel_path}"
            ct.save()

# --- Content Data ---

POORAM_CONTENT = [
    {
        'title': 'The Festival of Festivals',
        'content': """### Thrissur Pooram: The Mother of All Poorams

**Thrissur Pooram** is the most spectacular temple festival in Kerala, celebrated annually at the Vadakkunnathan Temple in Thrissur. Conceived by **Sakthan Thampuran**, the Maharaja of Cochin, in the 18th century, it is a grand assembly of deities from neighboring temples, unified in a celebration of rhythm and light.

The festival is famous for its **Kudamattom** (exchange of umbrellas) ceremony, where two competing groups (Paramekkavu and Thiruvambady) sit atop 15 caparisoned elephants each and engage in a rhythmic and vibrant exchange of colorful, multi-layered umbrellas.

#### Example: Caparisoned Elephants
![Thrissur Pooram](/media/study_materials/images/pooram.png)
*The sight of 30 caparisoned elephants with traditional gold ornaments (Nettipattam) is the highlight of the festival.*
"""
    },
    {
        'title': 'The Rhythm of the Panchavadyam',
        'content': """### Melodic Thunder: Ilanjithara Melam

The Pooram is not just a visual treat; it is a sonic immersion. The **Ilanjithara Melam** is a magnificent performance involving over 200 musicians playing traditional instruments like the *Chenda*, *Elathalam*, *Kuzhal*, and *Kombu*.

This performance, held under the Ilanji tree in the temple courtyard, is considered one of the highest forms of traditional percussion ensembles. The synchronized beats create a crescendo that resonates through the entire city, drawing hundreds of thousands of spectators from across the globe.
"""
    }
]

THEYYAM_CONTENT = [
    {
        'title': 'When God Meets Man',
        'content': """### Theyyam: The Ritual Dance of Malabar

**Theyyam** is a popular ritual form of worship in North Kerala, particularly in the Kolathunadu region. It is more than just a dance; it is a living tradition where the performer is believed to become the **incarnation of a deity**.

There are over 400 different types of Theyyams, each with its own unique story, makeup, and costume. The most common themes involve the legends of heroes, ancestral spirits, and village deities who protect the community.

#### Example: Theyyam Performance
![Theyyam](/media/study_materials/images/theyyam.png)
*The performer's intense gaze and rhythmic movements, often performed around a fire at night, create a surreal and spiritual experience.*
"""
    }
]

# (I'll keep the previous ones too in the script to ensure they are updated with the latest images)
# ... [rest of the script remains same as before, just added Pooram and Theyyam]

# --- Execution ---

# ... [previous update calls]

update_topic_content(
    ['Thrissur Pooram'], 
    'The most spectacular temple festival of Kerala, known for its grand elephant parade and percussion.',
    POORAM_CONTENT, 
    'pooram.png'
)

update_topic_content(
    ['Theyyam'], 
    'An ancient ritual dance form where performers embody deities and local heroes.',
    THEYYAM_CONTENT, 
    'theyyam.png'
)
