"""
Management command to add general content with new 7-section topic structure and quiz data.

Topic Structure:
1. Overview - Introduction and basic understanding
2. Background / Formation - Historical context and origins
3. Key Features - Main characteristics and attributes
4. Important Examples - Notable instances and case studies
5. Key Term - Important terminology and definitions
6. Importance - Significance and relevance
7. Summary - Recap and key takeaways

Quiz Data: Max 5 questions per difficulty (easy, medium, hard) = 15 questions per topic
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from mainapp.models import Section, Topic, StudyMaterial, Question, Choice


class Command(BaseCommand):
    help = 'Add general content with new 7-section topic structure and quiz data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Starting General Content Creation ===\n'))
        
        with transaction.atomic():
            # Create sections
            env_section = self.create_or_get_section(
                'Environment', 
                'Learn about the environment, climate change, and conservation in Kerala and India'
            )
            
            her_section = self.create_or_get_section(
                'Heritage Sites',
                'Explore historical heritage sites in Kerala and their cultural significance'
            )
            
            cul_section = self.create_or_get_section(
                'Cultural Artforms',
                'Discover Kerala\'s rich cultural heritage and traditional art forms'
            )
            
            # Clear existing data for these sections to ensure source-of-truth consistency
            self.clear_section_data(env_section)
            self.clear_section_data(her_section)
            self.clear_section_data(cul_section)
            
            # ========================================
            # ENVIRONMENT SECTION
            # ========================================
            self.stdout.write(self.style.SUCCESS('\n--- Creating Environment Topics ---\n'))
            
            # Environment Section Topics (Root Topics ONLY)
            # These names are chosen to trigger specific layouts in topic_study.html
            tg1 = self.create_topic(env_section, "Highlands (Western Ghats)", "The Sahyadri mountain range.", "The Highlands (Western Ghats) form the eastern boundary of Kerala and are a UNESCO World Heritage site.")
            tg2 = self.create_topic(env_section, "Lowlands (Coastal Plains)", "The coastal area and backwaters.", "The Lowlands consists of the coastal belt and the vast network of backwaters.")
            tg3 = self.create_topic(env_section, "Midlands (The Transition Belt)", "Rolling hills and laterite plateaus.", "The Midlands represent the transitional zone between the mountains and the sea.")
            tg4 = self.create_topic(env_section, "Below Sea Level (Kuttanad)", "Unique farming at low altitude.", "Kuttanad is one of the few places in the world where farming occurs below sea level.")
            
            self.add_highlands_content(tg1, env_section)
            self.add_lowlands_content(tg2, env_section)
            self.add_midlands_content(tg3, env_section)
            self.add_kuttanad_content(tg4, env_section)
            
            # ========================================
            # HERITAGE SITES SECTION
            th1 = self.create_topic(her_section, 'Fort Kochi', 'A historic port town where European, Jewish, and Chinese cultures meet.', 'Fort Kochi is a cultural melting pot with a history spanning Portuguese, Dutch, and British eras.')
            self.add_fort_kochi_content(th1, her_section)
            
            th2 = self.create_topic(her_section, 'Padmanabhapuram Palace', 'The world\'s largest wooden palace, a masterpiece of Kerala architecture.', 'Built around 1550 AD, this palace is a testament to traditional Kerala craftsmanship without using iron nails.')
            self.add_padmanabhapuram_content(th2, her_section)
            
            th3 = self.create_topic(her_section, 'Bekal Fort', 'The largest and best-preserved fort in Kerala, rising from the Arabian Sea.', 'Built in the 17th century, Bekal Fort offers stunning views and a glimpse into Kerala\'s strategic military past.')
            self.add_bekal_fort_content(th3, her_section)
            
            th4 = self.create_topic(her_section, 'Sree Padmanabhaswamy Temple', 'The world\'s richest temple, dedicated to Lord Vishnu.', 'A legendary temple in Thiruvananthapuram known for its Dravidian architecture and hidden treasures.')
            self.add_padmanabhaswamy_content(th4, her_section)
            
            th5 = self.create_topic(her_section, 'Hill Palace Museum', 'Kerala\'s largest archaeological museum, once a royal residence.', 'Built in 1865, it was the official residence of the Cochin royal family and now houses invaluable antiques.')
            self.add_hill_palace_content(th5, her_section)
            
            th6 = self.create_topic(her_section, 'Koyikkal Palace', 'A 16th-century palace housing the largest folklore museum in the state.', 'Located near Kottayam, it preserves Kerala\'s rich folk traditions and medieval architecture.')
            self.add_koyikkal_palace_content(th6, her_section)
            
            th7 = self.create_topic(her_section, 'Krishnapuram Palace', 'A classic Kerala-style palace famous for the largest mural painting in the state.', 'Known for the "Gajendra Vargasamohanam" mural, this 18th-century palace is a treasure of art.')
            self.add_krishnapuram_content(th7, her_section)
            
            # ========================================
            # CULTURAL ARTFORMS SECTION
            # ========================================
            self.stdout.write(self.style.SUCCESS('\n--- Creating Cultural Artforms Topics ---\n'))
            
            # Kathakali
            kath_topic = self.create_topic(cul_section, 'Kathakali', 'Learn about the classical dance-drama of Kerala known for elaborate makeup', 'Kathakali is a major form of classical Indian dance. It is a "story play" genre of art, but one distinguished by the elaborately colourful make-up, costumes and face masks.')
            self.add_kathakali_content(kath_topic, cul_section)
            
            # Mohiniyattam
            moh_topic = self.create_topic(cul_section, 'Mohiniyattam', 'Discover the graceful classical dance form of Kerala', 'Mohiniyattam is an Indian classical dance form that developed and remained popular in the state of Kerala. Mohiniyattam dance is performed by women in a graceful, elegant, and gentle style.')
            self.add_mohiniyattam_content(moh_topic, cul_section)
            
            # Theyyam
            they_topic = self.create_topic(cul_section, 'Theyyam', 'Explore the ritual dance form of North Kerala', 'Theyyam is an ancient ritual art form prevalent in North Kerala, particularly in the Kannur and Kasaragod districts. It is a vibrant and powerful ritual where performers embody deities.')
            self.add_theyyam_content(they_topic, cul_section)
            
            # Kalaripayattu
            kal_topic = self.create_topic(cul_section, 'Kalaripayattu', 'Discover the ancient martial art form of Kerala', 'Kalaripayattu is an Indian martial art originating in modern-day Kerala. It is one of the oldest surviving martial arts in India, with a history spanning over 3,000 years.')
            self.add_kalaripayattu_content(kal_topic, cul_section)
            
            # Thullal
            thu_topic = self.create_topic(cul_section, 'Thullal', 'Learn about the solo dance recital tradition of Kerala', 'Ottan Thullal is a solo dance-recital art form of Kerala, created by the poet Kunchan Nambiar in the 18th century. It is characterized by its satirical humor and social criticism.')
            self.add_thullal_content(thu_topic, cul_section)
            
            # Panchavadyam
            pan_topic = self.create_topic(cul_section, 'Panchavadyam', 'Explore the traditional percussion ensemble of Kerala', 'Panchavadyam is a classical temple art form of Kerala, India. It is an ensemble of five percussion instruments, creating a mesmerizing symphony often performed during temple festivals.')
            self.add_panchavadyam_content(pan_topic, cul_section)
            
            # Kerala Mural Art
            mur_topic = self.create_topic(cul_section, 'Kerala Mural Art', 'Discover the ancient wall painting tradition of Kerala', 'Kerala Mural Art is a tradition of fresco painting, depicting Hindu mythology, that dates back to the 9th century. These murals are found in temples and palaces across Kerala.')
            self.add_mural_art_content(mur_topic, cul_section)
            
        self.stdout.write(self.style.SUCCESS('\n=== General Content Created Successfully! ===\n'))

    def create_or_get_section(self, name, description):
        section, created = Section.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'is_general': True
            }
        )
        if created:
            self.stdout.write(f'  Created section: {name}')
        else:
            section.description = description
            section.is_general = True
            section.save()
            self.stdout.write(f'  Updated section: {name}')
        return section

    def clear_section_data(self, section):
        """Clear existing topics and study materials for a section"""
        topics = Topic.objects.filter(section=section)
        for topic in topics:
            StudyMaterial.objects.filter(topic=topic).delete()
            Question.objects.filter(topic=topic).delete()
        topics.delete()
        self.stdout.write(f'  Cleared existing data for: {section.name}')

    def create_topic(self, section, name, description, intro_text, parent=None):
        # The 'order' field is now implicitly handled by the order of creation or can be set later if needed.
        # For now, we'll use the description for the topic's description field and intro_text for a new field if it existed.
        # Assuming 'description' in Topic model will store the 'intro_text' from the new calls.
        # If a separate 'short_description' field is needed, the Topic model would need modification.
        # For this change, 'description' will be the longer 'intro_text' and 'short_description' is not stored in Topic model directly.
        topic, created = Topic.objects.get_or_create(
            section=section,
            name=name,
            defaults={
                'description': intro_text, # Using intro_text for the main description field
                'parent_topic': parent,
                'is_general': True
            }
        )
        if not created and parent and topic.parent_topic != parent:
            topic.parent_topic = parent
            topic.save()
            
        if created:
            self.stdout.write(f'    Created topic: {name}')
        return topic

    def create_study_material(self, topic, title, content, order, image_url=''):
        sm, created = StudyMaterial.objects.get_or_create(
            topic=topic,
            title=title,
            defaults={
                'content_text': content,
                'order': order,
                'image_url': image_url,
                'difficulty': 'beginner'
            }
        )
        return sm

    def add_quiz_questions(self, topic, section, questions_data):
        """Add quiz questions with choices for a topic"""
        for q_data in questions_data:
            question = Question.objects.create(
                section=section,
                topic=topic,
                question_text=q_data['question'],
                difficulty=q_data['difficulty']
            )
            # Create choices
            for choice_data in q_data['choices']:
                Choice.objects.create(
                    question=question,
                    choice_text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )
        self.stdout.write(f'      Added {len(questions_data)} quiz questions')

    # ========================================
    # HIGHLANDS (WESTERN GHATS) CONTENT
    # ========================================
    def add_highlands_content(self, topic, section):
        content = """# Introduction & Overview

The **Highlands** of Kerala are dominated by the **Western Ghats** (Sahyadri), a biological island that defines the state's climate and identity. Older than the Himalayas, these mountains act as a massive "Rain-Maker" for the entire peninsula.

## Key Highlights
- **Biodiversity**: One of the world's 8 'hottest hotspots' of biological diversity.
- **Water Tower**: Source of all 44 rivers that flow through Kerala.
- **Climate Regulator**: Intercepts the monsoon winds, ensuring heavy rainfall.
- **Endemism**: Home to the Nilgiri Tahr and Lion-tailed Macaque, found nowhere else."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/western_ghats_highlands.png')
        
        content = """# The Shola-Grassland Mosaic

A symbiotic ecosystem found above 1,500m, consisting of stunted montane forests (**Sholas**) in valleys and undulating grasslands on the ridges.

## Key Concepts
- **Climatic Relicts**: Remnants of the Pleistocene Ice Age.
- **The Sponge Effect**: The Shola floor acts as a natural aquifer, absorbing monsoon rain and releasing it slowly.
- **Thermal Stability**: Shola interiors maintain a constant cool temperature, protecting sensitive species."""
        self.create_study_material(topic, 'The Shola-Grassland Mosaic', content, 2)

        content = """# Evolutionary Icons (Wildlife)

The Western Ghats is defined by **The Science of Endemism**. Key species include:
- **Nilgiri Tahr**: Expert cliff-climber with rubbery hooves.
- **Lion-tailed Macaque**: Arboreal canopy specialist.
- **Purple Frog (Patal)**: Living fossil that lives underground.
- **Great Indian Hornbill**: The "Forest Engineer" that spreads seeds.
- **Flying Lizard**: Glides between trees using patagia."""
        self.create_study_material(topic, 'Evolutionary Icons', content, 3)

        content = """# Heritage & Tribal Wisdom

## Edakkal Caves
Located on Ambukuthi Mala, these fissure caves contain petroglyphs dating back to **6,000 BCE**, proving ancient high-altitude civilizations.

## Tribal Custodians
- **Kani Tribe**: Holders of secret botanical knowledge (e.g., Arogyapacha).
- **Muthuvan Tribe**: Nomadic farmers known for their minimal-footprint "Kudi" system."""
        self.create_study_material(topic, 'Heritage & Tribal Wisdom', content, 4)

        content = """# Threats & Resilience

## Anthropogenic Pressure
- **Habitat Fragmentation**: Roads and plantations breaking up wildlife corridors.
- **Invasive Species**: Threats from Lantana and other non-native plants.

## Climate Resilience
Scientific intervention and sustainable tourism are the way forward to protect this fragile "Biological Island." """
        self.create_study_material(topic, 'Threats & Resilience', content, 5)

        quiz_data = [
            {'question': 'What is the other name for the Western Ghats?', 'difficulty': 'easy', 'choices': [
                {'text': 'Sahyadri', 'is_correct': True},
                {'text': 'Himalayas', 'is_correct': False},
                {'text': 'Nilgiris', 'is_correct': False},
                {'text': 'Vindhyas', 'is_correct': False}
            ]},
            {'question': 'Which animal is known as the "Forest Engineer" for spreading seeds of giant trees?', 'difficulty': 'easy', 'choices': [
                {'text': 'Great Indian Hornbill', 'is_correct': True},
                {'text': 'Elephant', 'is_correct': False},
                {'text': 'Macaque', 'is_correct': False},
                {'text': 'Tiger', 'is_correct': False}
            ]},
            {'question': 'Which peak is the highest in the Western Ghats (South of Himalayas)?', 'difficulty': 'easy', 'choices': [
                {'text': 'Anamudi', 'is_correct': True},
                {'text': 'Ponmudi', 'is_correct': False},
                {'text': 'Agasthyakoodam', 'is_correct': False},
                {'text': 'Chembra Peak', 'is_correct': False}
            ]},
            {'question': 'What is the "Sponge Effect" associated with Shola forests?', 'difficulty': 'medium', 'choices': [
                {'text': 'Absorbing monsoon rain and releasing it slowly', 'is_correct': True},
                {'text': 'Attracting clouds via magnetism', 'is_correct': False},
                {'text': 'Filtering salt from water', 'is_correct': False},
                {'text': 'Preventing landslides via root pressure', 'is_correct': False}
            ]},
            {'question': 'Which rare frog is considered a "living fossil" and lives underground most of the year?', 'difficulty': 'medium', 'choices': [
                {'text': 'Purple Frog (Patal)', 'is_correct': True},
                {'text': 'Bullfrog', 'is_correct': False},
                {'text': 'Tree Frog', 'is_correct': False},
                {'text': 'Malabar Flying Frog', 'is_correct': False}
            ]},
            {'question': 'Which tribe is known for their minimal-footprint "Kudi" village system?', 'difficulty': 'medium', 'choices': [
                {'text': 'Muthuvan Tribe', 'is_correct': True},
                {'text': 'Kani Tribe', 'is_correct': False},
                {'text': 'Irular Tribe', 'is_correct': False},
                {'text': 'Uraly Tribe', 'is_correct': False}
            ]},
            {'question': 'The presence of Podocarp trees in the Ghats is evidence of which prehistoric connection?', 'difficulty': 'hard', 'choices': [
                {'text': 'The Gondwana Legacy', 'is_correct': True},
                {'text': 'The Silk Road', 'is_correct': False},
                {'text': 'Tethys Sea', 'is_correct': False},
                {'text': 'Ice Age Migration', 'is_correct': False}
            ]},
            {'question': 'Which Neolithic site in the Ghats features petroglyphs dating back to 6,000 BCE?', 'difficulty': 'hard', 'choices': [
                {'text': 'Edakkal Caves', 'is_correct': True},
                {'text': 'Marayoor Dolmens', 'is_correct': False},
                {'text': 'Muziris', 'is_correct': False},
                {'text': 'Muniyara', 'is_correct': False}
            ]},
            {'question': 'What characterizes the "Shola-Grassland Mosaic" found at high altitudes?', 'difficulty': 'hard', 'choices': [
                {'text': 'Stunted montane forests in valleys and ridges of grasslands', 'is_correct': True},
                {'text': 'Dense evergreen rainforests on all slopes', 'is_correct': False},
                {'text': 'Deciduous forests with cactus', 'is_correct': False},
                {'text': 'Mangrove swamps with stilt roots', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)
        
        self.stdout.write(f'      Added Highlands content and quiz data')

    # ========================================
    # LOWLANDS (COASTAL PLAINS) CONTENT
    # ========================================
    def add_lowlands_content(self, topic, section):
        content = """# Introduction & Overview

The **Lowlands** of Kerala represent the brackish, pulse-like boundary between the land and the Arabian Sea. This region is a complex network of estuaries, deltas, and the famous **Backwaters** (Kayals).

## Key Highlights
- **Hydrological Network**: A chain of 34 backwaters and over 900 km of navigable waterways.
- **Brackish Ecology**: A unique mix of fresh river water and salt sea water.
- **Economic Lifeline**: Hub of Kerala's coir industry, inland fishing, and tourism.
- **Vembanad Lake**: The largest brackish water body in South India."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/kerala_lowlands_backwaters.png')
        self.stdout.write(f'      Added Lowlands content with regional imagery')

    # ========================================
    # MIDLANDS (TRANSITION BELT) CONTENT
    # ========================================
    def add_midlands_content(self, topic, section):
        content = """# Introduction & Overview

The **Midlands** represent Kerala’s rolling transition zone. Characterized by laterite hills and lush valleys, this region bridges the high mountains and the flat coast.

## Key Highlights
- **The Laterite Matrix**: Porous red rock that acts as a primary groundwater reservoir.
- **Sacred Groves (Kaavu)**: Ancient "islands" of primary forest preserved by tradition.
- **The Spring System**: Home to perennial springs (Charas) that feed the inland wells.
- **Transition Ecology**: A mix of highland flora and lowland agriculture."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/sacred_grove_midlands.png')
        self.stdout.write(f'      Added Midlands content with regional imagery')

    # ========================================
    # BELOW SEA LEVEL (KUTTANAD) CONTENT
    # ========================================
    def add_kuttanad_content(self, topic, section):
        content = """# Introduction & Overview

**Kuttanad**, often called the "Rice Bowl of Kerala," is a unique geographical marvel where farming is carried out **Below Sea Level**. It is one of the few places in the world with such an agricultural system.

## Key Highlights
- **Altitude**: Situated 1.5 to 2.5 meters below mean sea level.
- **Four Rivers**: Fed by the Pamba, Meenachil, Achankovil, and Manimala rivers.
- **Polder System**: Reclaimed land protected by embankments, similar to the Netherlands.
- **Heritage Farming**: Recognized by FAO as a Globally Important Agricultural Heritage System (GIAHS)."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1)
        self.stdout.write(f'      Added Kuttanad content')

    # ========================================
    # THEYYAM CONTENT
    # ========================================
    def add_theyyam_content(self, topic, section):
        content = """# Introduction & Overview

**Theyyam** (a corruption of *Daivam* or God) is an ancient ritual art form prevalent in North Kerala, particularly in the Kannur and Kasaragod districts. It is a spectacular fusion of dance, music, and mime, where the performer is believed to become the deity himself.

## Key Highlights
- **Spiritual Essence**: A channel through which the divine is invoked to bless and counsel the community.
- **Diversity**: Over 400 distinct forms of Theyyam exist, each representing a unique deity or historical hero.
- **Social Unity**: Historically, it has been a platform for breaking caste barriers as the performer often comes from marginalized communities but is worshipped by all."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/theyyam_ritual.png')

        content = """# Ritual Costumes & Makeup (Vesham)

The visual impact of Theyyam comes from its overwhelming costumes and facial painting (*Mukhathezhuthu*).

## Makeup Elements
- **Facial Art**: Intricate patterns drawn using natural colors like rice paste (white), charcoal (black), and vermilion (red).
- **Headgear (*Mudi*)**: Massive, decorated crowns made of light wood, bamboo, and coconut leaves. Some MUdis can be over 10 feet tall!
- **Body Paint**: Many Theyyams feature elaborate body painting or the use of breastplates and armlets.

## Materials Used
- **Young Coconut Fronds**: Used for skirts and fringes.
- **Peacock Feathers**: Often used to decorate the Mudi.
- **Areca Palm Leaves**: For masks and structural support."""
        self.create_study_material(topic, 'Ritual Costumes & Materials', content, 2)

        content = """# Theyyam Season 2026-2027

Theyyam is a seasonal ritual, traditionally performed in "Kavus" (Sacred Groves) and temples during the post-monsoon months.

## Calendar
- **Season Starts**: October 2026 (Thulam 1 - Malayalam Month)
- **Peak Period**: December 2026 to April 2027.
- **Season Ends**: May/June 2027 (Karkidakam).
- **Major Festivals**: Perumthitta Tharavad (December), Kanathoor Nalvar (January)."""
        self.create_study_material(topic, 'Theyyam Season & Calendar', content, 3)
        
        content = """# Background / Formation

## Origins
- Ancient ritual art form
- Dates back over 1,500 years
- Rooted in tribal traditions
- Associated with deity worship
- Performed in village temples

## History
- Primitive dance form
- Mentioned in ancient texts
- Survived through folk tradition
- Preserved by specific communities"""
        self.create_study_material(topic, 'Background / Formation', content, 4)
        
        content = """# Key Features

## Performance
- Night-long performances
- Starts after sunset
- Invocations and rituals
- Dramatic enactments
- Audience participation

## Makeup and Costumes
- Elaborate face painting
- Colorful costumes
- Traditional ornaments
- Headgear and masks
- Body decorations"""
        self.create_study_material(topic, 'Key Features', content, 5)
        
        content = """# Important Examples

## Famous Theyyam Forms
- **Vishnumurti**: Lord Vishnu form
- **Kuttichathan**: Magical character
- **Kali**: Goddess Kali
- **Sasta**: Lord Ayyappa
- **Bhairavi**: Goddess Bhairavi

## Performance Venues
- Village temples
- Sacred groves
- Family shrines
- Open grounds"""
        self.create_study_material(topic, 'Important Examples', content, 6)
        
        content = """# Key Terms

## Theyyam
"Rash" or "Red" - referring to the elaborate makeup

## Kavu
Sacred grove where Theyyam is performed

## Thottam
Ritual songs sung during Theyyam

## Velichappad
The oracle or possessed performer"""
        self.create_study_material(topic, 'Key Terms', content, 7)
        
        content = """# Importance

## Cultural Importance
- Preserves ancient traditions
- Connects to mythological roots
- Community participation
- Oral tradition carrier

## Religious Importance
- Considered sacred
- Medium for deity worship
- Blessings for villagers
- Ritual significance"""
        self.create_study_material(topic, 'Importance', content, 8)
        
        content = """# Summary

Theyyam is Kerala's ancient ritual dance:

- **Origin**: Over 1,500 years old
- **Region**: North Kerala (Kannur, Kasaragod)
- **Features**: Elaborate makeup, night performances
- **Significance**: Living ritual art form"""
        self.create_study_material(topic, 'Summary', content, 9)
        
        quiz_data = [
            {'question': 'From which region of Kerala does Theyyam originate?', 'difficulty': 'easy', 'choices': [
                {'text': 'North Kerala', 'is_correct': True},
                {'text': 'South Kerala', 'is_correct': False},
                {'text': 'Central Kerala', 'is_correct': False},
                {'text': 'All over Kerala', 'is_correct': False}
            ]},
            {'question': 'What does the term Theyyam mean?', 'difficulty': 'easy', 'choices': [
                {'text': 'Red or rash', 'is_correct': True},
                {'text': 'Dance', 'is_correct': False},
                {'text': 'God', 'is_correct': False},
                {'text': 'Mask', 'is_correct': False}
            ]},
            {'question': 'When is Theyyam typically performed?', 'difficulty': 'easy', 'choices': [
                {'text': 'At night', 'is_correct': True},
                {'text': 'In the morning', 'is_correct': False},
                {'text': 'At noon', 'is_correct': False},
                {'text': 'Any time', 'is_correct': False}
            ]},
            {'question': 'Who performs Theyyam?', 'difficulty': 'medium', 'choices': [
                {'text': 'Men only', 'is_correct': True},
                {'text': 'Women only', 'is_correct': False},
                {'text': 'Both men and women', 'is_correct': False},
                {'text': 'Children', 'is_correct': False}
            ]},
            {'question': 'What is the traditional venue for Theyyam performances?', 'difficulty': 'medium', 'choices': [
                {'text': 'Sacred groves (Kavu)', 'is_correct': True},
                {'text': 'Temples', 'is_correct': False},
                {'text': 'Theaters', 'is_correct': False},
                {'text': 'Schools', 'is_correct': False}
            ]},
            {'question': 'What are the ritual songs sung during Theyyam called?', 'difficulty': 'medium', 'choices': [
                {'text': 'Thottam', 'is_correct': True},
                {'text': 'Carnatic', 'is_correct': False},
                {'text': 'Sopanam', 'is_correct': False},
                {'text': 'Vedic chants', 'is_correct': False}
            ]},
            {'question': 'Theyyam is considered one of the oldest dance forms in Kerala, dating back how many years?', 'difficulty': 'hard', 'choices': [
                {'text': 'Over 1,500 years', 'is_correct': True},
                {'text': 'About 500 years', 'is_correct': False},
                {'text': 'About 1,000 years', 'is_correct': False},
                {'text': 'About 2,000 years', 'is_correct': False}
            ]},
            {'question': 'What is the possessed performer called in Theyyam?', 'difficulty': 'hard', 'choices': [
                {'text': 'Velichappad', 'is_correct': True},
                {'text': 'Pujari', 'is_correct': False},
                {'text': 'Pandaravaka', 'is_correct': False},
                {'text': 'Nair', 'is_correct': False}
            ]},
            {'question': 'Which famous Theyyam form depicts Lord Vishnu?', 'difficulty': 'hard', 'choices': [
                {'text': 'Vishnumurti', 'is_correct': True},
                {'text': 'Kali', 'is_correct': False},
                {'text': 'Kuttichathan', 'is_correct': False},
                {'text': 'Sasta', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KALARIPAYATTU CONTENT
    # ========================================
    def add_kalaripayattu_content(self, topic, section):
        content = """# Introduction & Overview

**Kalaripayattu** is often hailed as the "Mother of All Martial Arts." Originating in Kerala over 3,000 years ago, it is a holistic system that combines physical combat, healing arts (*Marmachikitsa*), and spiritual discipline.

## Key Highlights
- **Philosophy**: The goal is not just combat but the mastery of the mind and body.
- **Training Ground**: Performed in a "Kalari," a special pit dug into the ground.
- **Global Influence**: Believed to be the ancestor of East Asian martial arts like Kung Fu and Karate."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/kalaripayattu_combat.png')

        content = """# The Weapons of Kalari

Kalaripayattu training progresses from barehanded combat to various traditional weapons.

## Key Weapons
- **Urumi (Flexible Sword)**: The most dangerous weapon, a long flexible blade worn like a belt.
- **Valum Parichayum (Sword and Shield)**: The classic combination for warriors.
- **Kuntham (Spear)**: Used for long-range attacks.
- **Gada (Mace)**: A heavy wooden or metal weapon for strength training and combat.
- **Cheruvadi (Short Stick)**: A very fast weapon used for striking and blocking.

## Materials
- **High-grade Steel**: Used for Urumi and Swords.
- **Teak & Rosewood**: For shields and wooden training weapons.
- **Medicinal Oils**: Crucial for body flexibility and treating injuries."""
        self.create_study_material(topic, 'Weapons & Materials', content, 2)
        
        content = """# Background / Formation

## Origins
- Developed in **Kerala** around 3rd century CE
- Ancient martial art tradition
- Created by warriors and Nairs
- Mentioned in ancient texts
- Preserved through generations

## History
- Golden period under Chera dynasty
- Training for royal armies
- Decline during colonial period
- Revival in modern times"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Training Methods
- **Vadivu**: Animal postures
- **Meipayattu**: Body exercises
- **Kolthari**: Stick weapons
- **Angathari**: Advanced weapons

## Techniques
- Striking and kicking
- Grappling and locks
- Weapon combat
- Self-defense
- Flexibility exercises"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Schools (Kalari)
- **Parthazhathy Kalari**
- **Vijayanagara Kalari**
- **Mavelikkara Kalari**
- **Kottakkal Arya Vidya Sala**

## Modern Practitioners
- Migrant practitioners worldwide
- Bollywood influence
- International recognition
- Wellness applications"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Kalari
Training center for Kalaripayattu

## Guru
Master or teacher

## Vadivu
Animal postures used in training

## Meipayattu
Body exercises in Kalaripayattu

## Marmam
Vital points in the body"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Historical Importance
- Oldest martial art
- Preserves ancient traditions
- Cultural heritage
- Military history

## Modern Importance
- Self-defense
- Physical fitness
- Mental discipline
- Global recognition"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Kalaripayattu is Kerala's ancient martial art:

- **Origin**: 3rd century CE
- **Type**: Complete martial art system
- **Features**: Weapon training, body exercises
- **Significance**: Oldest martial art in the world"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'From which state in India does Kalaripayattu originate?', 'difficulty': 'easy', 'choices': [
                {'text': 'Kerala', 'is_correct': True},
                {'text': 'Tamil Nadu', 'is_correct': False},
                {'text': 'Karnataka', 'is_correct': False},
                {'text': 'Andhra Pradesh', 'is_correct': False}
            ]},
            {'question': 'In which century did Kalaripayattu originate?', 'difficulty': 'easy', 'choices': [
                {'text': '3rd century CE', 'is_correct': True},
                {'text': '10th century CE', 'is_correct': False},
                {'text': '15th century CE', 'is_correct': False},
                {'text': '1st century CE', 'is_correct': False}
            ]},
            {'question': 'What is the training center for Kalaripayattu called?', 'difficulty': 'easy', 'choices': [
                {'text': 'Kalari', 'is_correct': True},
                {'text': 'Gurukula', 'is_correct': False},
                {'text': 'Akhara', 'is_correct': False},
                {'text': 'Mandir', 'is_correct': False}
            ]},
            {'question': 'What are the animal postures in Kalaripayattu called?', 'difficulty': 'medium', 'choices': [
                {'text': 'Vadivu', 'is_correct': True},
                {'text': 'Asana', 'is_correct': False},
                {'text': 'Mudra', 'is_correct': False},
                {'text': 'Pranayama', 'is_correct': False}
            ]},
            {'question': 'What type of exercises are the body exercises in Kalaripayattu called?', 'difficulty': 'medium', 'choices': [
                {'text': 'Meipayattu', 'is_correct': True},
                {'text': 'Vadivu', 'is_correct': False},
                {'text': 'Yoga', 'is_correct': False},
                {'text': 'Pranayama', 'is_correct': False}
            ]},
            {'question': 'Who is the master or teacher in Kalaripayattu called?', 'difficulty': 'medium', 'choices': [
                {'text': 'Guru', 'is_correct': True},
                {'text': 'Acharya', 'is_correct': False},
                {'text': 'Ustad', 'is_correct': False},
                {'text': 'Pandit', 'is_correct': False}
            ]},
            {'question': 'What are the vital points in the body called in Kalaripayattu?', 'difficulty': 'hard', 'choices': [
                {'text': 'Marmam', 'is_correct': True},
                {'text': 'Chakra', 'is_correct': False},
                {'text': 'Nadi', 'is_correct': False},
                {'text': 'Prana', 'is_correct': False}
            ]},
            {'question': 'Kalaripayattu is considered one of the oldest martial arts in the world. How old is it approximately?', 'difficulty': 'hard', 'choices': [
                {'text': 'Over 2,000 years old', 'is_correct': True},
                {'text': 'About 500 years old', 'is_correct': False},
                {'text': 'About 1,000 years old', 'is_correct': False},
                {'text': 'About 100 years old', 'is_correct': False}
            ]},
            {'question': 'Which dynasty promoted Kalaripayattu during its golden period?', 'difficulty': 'hard', 'choices': [
                {'text': 'Chera dynasty', 'is_correct': True},
                {'text': 'Mughal dynasty', 'is_correct': False},
                {'text': 'British Raj', 'is_correct': False},
                {'text': 'Chola dynasty', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # THULLAL CONTENT
    # ========================================
    def add_thullal_content(self, topic, section):
        content = """# Introduction & Overview

**Thullal**, particularly *Ottan Thullal*, is a solo dance-recital form from Kerala that is famous for its wit, humor, and social satire. Created by the legendary poet **Kunchan Nambiar** in the 18th century, it was designed to bring classical stories to the common man in a language they understood.

## Key Highlights
- **Satirical Nature**: Uses humor to criticize social evils and human follies.
- **Solo Performance**: A single performer acts, dances, and sings, accompanied by a few musicians.
- **Fast-paced**: Known for its rapid-fire narration and rhythmic movements."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/tullal_satire.png')

        content = """# Costumes & Style

The Thullal costume is colorful and designed for high-energy movements.

## Costume Elements
- **Waist Dress**: A skirt made of a long piece of cloth with red and white frills, similar to Kathakali but lighter.
- **Chest Plate**: Decorated with colorful beads and glass.
- **Headgear (*Mudi*)**: A smaller, easier-to-wear crown compared to Kathakali.

## Makeup & Materials
- **Face Paint**: Predominantly green, highlighted with black around the eyes.
- **Wooden Ornaments**: Light wood is used for the ornaments to allow the performer to move and jump freely."""
        self.create_study_material(topic, 'Costumes & Materials', content, 2)
        
        content = """# Background / Formation

## Origins
- Created in **17th century**
- Founder: **Vallathol Narayana Bhattathiripad**
- Inspired by Krishnanattam
- Reform of older dance forms
- Solo interpretation

## History
- Devadasi system background
- Decline and revival
- Modern performances
- Cultural preservation"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Performance
- Solo dancer
- Narrates Puranic stories
- Expressive eye movements
- Rhythmic footwork
- Simple costume

## Dance Style
- Graceful movements
- Storytelling through eyes
- Hand gestures
- Body positions
- Musical accompaniment"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Types of Thullal
- **Ottan Thullal**: Most popular
- **Chaknan Thullal**: Rare form
- **Parayan Thullal**: Another variant

## Stories
- Ramayana episodes
- Krishna leelas
- Mahabharata tales
- Puranic legends"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Thullal
"Sacred leap" - a solo dance form

## Vallathol
The founder of modern Thullal

## Ottan Thullal
Most popular form of Thullal

## Puranas
Ancient Hindu scriptures"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Cultural Importance
- Preserves Puranic stories
- Solo performance tradition
- Literary significance
- Artistic expression

## Educational Importance
- Religious teachings
- Moral values
- Storytelling tradition
- Cultural awareness"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Thullal is Kerala's solo dance tradition:

- **Created by**: Vallathol Narayana Bhattathiripad
- **Period**: 17th century
- **Style**: Expressive solo performance
- **Content**: Puranic stories"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'Who is the founder of Thullal?', 'difficulty': 'easy', 'choices': [
                {'text': 'Vallathol Narayana Bhattathiripad', 'is_correct': True},
                {'text': 'Kunjan Nambiar', 'is_correct': False},
                {'text': 'Mahendra', 'is_correct': False},
                {'text': 'Krishnan', 'is_correct': False}
            ]},
            {'question': 'In which century was Thullal created?', 'difficulty': 'easy', 'choices': [
                {'text': '17th century', 'is_correct': True},
                {'text': '15th century', 'is_correct': False},
                {'text': '19th century', 'is_correct': False},
                {'text': '21st century', 'is_correct': False}
            ]},
            {'question': 'What type of performance is Thullal?', 'difficulty': 'easy', 'choices': [
                {'text': 'Solo dance', 'is_correct': True},
                {'text': 'Group dance', 'is_correct': False},
                {'text': 'Drama', 'is_correct': False},
                {'text': 'Music', 'is_correct': False}
            ]},
            {'question': 'What are the stories in Thullal based on?', 'difficulty': 'medium', 'choices': [
                {'text': 'Puranas', 'is_correct': True},
                {'text': 'Vedas', 'is_correct': False},
                {'text': 'Bible', 'is_correct': False},
                {'text': 'Folk tales', 'is_correct': False}
            ]},
            {'question': 'Which is the most popular form of Thullal?', 'difficulty': 'medium', 'choices': [
                {'text': 'Ottan Thullal', 'is_correct': True},
                {'text': 'Chaknan Thullal', 'is_correct': False},
                {'text': 'Parayan Thullal', 'is_correct': False},
                {'text': 'Mishra Thullal', 'is_correct': False}
            ]},
            {'question': 'What is the main medium of storytelling in Thullal?', 'difficulty': 'medium', 'choices': [
                {'text': 'Expressive eye movements', 'is_correct': True},
                {'text': 'Vocal singing only', 'is_correct': False},
                {'text': 'Facial makeup', 'is_correct': False},
                {'text': 'Complex costumes', 'is_correct': False}
            ]},
            {'question': 'Thullal is derived from which older art form?', 'difficulty': 'hard', 'choices': [
                {'text': 'Krishnanattam', 'is_correct': True},
                {'text': 'Kathakali', 'is_correct': False},
                {'text': 'Mohiniyattam', 'is_correct': False},
                {'text': 'Bharatanatyam', 'is_correct': False}
            ]},
            {'question': 'What does the word Thullal mean?', 'difficulty': 'hard', 'choices': [
                {'text': 'Sacred leap', 'is_correct': True},
                {'text': 'Temple dance', 'is_correct': False},
                {'text': 'Royal performance', 'is_correct': False},
                {'text': 'Folk dance', 'is_correct': False}
            ]},
            {'question': 'How many types of Thullal are there traditionally?', 'difficulty': 'hard', 'choices': [
                {'text': 'Three', 'is_correct': True},
                {'text': 'Two', 'is_correct': False},
                {'text': 'Five', 'is_correct': False},
                {'text': 'One', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # PANCHAVADYAM CONTENT
    # ========================================
    def add_panchavadyam_content(self, topic, section):
        content = """# Introduction & Overview

**Panchavadyam** is Kerala's majestic "orchestra of five instruments." It is a spontaneous and rhythmic percussion ensemble that is a hallmark of Kerala's temple festivals, particularly the world-famous *Thrissur Pooram*.

## Key Highlights
- **Symphony of Five**: Combines four percussion instruments and one wind instrument.
- **Pyramidal Rhythm**: The tempo starts very slow and gradually accelerates to a breathtaking crescendo.
- **Collective Spirit**: Can involve dozens of artists performing in perfect harmony."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/panchavadyam_ensemble.png')

        content = """# The Five Instruments

Each instrument in Panchavadyam has a unique role and sound.

## The Ensemble
1. **Thimila**: An hour-glass shaped drum, the lead instrument.
2. **Maddalam**: A heavy drum made of jackfruit wood and leather.
3. **Idakka**: A small, delicate drum used for melodic variations.
4. **Ilathalam**: Bronze cymbals that provide the rhythmic backbone.
5. **Kombu**: A C-shaped brass trumpet, the only wind instrument in the group.

## Materials
- **Jackfruit Wood**: Preferred for making the bodies of Thimila and Maddalam.
- **Animal Hide**: Carefully cured leather used for the drum heads.
- **Bronze**: For the Ilathalam cymbals."""
        self.create_study_material(topic, 'Instruments & Materials', content, 2)

        content = """# Festival Calendar 2026-2027

Panchavadyam is the heartbeat of major temple festivals in Central Kerala.

## Major Dates
- **Thrissur Pooram**: April 27, 2026 (The most famous 'Madhilkkunnu' Panchavadyam).
- **Arattupuzha Pooram**: March 2026 (An ancient and grand ensemble).
- **Uthralikkavu Pooram**: February 2026."""
        self.create_study_material(topic, 'Festival Calendar', content, 3)
        
        content = """# Background / Formation

## Origins
- Ancient Kerala tradition
- Developed over centuries
- Temple ritual background
- Folk art integration
- Royal patronage

## History
- References in ancient texts
- Temple festival tradition
- Community performances
- Modern adaptations"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Instruments
1. **Panchavadyam** - Five instruments
2. **Thimila** - Bronze kettle drum
3. **Idakka** - Damaru-shaped drum
4. **Cymbals** - Metallic plates
5. **Mizhavu** - Large earthen drum

## Performance Style
- Processional music
- Festival accompaniment
- Competitive ensembles
- Complex rhythms"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Famous Ensembles
- **Pottamkulal Panchavadyam**
- **Kottayam Panchavadyam**
- **Kunnamkulam Panchavadyam**

## Festivals
- Temple festivals
- Onam celebrations
- Cultural programs
- Processions"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Panchavadyam
"Five instruments" - the percussion ensemble

## Thimila
Bronze kettle drum - primary instrument

## Idakka
Damru-shaped drum used in Panchavadyam

## Mizhavu
Large earthen drum with distinctive sound"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Cultural Importance
- Temple heritage
- Festival traditions
- Community participation
- Artistic expression

## Musical Importance
- Unique rhythm patterns
- Instrumental innovation
- Traditional preservation
- Musical training"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Panchavadyam is Kerala's traditional percussion ensemble:

- **Instruments**: Five (Panchavadyam)
- **Occasion**: Temple festivals
- **Style**: Processional and rhythmic
- **Significance**: Cultural identity"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What does Panchavadyam literally mean?', 'difficulty': 'easy', 'choices': [
                {'text': 'Five instruments', 'is_correct': True},
                {'text': 'Five drums', 'is_correct': False},
                {'text': 'Five sounds', 'is_correct': False},
                {'text': 'Five beats', 'is_correct': False}
            ]},
            {'question': 'Where is Panchavadyam primarily performed?', 'difficulty': 'easy', 'choices': [
                {'text': 'Temple festivals', 'is_correct': True},
                {'text': 'Theaters', 'is_correct': False},
                {'text': 'Concerts', 'is_correct': False},
                {'text': 'Schools', 'is_correct': False}
            ]},
            {'question': 'How many instruments are in Panchavadyam?', 'difficulty': 'easy', 'choices': [
                {'text': 'Five', 'is_correct': True},
                {'text': 'Four', 'is_correct': False},
                {'text': 'Three', 'is_correct': False},
                {'text': 'Six', 'is_correct': False}
            ]},
            {'question': 'Which is the primary drum in Panchavadyam?', 'difficulty': 'medium', 'choices': [
                {'text': 'Thimila', 'is_correct': True},
                {'text': 'Tabla', 'is_correct': False},
                {'text': 'Mridangam', 'is_correct': False},
                {'text': 'Drums', 'is_correct': False}
            ]},
            {'question': 'What type of drum is the Idakka?', 'difficulty': 'medium', 'choices': [
                {'text': 'Damru-shaped', 'is_correct': True},
                {'text': 'Kettle-shaped', 'is_correct': False},
                {'text': 'Cylindrical', 'is_correct': False},
                {'text': 'Double-headed', 'is_correct': False}
            ]},
            {'question': 'What is the Mizhavu made of?', 'difficulty': 'medium', 'choices': [
                {'text': 'Earthen', 'is_correct': True},
                {'text': 'Wood', 'is_correct': False},
                {'text': 'Metal', 'is_correct': False},
                {'text': 'Leather', 'is_correct': False}
            ]},
            {'question': 'Panchavadyam is a traditional art form from which Indian state?', 'difficulty': 'hard', 'choices': [
                {'text': 'Kerala', 'is_correct': True},
                {'text': 'Tamil Nadu', 'is_correct': False},
                {'text': 'Karnataka', 'is_correct': False},
                {'text': 'Andhra Pradesh', 'is_correct': False}
            ]},
            {'question': 'What type of performances is Panchavadyam known for?', 'difficulty': 'hard', 'choices': [
                {'text': 'Processional music', 'is_correct': True},
                {'text': 'Solo performances', 'is_correct': False},
                {'text': 'Court music', 'is_correct': False},
                {'text': 'Devotional singing', 'is_correct': False}
            ]},
            {'question': 'Which instrument in Panchavadyam is made of bronze?', 'difficulty': 'hard', 'choices': [
                {'text': 'Thimila', 'is_correct': True},
                {'text': 'Mizhavu', 'is_correct': False},
                {'text': 'Cymbals', 'is_correct': False},
                {'text': 'Idakka', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KERALA MURAL ART CONTENT
    # ========================================
    def add_mural_art_content(self, topic, section):
        content = """# Introduction & Overview

**Kerala Mural Art** is a tradition of fresco painting that dates back to the 9th to 12th centuries AD. These paintings, usually found on temple and palace walls, are known for their technical precision, vibrant natural colors, and depictions of Hindu mythology.

## Key Highlights
- **Vibrant Palette**: Uses a restricted set of five colors (*Panchavarna*).
- **Spiritual Themes**: Depicts stories of deities like Shiva, Vishnu, and Ganesha in grand detail.
- **Architectural Harmony**: The murals are designed to blend seamlessly with Kerala's traditional wooden architecture."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/kerala_mural_artist.png')

        content = """# Traditional Materials & Pigments

The most remarkable feature of Kerala Murals is the use of 100% natural materials.

## The Panchavarna (Five Colors)
1. **Yellow (*Manayola*)**: Derived from yellow arsenic.
2. **Red (*Shathalingam*)**: Derived from cinnabar.
3. **Green (*Eravikkara*)**: A mineral pigment or extract from the *Eravikkara* plant.
4. **White**: Made from lime or rice paste.
5. **Black**: Soot collected from oil lamps burning sesamum oil.

## Preparation
- **Brushes**: Made from the hair of calves' ears or certain types of grass.
- **Base**: The walls are prepared with a mixture of lime, sand, and coconut water to ensure the colors last for centuries."""
        self.create_study_material(topic, 'Materials & Pigments', content, 2)
        
        content = """# Background / Formation

## Origins
- Developed in **14th century**
- Peak period under **Travancore**
- Influenced by Pallava art
- Temple construction boom
- Royal patronage

## History
- Ancient painting traditions
- Temple decoration
- Palace murals
- Church paintings
- Modern revival"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Artistic Style
- Bold outlines
- Vibrant natural colors
- Two-dimensional figures
- Decorative backgrounds
- Symbolic representations

## Techniques
- Natural pigments
- Lime plaster preparation
- Layered painting
- Geometric patterns
- Floral designs"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Famous Murals
- **Padmanabhapuram Palace**
- **Krishnapuram Palace**
- **Mattancherry Palace**
- **Vijayanagara Fort**

## Themes
- Hindu mythology
- Krishna legends
- Ramayana stories
- Goddess depictions
- Court scenes"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Mural Art
Wall paintings on permanent surfaces

## Pigments
Natural colors used in murals

## Fresco
Painting on wet plaster

## Tempera
Paint mixed with binding agent"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Artistic Importance
- Unique Indian art form
- Preserves traditions
- Cultural identity
- Aesthetic value

## Historical Importance
- Documents history
- Religious significance
- Royal lifestyle
- Architectural heritage"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Kerala Mural Art is the ancient wall painting tradition:

- **Origin**: 14th century
- **Style**: Bold lines, vivid colors
- **Locations**: Temples, palaces
- **Themes**: Hindu mythology"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'In which century did Kerala Mural Art originate?', 'difficulty': 'easy', 'choices': [
                {'text': '14th century', 'is_correct': True},
                {'text': '10th century', 'is_correct': False},
                {'text': '18th century', 'is_correct': False},
                {'text': '20th century', 'is_correct': False}
            ]},
            {'question': 'Where are Kerala murals primarily found?', 'difficulty': 'easy', 'choices': [
                {'text': 'Temples and palaces', 'is_correct': True},
                {'text': 'Homes', 'is_correct': False},
                {'text': 'Museums', 'is_correct': False},
                {'text': 'Caves', 'is_correct': False}
            ]},
            {'question': 'What characterizes Kerala mural paintings?', 'difficulty': 'easy', 'choices': [
                {'text': 'Vivid colors and bold lines', 'is_correct': True},
                {'text': 'Abstract designs', 'is_correct': False},
                {'text': 'Modern art style', 'is_correct': False},
                {'text': 'Landscapes only', 'is_correct': False}
            ]},
            {'question': 'Which kingdom promoted Kerala murals during its peak?', 'difficulty': 'medium', 'choices': [
                {'text': 'Travancore', 'is_correct': True},
                {'text': 'Mughal', 'is_correct': False},
                {'text': 'British', 'is_correct': False},
                {'text': 'Chola', 'is_correct': False}
            ]},
            {'question': 'What type of themes are depicted in Kerala murals?', 'difficulty': 'medium', 'choices': [
                {'text': 'Hindu mythology', 'is_correct': True},
                {'text': 'Modern life', 'is_correct': False},
                {'text': 'Western art', 'is_correct': False},
                {'text': 'Landscapes', 'is_correct': False}
            ]},
            {'question': 'What kind of pigments were used in traditional Kerala murals?', 'difficulty': 'medium', 'choices': [
                {'text': 'Natural pigments', 'is_correct': True},
                {'text': 'Synthetic colors', 'is_correct': False},
                {'text': 'Oil paints', 'is_correct': False},
                {'text': 'Watercolors', 'is_correct': False}
            ]},
            {'question': 'Which palace is famous for its Kerala murals?', 'difficulty': 'hard', 'choices': [
                {'text': 'Krishnapuram Palace', 'is_correct': True},
                {'text': 'Red Fort', 'is_correct': False},
                {'text': 'Hawa Mahal', 'is_correct': False},
                {'text': 'Mysore Palace', 'is_correct': False}
            ]},
            {'question': 'What technique involves painting on wet plaster?', 'difficulty': 'hard', 'choices': [
                {'text': 'Fresco', 'is_correct': True},
                {'text': 'Oil painting', 'is_correct': False},
                {'text': 'Watercolor', 'is_correct': False},
                {'text': 'Acrylic', 'is_correct': False}
            ]},
            {'question': 'Kerala murals are known for their two-dimensional figures and decorative backgrounds. What painting style is this?', 'difficulty': 'hard', 'choices': [
                {'text': 'Traditional Indian style', 'is_correct': True},
                {'text': 'Realistic style', 'is_correct': False},
                {'text': 'Impressionist style', 'is_correct': False},
                {'text': 'Cubist style', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # CLIMATE CHANGE CONTENT
    # ========================================
    def add_climate_change_content(self, topic, section):
        content = """# Introduction & Overview

**Climate Change** is the defining challenge of our era. It refers to the long-term shifts in global temperatures and weather patterns. In Kerala, these changes are felt through increasingly unpredictable monsoons and rising sea levels along our 590 km coastline.

## Key Facts
- **The Human Element**: Since the 19th century, human activities like burning fossil fuels have been the primary driver of global warming.
- **The Greenhouse Effect**: Trace gases in our atmosphere trap heat, acting like a blanket around the Earth.
- **Local Impact**: Kerala's high population density and coastal geography make it particularly vulnerable to extreme weather events."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1)
        
        content = """# Background / Formation

## Causes of Climate Change

### Natural Causes
- **Volcanic eruptions** - Release greenhouse gases
- **Solar radiation variations** - Changes in sun's energy
- **Ocean current changes** - Affect heat distribution
- **Natural greenhouse gases** - Methane from wetlands

### Human Causes (Primary Driver)
- **Burning fossil fuels** - Coal, oil, and natural gas
- **Deforestation** - Reduces carbon absorption
- **Industrial processes** - Release greenhouse gases
- **Agriculture** - Methane from livestock and rice paddies
- **Transportation** - Vehicle emissions

## The Greenhouse Effect
The greenhouse effect is a natural process that warms Earth's surface. Human activities have intensified this effect by adding more greenhouse gases to the atmosphere."""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Greenhouse Gases
- **Carbon Dioxide (CO2)** - From burning fossil fuels
- **Methane (CH4)** - From agriculture and landfills
- **Nitrous Oxide (N2O)** - From fertilizers
- **Water Vapor** - Amplifies warming
- **CFCs** - From refrigerants

## Evidence of Climate Change
1. **Rising temperatures** - Each decade since 1980 has been warmer
2. **Melting ice caps** - Arctic sea ice declining
3. **Sea level rise** - Oceans expanding as they warm
4. **Changing precipitation** - Some areas wetter, others drier
5. **Ocean acidification** - CO2 dissolving in oceans"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Recent Climate Events
- **2018 Kerala Floods** - Unprecedented rainfall in Kerala
- **Australian Bushfires (2019-2020)** - Devastating wildfires
- **European Heatwaves (2022)** - Record temperatures
- **Glacial Lake Outburst Floods** - In Himalayan region

## Global Initiatives
- **Paris Agreement (2015)** - Limit warming to 1.5-2C
- **Kyoto Protocol** - Reduce emissions
- **IPCC Reports** - Scientific assessments
- **UN Climate Summits** - Annual negotiations

## Indian Initiatives
- **National Action Plan on Climate Change**
- **Solar Energy Mission**
- **National Green Tribunal**
- **Electric Vehicle Promotion**"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Carbon Footprint
The total amount of greenhouse gases produced by our actions, measured in CO2 equivalent.

## Global Warming
The increase in Earth's average surface temperature due to greenhouse gases.

## Climate Adaptation
Adjusting to current or expected climate change effects to reduce harm.

## Climate Mitigation
Actions to reduce greenhouse gas emissions to limit climate change.

## Carbon Neutral
Achieving net-zero carbon dioxide emissions by balancing emissions with removal.

## Paris Agreement
International treaty on climate change adopted in 2015 by 196 parties.

## IPCC
Intergovernmental Panel on Climate Change - the UN body for assessing climate science."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Environmental Impact
- Loss of biodiversity as habitats change
- Coral reef destruction
- Extreme weather events
- Water scarcity in many regions

## Economic Impact
- Damage to infrastructure from floods and storms
- Agricultural losses
- Healthcare costs
- Displacement of populations

## Social Impact
- Food and water insecurity
- Climate refugees
- Health impacts from heat and disease
- Conflict over resources"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Climate change is one of the greatest challenges facing humanity today:

- **Main cause**: Human activities, especially burning fossil fuels
- **Key indicator**: 1.1C increase in global temperature
- **CO2 levels**: Over 420 ppm - highest in 2 million years
- **Solution**: Requires both mitigation and adaptation
- **India's role**: Implementing renewable energy and climate policies

Individual actions combined with government policies and international cooperation can help combat climate change for a sustainable future."""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What is the main cause of current climate change?', 'difficulty': 'easy', 'choices': [
                {'text': 'Human activities', 'is_correct': True},
                {'text': 'Natural cycles', 'is_correct': False},
                {'text': 'Volcanic eruptions', 'is_correct': False},
                {'text': 'Ocean currents', 'is_correct': False}
            ]},
            {'question': 'What is the current CO2 level in the atmosphere?', 'difficulty': 'easy', 'choices': [
                {'text': 'Over 420 ppm', 'is_correct': True},
                {'text': 'About 200 ppm', 'is_correct': False},
                {'text': 'About 100 ppm', 'is_correct': False},
                {'text': 'About 600 ppm', 'is_correct': False}
            ]},
            {'question': 'Which gas is the primary driver of the greenhouse effect?', 'difficulty': 'easy', 'choices': [
                {'text': 'Carbon Dioxide', 'is_correct': True},
                {'text': 'Oxygen', 'is_correct': False},
                {'text': 'Nitrogen', 'is_correct': False},
                {'text': 'Hydrogen', 'is_correct': False}
            ]},
            {'question': 'How much has the global average temperature increased since the late 19th century?', 'difficulty': 'medium', 'choices': [
                {'text': 'About 1.1C', 'is_correct': True},
                {'text': 'About 5C', 'is_correct': False},
                {'text': 'About 0.1C', 'is_correct': False},
                {'text': 'About 10C', 'is_correct': False}
            ]},
            {'question': 'In which year was the Paris Agreement adopted?', 'difficulty': 'medium', 'choices': [
                {'text': '2015', 'is_correct': True},
                {'text': '2010', 'is_correct': False},
                {'text': '2000', 'is_correct': False},
                {'text': '2020', 'is_correct': False}
            ]},
            {'question': 'What does the term "carbon footprint" refer to?', 'difficulty': 'medium', 'choices': [
                {'text': 'Total greenhouse gases produced by our actions', 'is_correct': True},
                {'text': 'Amount of carbon in soil', 'is_correct': False},
                {'text': 'Size of carbon particles', 'is_correct': False},
                {'text': 'Carbon stored in forests', 'is_correct': False}
            ]},
            {'question': 'Which organization publishes the IPCC reports on climate change?', 'difficulty': 'hard', 'choices': [
                {'text': 'United Nations', 'is_correct': True},
                {'text': 'World Bank', 'is_correct': False},
                {'text': 'European Union', 'is_correct': False},
                {'text': 'NASA', 'is_correct': False}
            ]},
            {'question': 'What is the target of the Paris Agreement to limit global warming?', 'difficulty': 'hard', 'choices': [
                {'text': '1.5-2C above pre-industrial levels', 'is_correct': True},
                {'text': '3-4C above pre-industrial levels', 'is_correct': False},
                {'text': 'Below 0.5C above pre-industrial levels', 'is_correct': False},
                {'text': '5C above pre-industrial levels', 'is_correct': False}
            ]},
            {'question': 'Which of the following is a climate change mitigation strategy?', 'difficulty': 'hard', 'choices': [
                {'text': 'Transitioning to renewable energy', 'is_correct': True},
                {'text': 'Building flood defenses', 'is_correct': False},
                {'text': 'Developing drought-resistant crops', 'is_correct': False},
                {'text': 'Relocating communities from vulnerable areas', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # WILDLIFE PROTECTION CONTENT
    # ========================================
    def add_wildlife_protection_content(self, topic, section):
        content = """# Introduction & Overview

**Wildlife Protection** is the practice of protecting endangered plant and animal species and their habitats. India is one of the world's 17 "megadiverse" countries, and its conservation efforts are crucial for global biodiversity.

## Key Highlights
- **Legal Backbone**: The Wildlife Protection Act of 1972 is the primary law safeguarding India's animals.
- **Success Stories**: Iconic species like the Bengal Tiger and One-horned Rhino have seen their populations bounce back due to dedicated projects.
- **The Human Link**: Effective conservation now focuses on community participation and reducing human-wildlife conflict."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1)
        
        content = """# Background / Formation

## History of Wildlife Conservation in India
- **1972**: Wildlife Protection Act enacted
- **1973**: Project Tiger launched
- **1986**: Forest Conservation Act
- **1992**: Project Elephant launched
- **2003**: Biological Diversity Act

## Conservation Network
- Wildlife Sanctuaries: 550+
- National Parks: 100+
- Tiger Reserves: 50+
- Conservation Reserves: 100+"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Major Conservation Projects
- **Project Tiger**: 1973, 50+ reserves, saved tigers from extinction
- **Project Elephant**: 1992, 30+ elephant reserves
- **Sea Turtle Project**: Protect marine turtles
- **Vulture Conservation**: Save vultures from diclofenac

## Protected Areas
- National Parks: Complete protection
- Wildlife Sanctuaries: Limited human activities
- Conservation Reserves: Community involvement
- Tiger/Elephant Corridors: Migration routes"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Success Stories
- **Bengal Tiger**: Population increased from 1,400 (1973) to 3,000+
- **Indian Rhino**: Increased from 200 (1975) to 3,500+
- **Lion-tailed Macaque**: Protected in Silent Valley

## National Parks in Kerala
- **Periyar National Park**: Elephant and tiger habitat
- **Silent Valley National Park**: Rare species
- **Eravikulam National Park**: Nilgiri Tahr

## Endangered Species
- Bengal Tiger, Asiatic Lion
- Snow Leopard, One-horned Rhinoceros
- Great Indian Bustard, Ganges River Dolphin"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Endangered Species
Species at risk of becoming extinct due to low population or threats.

## Poaching
Illegal hunting or capturing of wild animals.

## Habitat Loss
Destruction of natural environments where species live.

## Biodiversity Hotspot
Region with high species diversity under threat.

## IUCN Red List
Global list of threatened species conservation status.

## Wildlife Corridor
Protected route connecting fragmented habitats."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Ecological Value
- Maintains ecosystem balance
- Supports food chains
- Pollination and seed dispersal
- Natural pest control

## Economic Value
- Tourism revenue
- Forest products
- Medical research
- Agricultural benefits

## Cultural Value
- Part of Indian identity
- Religious significance
- Traditional knowledge
- Educational value"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Wildlife protection is crucial for maintaining ecological balance:

- **Project Tiger** increased tiger population from 1,400 to 3,000+
- India has **550+ wildlife sanctuaries** and **100+ national parks**
- **Wildlife Protection Act 1972** provides legal protection
- Conservation requires community participation
- Success stories show protection efforts work"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'When was Project Tiger launched in India?', 'difficulty': 'easy', 'choices': [
                {'text': '1973', 'is_correct': True},
                {'text': '1980', 'is_correct': False},
                {'text': '1965', 'is_correct': False},
                {'text': '1990', 'is_correct': False}
            ]},
            {'question': 'What is India\'s national animal?', 'difficulty': 'easy', 'choices': [
                {'text': 'Bengal Tiger', 'is_correct': True},
                {'text': 'Asiatic Lion', 'is_correct': False},
                {'text': 'Indian Elephant', 'is_correct': False},
                {'text': 'One-horned Rhinoceros', 'is_correct': False}
            ]},
            {'question': 'How many tiger reserves are there in India?', 'difficulty': 'easy', 'choices': [
                {'text': 'Over 50', 'is_correct': True},
                {'text': 'About 10', 'is_correct': False},
                {'text': 'About 100', 'is_correct': False},
                {'text': 'About 5', 'is_correct': False}
            ]},
            {'question': 'What was the tiger population in India in 1973?', 'difficulty': 'medium', 'choices': [
                {'text': 'About 1,400', 'is_correct': True},
                {'text': 'About 500', 'is_correct': False},
                {'text': 'About 3,000', 'is_correct': False},
                {'text': 'About 200', 'is_correct': False}
            ]},
            {'question': 'Which national park in Kerala is home to the Nilgiri Tahr?', 'difficulty': 'medium', 'choices': [
                {'text': 'Eravikulam National Park', 'is_correct': True},
                {'text': 'Periyar National Park', 'is_correct': False},
                {'text': 'Silent Valley National Park', 'is_correct': False},
                {'text': 'Bandipur National Park', 'is_correct': False}
            ]},
            {'question': 'What law provides legal protection to wildlife in India?', 'difficulty': 'medium', 'choices': [
                {'text': 'Wildlife Protection Act 1972', 'is_correct': True},
                {'text': 'Forest Conservation Act 1986', 'is_correct': False},
                {'text': 'Biological Diversity Act 2003', 'is_correct': False},
                {'text': 'Environmental Protection Act 1986', 'is_correct': False}
            ]},
            {'question': 'The Indian rhinoceros population has increased from about 200 in 1975 to what number today?', 'difficulty': 'hard', 'choices': [
                {'text': 'Over 3,500', 'is_correct': True},
                {'text': 'About 1,000', 'is_correct': False},
                {'text': 'About 500', 'is_correct': False},
                {'text': 'Over 5,000', 'is_correct': False}
            ]},
            {'question': 'What is the IUCN Red List?', 'difficulty': 'hard', 'choices': [
                {'text': 'Global list of threatened species conservation status', 'is_correct': True},
                {'text': 'List of national parks in India', 'is_correct': False},
                {'text': 'List of endangered animals in Kerala', 'is_correct': False},
                {'text': 'A wildlife documentary series', 'is_correct': False}
            ]},
            {'question': 'Which international body declares species as endangered or threatened?', 'difficulty': 'hard', 'choices': [
                {'text': 'IUCN (International Union for Conservation of Nature)', 'is_correct': True},
                {'text': 'UNEP (United Nations Environment Programme)', 'is_correct': False},
                {'text': 'WWF (World Wildlife Fund)', 'is_correct': False},
                {'text': 'UNESCO', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KERALA RIVERS & BACKWATERS CONTENT
    # ========================================
    def add_rivers_backwaters_content(self, topic, section):
        content = """# Introduction & Overview

Kerala is often called the "Land of 44 Rivers." These rivers, along with the labyrinthine network of **Backwaters**, form the watery veins of the state, supporting millions of livelihoods and a unique way of life centered around the water.

## Key Highlights
- **The Flow**: 41 rivers flow westward towards the Arabian Sea, while 3 flow eastward.
- **The Backwaters**: These are a chain of brackish lagoons and lakes lying parallel to the Arabian Sea coast.
- **Vembanad Lake**: The longest lake in India and the heart of Kerala's backwater tourism."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1)
        
        content = """# Background / Formation

## River Systems
### West Flowing Rivers (41)
- **Periyar** - Longest river (244 km)
- **Bharatapuzha** (River of Heaven)
- **Pamba River** - Flows to Vembanad
- **Chalakudy River**

### East Flowing Rivers (3)
- **Kabani** (Kabini)
- **Bhavani**
- **Pennai**

## Backwater Formation
- Created by sea invasion into low-lying areas
- Connected by canals
- Form unique lagoon ecosystem
- Support diverse flora and fauna"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Major Backwaters
- **Vembanad Lake** - Largest in Kerala
- **Ashtamudi Lake** - Eight arms
- **Poovar Backwater**
- **Kumarakom Backwaters**
- **Kochi Backwaters**

## River Features
- Originate from Western Ghats
- Monsoon-fed rivers
- Many dams built for irrigation
- Support agriculture and drinking water"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Major Dams
- **Mullaperiyar Dam** (1895) - Oldest in Kerala
- **Idukki Dam** - Double curvature arch dam
- **Kallanai Dam** - Oldest dam in India

## Famous Boats
- **Houseboats** - Tourist attraction in Alappuzha
- **Kettuvallams** - Traditional cargo boats

## Tourist Destinations
- Alappuzha (Venice of the East)
- Kumarakom Bird Sanctuary
- Pathiramanal Island"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Backwater
A body of water formed by the meeting of a river and the sea, creating a lagoon-like environment.

## Kettuvallam
Traditional Kerala houseboat used for cargo transport, now modified for tourism.

## Estuary
Where a river meets the sea, mixing freshwater with saltwater.

## Mullaperiyar Dam
One of the oldest dams in India, built in 1895 on the Periyar River.

## Vembanad Lake
The largest lake in Kerala, spanning Alappuzha, Kottayam, and Ernakulam districts."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Economic Importance
- **Tourism**: Houseboats and backwater cruises
- **Agriculture**: Irrigation for paddy fields
- **Fishing**: Freshwater and brackish water fish
- **Transportation**: Traditional boat travel

## Ecological Importance
- **Biodiversity**: Unique aquatic ecosystem
- **Bird Habitat**: Migratory birds winter here
- **Mangrove Protection**: Coastal protection

## Cultural Importance
- **Snake Boat Race**: Nehru Trophy Snake Boat Race
- **Traditional Arts**: Backwater settings in literature
- **Fishing Communities**: Traditional occupations"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Kerala's rivers and backwaters are vital to the state's identity:

- **44 rivers** originate from Western Ghats
- **Vembanad Lake** is the largest backwater
- **Mullaperiyar Dam** is one of India's oldest dams
- Support **tourism, agriculture, and biodiversity**
- **Houseboats** are major tourist attraction"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'How many rivers are there in Kerala?', 'difficulty': 'easy', 'choices': [
                {'text': '44 rivers', 'is_correct': True},
                {'text': '20 rivers', 'is_correct': False},
                {'text': '60 rivers', 'is_correct': False},
                {'text': '30 rivers', 'is_correct': False}
            ]},
            {'question': 'Which is the longest river in Kerala?', 'difficulty': 'easy', 'choices': [
                {'text': 'Periyar', 'is_correct': True},
                {'text': 'Pamba', 'is_correct': False},
                {'text': 'Bharatapuzha', 'is_correct': False},
                {'text': 'Chalakudy', 'is_correct': False}
            ]},
            {'question': 'Which is the largest lake in Kerala?', 'difficulty': 'easy', 'choices': [
                {'text': 'Vembanad Lake', 'is_correct': True},
                {'text': 'Ashtamudi Lake', 'is_correct': False},
                {'text': 'Kayamkulam Lake', 'is_correct': False},
                {'text': 'Sasthamkotta Lake', 'is_correct': False}
            ]},
            {'question': 'In which year was the Mullaperiyar Dam built?', 'difficulty': 'medium', 'choices': [
                {'text': '1895', 'is_correct': True},
                {'text': '1905', 'is_correct': False},
                {'text': '1885', 'is_correct': False},
                {'text': '1910', 'is_correct': False}
            ]},
            {'question': 'What is the traditional Kerala houseboat called?', 'difficulty': 'medium', 'choices': [
                {'text': 'Kettuvallam', 'is_correct': True},
                {'text': 'Dhoni', 'is_correct': False},
                {'text': 'Charam', 'is_correct': False},
                {'text': 'Vallam', 'is_correct': False}
            ]},
            {'question': 'How many rivers in Kerala flow westwards to the Arabian Sea?', 'difficulty': 'medium', 'choices': [
                {'text': '41 rivers', 'is_correct': True},
                {'text': '35 rivers', 'is_correct': False},
                {'text': '38 rivers', 'is_correct': False},
                {'text': '30 rivers', 'is_correct': False}
            ]},
            {'question': 'Alappuzha is known as what?', 'difficulty': 'hard', 'choices': [
                {'text': 'Venice of the East', 'is_correct': True},
                {'text': 'Queen of the Backwaters', 'is_correct': False},
                {'text': 'Gateway to Kerala', 'is_correct': False},
                {'text': 'City of Lakes', 'is_correct': False}
            ]},
            {'question': 'What type of dam is the Idukki Dam?', 'difficulty': 'hard', 'choices': [
                {'text': 'Double curvature arch dam', 'is_correct': True},
                {'text': 'Gravity dam', 'is_correct': False},
                {'text': 'Earthen dam', 'is_correct': False},
                {'text': 'Buttress dam', 'is_correct': False}
            ]},
            {'question': 'Which famous snake boat race is held on the Punnamada Lake?', 'difficulty': 'hard', 'choices': [
                {'text': 'Nehru Trophy Snake Boat Race', 'is_correct': True},
                {'text': 'Champakulam Boat Race', 'is_correct': False},
                {'text': 'Aranmula Boat Race', 'is_correct': False},
                {'text': 'President\'s Trophy Boat Race', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KERALA FORESTS & WILDLIFE CONTENT
    # ========================================
    def add_forests_wildlife_content(self, topic, section):
        content = """# Introduction & Overview

Kerala's **Forests and Wildlife** are a treasure trove of biological diversity. From the misty high-altitude shola grasslands to the dense tropical evergreen rainforests, these ecosystems are the green lungs of the state.

## Key Highlights
- **Endemism**: Many species found here, like the Lion-tailed Macaque, are found nowhere else on Earth.
- **Protection**: Over 23% of Kerala's land is under forest cover, with numerous National Parks and Wildlife Sanctuaries.
- **The Web of Life**: These forests are vital for the state's water security, acting as catchments for all 44 rivers."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1)
        
        content = """# Background / Formation

## Forest Types in Kerala
### Tropical Rainforests
- Found in Western Ghats
- High rainfall areas
- Dense canopy
- High biodiversity

### Semi-Evergreen Forests
- Mix of evergreen and deciduous
- Found in mid-elevation areas
- Important for wildlife

### Montane Grasslands (Sholas)
- Found at high elevations
- Unique ecosystem
- Home to endemic species"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Wildlife Sanctuaries
- **Wayanad Wildlife Sanctuary**
- **Periyar Tiger Reserve**
- **Silent Valley National Park**
- **Eravikulam National Park**
- **Mukurthi National Park**

## Forest Fauna
- **Mammals**: Tiger, Elephant, Leopard, Gaur
- **Primates**: Lion-tailed Macaque, Bonnet Macaque
- **Birds**: Great Indian Hornbill, Malabar Trogon
- **Butterflies**: Over 300 species"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Protected Areas
- **Periyar Tiger Reserve**: One of India's best tiger habitats
- **Silent Valley**: Pristine rainforests
- **Eravikulam**: Nilgiri Tahr conservation
- **Wayanad**: Elephant corridor

## Endemic Species
- **Lion-tailed Macaque**: World's rarest primate
- **Malabar Giant Squirrel**
- **Neelakurinji**: Blooms every 12 years
- **Great Indian Hornbill**"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Shola Forests
Tropical montane forests found in the valleys of the Western Ghats at high altitudes.

## Endemic Species
Species found only in a specific region and nowhere else in the world.

## Wildlife Corridor
Protected route connecting wildlife habitats for animal movement.

## Tiger Reserve
Protected area specifically designated for tiger conservation under Project Tiger."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Ecological Importance
- **Biodiversity Conservation**: Home to endemic species
- **Water Resources**: Catchment for rivers
- **Carbon Sequestration**: Climate regulation

## Economic Importance
- **Non-timber Products**: Honey, bamboo, medicinal plants
- **Tourism**: Revenue generation
- **Employment**: Forest-based livelihoods

## Cultural Importance
- Sacred groves in villages
- Traditional forest knowledge
- Part of Kerala's identity"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Kerala's forests are part of the Western Ghats biodiversity hotspot:

- **Forest cover**: About 23% of state's area
- **Protected areas**: Multiple wildlife sanctuaries and national parks
- **Endemic species**: Lion-tailed Macaque, Neelakurinji
- **Ecotourism**: Periyar, Wayanad, Silent Valley"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What percentage of Kerala is covered by forests?', 'difficulty': 'easy', 'choices': [
                {'text': 'About 23%', 'is_correct': True},
                {'text': 'About 10%', 'is_correct': False},
                {'text': 'About 40%', 'is_correct': False},
                {'text': 'About 50%', 'is_correct': False}
            ]},
            {'question': 'Which national park in Kerala is known for the Nilgiri Tahr?', 'difficulty': 'easy', 'choices': [
                {'text': 'Eravikulam National Park', 'is_correct': True},
                {'text': 'Silent Valley National Park', 'is_correct': False},
                {'text': 'Periyar National Park', 'is_correct': False},
                {'text': 'Wayanad Wildlife Sanctuary', 'is_correct': False}
            ]},
            {'question': 'What is the rare primate found only in Kerala\'s rainforests?', 'difficulty': 'easy', 'choices': [
                {'text': 'Lion-tailed Macaque', 'is_correct': True},
                {'text': 'Bonnet Macaque', 'is_correct': False},
                {'text': 'Hanuman Langur', 'is_correct': False},
                {'text': 'Gibbon', 'is_correct': False}
            ]},
            {'question': 'How often does Neelakurinji bloom?', 'difficulty': 'medium', 'choices': [
                {'text': 'Every 12 years', 'is_correct': True},
                {'text': 'Every year', 'is_correct': False},
                {'text': 'Every 5 years', 'is_correct': False},
                {'text': 'Every 20 years', 'is_correct': False}
            ]},
            {'question': 'Which is the largest wildlife sanctuary in Kerala?', 'difficulty': 'medium', 'choices': [
                {'text': 'Wayanad Wildlife Sanctuary', 'is_correct': True},
                {'text': 'Periyar Tiger Reserve', 'is_correct': False},
                {'text': 'Silent Valley National Park', 'is_correct': False},
                {'text': 'Neyyar Wildlife Sanctuary', 'is_correct': False}
            ]},
            {'question': 'What type of forest is Silent Valley known for?', 'difficulty': 'medium', 'choices': [
                {'text': 'Tropical rainforests', 'is_correct': True},
                {'text': 'Deciduous forests', 'is_correct': False},
                {'text': 'Mangrove forests', 'is_correct': False},
                {'text': 'Montane grasslands', 'is_correct': False}
            ]},
            {'question': 'The Western Ghats in Kerala is recognized as what?', 'difficulty': 'hard', 'choices': [
                {'text': 'UNESCO World Heritage Site', 'is_correct': True},
                {'text': 'Tiger Reserve', 'is_correct': False},
                {'text': 'Biosphere Reserve', 'is_correct': False},
                {'text': 'National Park', 'is_correct': False}
            ]},
            {'question': 'What are Shola forests?', 'difficulty': 'hard', 'choices': [
                {'text': 'Tropical montane forests at high altitudes', 'is_correct': True},
                {'text': 'Coastal mangrove forests', 'is_correct': False},
                {'text': 'Riverine forests along backwaters', 'is_correct': False},
                {'text': 'Dry deciduous forests', 'is_correct': False}
            ]},
            {'question': 'Which bird is found in Kerala\'s forests and known for its large beak?', 'difficulty': 'hard', 'choices': [
                {'text': 'Great Indian Hornbill', 'is_correct': True},
                {'text': 'Peacock', 'is_correct': False},
                {'text': 'Parrot', 'is_correct': False},
                {'text': 'Woodpecker', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # FORT KOCHI CONTENT
    # ========================================
    def add_fort_kochi_content(self, topic, section):
        content = """# Introduction & Overview

**Fort Kochi** is a historic gem on the shores of the Arabian Sea. Walking through its narrow lanes is like traveling back in time, where you encounter a unique blend of Portuguese, Dutch, British, and local Kerala influences.

## Key Highlights
- **Colonial Echoes**: Home to the oldest European church in India (St. Francis Church) and Jewish heritage sites.
- **Iconic Vistas**: Famous for the "Cheenavalai" (Chinese Fishing Nets) that dot the shoreline.
- **Art Hub**: Today, it is the center of the world-renowned Kochi-Muziris Biennale."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/fort_kochi_port.png')
        
        content = """# Background / Formation

## Historical Timeline
- **1503**: Portuguese build first fort in India
- **1663**: Dutch capture and develop the area
- **1795**: British take control
- **1947**: Independence of India

## Colonial Powers
### Portuguese Era
- First Europeans to trade
- Built St. Francis Church
- Introduced Christianity

### Dutch Era
- Built Dutch Palace
- Developed Jew Street
- Established spice trade"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Landmarks
### St. Francis Church (1503)
- Oldest European church in India
- Built by Portuguese

### Chinese Fishing Nets
- Introduced by Chinese traders
- Still used by fishermen
- Iconic sunset view

### Indo-Portuguese Museum
- Cultural artifacts"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Cultural Quarters
- **Jew Street**: Antiques and spices
- **Mattancherry**: Dutch Palace area

## Modern Attractions
- **Kochi-Muziris Biennale**: International art exhibition
- **Kochi Maritime Museum**: Naval history"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Fort Kochi
The historic old town area of Kochi known for its colonial architecture.

## Cheenavalai
The local name for Chinese fishing nets in Malayalam.

## Mattancherry
Area near Fort Kochi known for the Dutch Palace and Jewish Quarter.

## Kochi-Muziris Biennale
International contemporary art exhibition held in Kochi every two years."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Historical Importance
- First European contact in India
- Trade hub for spices
- Colonial architectural heritage

## Cultural Importance
- Multi-cultural coexistence
- Art and literary tradition
- Culinary heritage"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Fort Kochi represents Kerala's colonial history:

- **1503**: First European fort built in India
- **Landmarks**: St. Francis Church, Chinese fishing nets
- **Cultural fusion**: Portuguese, Dutch, Jewish, Chinese influences"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'In which year was Fort Kochi established by the Portuguese?', 'difficulty': 'easy', 'choices': [
                {'text': '1503', 'is_correct': True},
                {'text': '1600', 'is_correct': False},
                {'text': '1498', 'is_correct': False},
                {'text': '1550', 'is_correct': False}
            ]},
            {'question': 'Which is the oldest European church in India located in Fort Kochi?', 'difficulty': 'easy', 'choices': [
                {'text': 'St. Francis Church', 'is_correct': True},
                {'text': 'Santa Cruz Basilica', 'is_correct': False},
                {'text': 'St. Thomas Church', 'is_correct': False},
                {'text': 'St. George Church', 'is_correct': False}
            ]},
            {'question': 'What are Chinese fishing nets called in Malayalam?', 'difficulty': 'easy', 'choices': [
                {'text': 'Cheenavalai', 'is_correct': True},
                {'text': 'Vallam', 'is_correct': False},
                {'text': 'Kettuvallam', 'is_correct': False},
                {'text': 'Charam', 'is_correct': False}
            ]},
            {'question': 'Which colonial power captured Kochi in 1663?', 'difficulty': 'medium', 'choices': [
                {'text': 'Dutch', 'is_correct': True},
                {'text': 'Portuguese', 'is_correct': False},
                {'text': 'British', 'is_correct': False},
                {'text': 'French', 'is_correct': False}
            ]},
            {'question': 'What is the Kochi-Muziris Biennale?', 'difficulty': 'medium', 'choices': [
                {'text': 'International art exhibition', 'is_correct': True},
                {'text': 'Music festival', 'is_correct': False},
                {'text': 'Food festival', 'is_correct': False},
                {'text': 'Trade fair', 'is_correct': False}
            ]},
            {'question': 'In which area of Fort Kochi can you find the Dutch Palace?', 'difficulty': 'medium', 'choices': [
                {'text': 'Mattancherry', 'is_correct': True},
                {'text': 'Princess Street', 'is_correct': False},
                {'text': 'Jew Street', 'is_correct': False},
                {'text': 'Marine Drive', 'is_correct': False}
            ]},
            {'question': 'Who is buried in St. Francis Church in Fort Kochi?', 'difficulty': 'hard', 'choices': [
                {'text': 'Samoothiri Ravi Varma', 'is_correct': True},
                {'text': 'Mahatma Gandhi', 'is_correct': False},
                {'text': 'Vasco da Gama', 'is_correct': False},
                {'text': 'Tipu Sultan', 'is_correct': False}
            ]},
            {'question': 'What was Kochi known for in ancient trade?', 'difficulty': 'hard', 'choices': [
                {'text': 'Spice trade', 'is_correct': True},
                {'text': 'Silk trade', 'is_correct': False},
                {'text': 'Gold trade', 'is_correct': False},
                {'text': 'Cotton trade', 'is_correct': False}
            ]},
            {'question': 'Which community settled in the Jew Street area of Kochi?', 'difficulty': 'hard', 'choices': [
                {'text': 'Jewish community', 'is_correct': True},
                {'text': 'Chinese community', 'is_correct': False},
                {'text': 'Arab community', 'is_correct': False},
                {'text': 'British community', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # PADMANABHAPURAM PALACE CONTENT
    # ========================================
    def add_padmanabhapuram_content(self, topic, section):
        content = """# Introduction & Overview

**Padmanabhapuram Palace** is an architectural marvel. It is the largest wooden palace in Asia and a masterpiece of traditional Kerala craftsmanship, known for its intricate wood carvings and elegant simplicity.

## Key Highlights
- **The Construction**: Built entirely of wood (teak and rosewood) without the use of a single iron nail!
- **Royal Legacy**: It served as the capital of the Travancore kingdom until the late 18th century.
- **Aesthetic Brilliance**: Features stunning mural paintings and a floor made of a secret mixture of ingredients like egg white and burnt coconut shells."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/padman_palace_interior.png')
        
        content = """# Background / Formation

## Historical Background
- Built in **16th century** (around 1550 AD)
- Served as residence of Travancore rulers
- Capital of Venad kingdom before Thiruvananthapuram
- Remained royal residence until 1795

## Notable Rulers
- **Marthanda Varma** (1729-1758): Founded modern Travancore"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Architecture
- Entirely made of wood (teak, rosewood, coconut)
- No nails used - only wooden pins
- Beautiful murals
- Unique ventilation system

## Palace Sections
- **Mantrasala**: King's council chamber
- **Nalukettu**: Four-hall traditional structure
- **Theppakavu**: Boat house"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Murals
- Scenes from Ramayana and Mahabharata
- Portraits of kings and queens
- Nature and floral designs
- Some over 400 years old

## Notable Halls
- **Thiruvathira Dance Hall**: Perfect acoustics
- **Royal Bedchamber**: Ivory decorations"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Nalukettu
Traditional Kerala architectural style with four halls surrounding a central courtyard.

## Mantrasala
The king's council chamber where official meetings were held.

## ASI
Archaeological Survey of India - the agency that maintains the palace."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Architectural Importance
- Finest example of Kerala wooden architecture
- Preserved traditional craftsmanship

## Historical Importance
- Witnessed Travancore's rise
- Center of royal power"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Padmanabhapuram Palace is a masterpiece of Kerala architecture:

- **Built**: Around 1550 AD
- **Material**: Entirely wooden (no nails)
- **Notable**: 400+ year old murals
- **Preserved by**: Archaeological Survey of India"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'In which century was Padmanabhapuram Palace built?', 'difficulty': 'easy', 'choices': [
                {'text': '16th century', 'is_correct': True},
                {'text': '18th century', 'is_correct': False},
                {'text': '15th century', 'is_correct': False},
                {'text': '17th century', 'is_correct': False}
            ]},
            {'question': 'Which material was used to build Padmanabhapuram Palace?', 'difficulty': 'easy', 'choices': [
                {'text': 'Wood', 'is_correct': True},
                {'text': 'Stone', 'is_correct': False},
                {'text': 'Brick', 'is_correct': False},
                {'text': 'Marble', 'is_correct': False}
            ]},
            {'question': 'Are nails used in the construction of Padmanabhapuram Palace?', 'difficulty': 'easy', 'choices': [
                {'text': 'No, only wooden pins', 'is_correct': True},
                {'text': 'Yes, iron nails', 'is_correct': False},
                {'text': 'Yes, brass nails', 'is_correct': False},
                {'text': 'No information available', 'is_correct': False}
            ]},
            {'question': 'Who maintained Padmanabhapuram Palace after the royal family moved?', 'difficulty': 'medium', 'choices': [
                {'text': 'Archaeological Survey of India', 'is_correct': True},
                {'text': 'Tamil Nadu government', 'is_correct': False},
                {'text': 'Kerala government', 'is_correct': False},
                {'text': 'Travancore royal family', 'is_correct': False}
            ]},
            {'question': 'What is the famous hall in Padmanabhapuram known for perfect acoustics?', 'difficulty': 'medium', 'choices': [
                {'text': 'Thiruvathira Dance Hall', 'is_correct': True},
                {'text': 'Mantrasala', 'is_correct': False},
                {'text': 'Royal Bedchamber', 'is_correct': False},
                {'text': 'Weapon Room', 'is_correct': False}
            ]},
            {'question': 'Which rulers used Padmanabhapuram as their residence?', 'difficulty': 'medium', 'choices': [
                {'text': 'Travancore rulers', 'is_correct': True},
                {'text': 'Dutch colonizers', 'is_correct': False},
                {'text': 'British administrators', 'is_correct': False},
                {'text': 'Vijayanagara kings', 'is_correct': False}
            ]},
            {'question': 'The murals in Padmanabhapuram Palace depict stories from which texts?', 'difficulty': 'hard', 'choices': [
                {'text': 'Ramayana and Mahabharata', 'is_correct': True},
                {'text': 'Bible and Quran', 'is_correct': False},
                {'text': 'Vedas only', 'is_correct': False},
                {'text': 'Puranas only', 'is_correct': False}
            ]},
            {'question': 'How old are some of the murals in Padmanabhapuram Palace?', 'difficulty': 'hard', 'choices': [
                {'text': 'Over 400 years old', 'is_correct': True},
                {'text': 'About 100 years old', 'is_correct': False},
                {'text': 'About 200 years old', 'is_correct': False},
                {'text': 'About 50 years old', 'is_correct': False}
            ]},
            {'question': 'Where is Padmanabhapuram Palace located now?', 'difficulty': 'hard', 'choices': [
                {'text': 'Kanyakumari district, Tamil Nadu', 'is_correct': True},
                {'text': 'Thiruvananthapuram, Kerala', 'is_correct': False},
                {'text': 'Kollam district, Kerala', 'is_correct': False},
                {'text': 'Kanyakumari district, Kerala', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # BEKAL FORT CONTENT
    # ========================================
    def add_bekal_fort_content(self, topic, section):
        content = """# Introduction & Overview

**Bekal Fort** is the largest and best-preserved fort in Kerala. Spreading over 40 acres, its massive laterite walls rise directly from the Arabian Sea, offering a breathtaking view of the coastline and a journey into the military history of the region.

## Key Highlights
- **Strategic Location**: Built by Shivappa Nayaka in the 17th century for coastal surveillance and defense.
- **Unique Architecture**: Features observation towers, zigzag entrances, and secret tunnels.
- **Cinematic Beauty**: One of the most photographed locations in Kerala, famous for its sunset views and beach."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/bekal_fort_walls.png')
        
        content = """# Background / Formation

## Construction
- Built by **Shivappa Nayaka** of Keladi Nayaka dynasty
- Built in the **17th century**
- Originally constructed as defense outpost
- Later modified by British

## Historical Significance
- Key defense position
- Protected trade routes
- Sea view for surveillance
- Underground tunnels"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Architecture
- Built using **laterite stones**
- Massive walls rising from sea
- Observation towers
- Secret tunnels
- Storehouses

## Structures
- Multiple observation towers
- Strategic vantage points
- Underground passages
- Fort walls (30-40 feet high)"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Features
- **Observation Towers**: For watching enemy ships
- **Secret Tunnels**: Escape routes
- **Storehouses**: For weapons and supplies
- **Beach**: Popular tourist spot

## Cultural Impact
- Featured in movie "Kamal" (1994)
- Symbol of Kerala's martial tradition
- Important archaeological site"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Laterite Stone
A type of rock used in construction, known for its reddish-brown color and durability.

## Keladi Nayaka
The dynasty that ruled parts of Karnataka and Kerala in the 17th century.

## ASI
Archaeological Survey of India - the body that maintains Bekal Fort."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Historical Importance
- Largest fort in Kerala
- Strategic defense location
- Archaeological significance

## Tourism Importance
- Major tourist destination
- Sunrise/sunset point
- Film location
- Photography destination"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Bekal Fort is Kerala's largest and most impressive fort:

- **Built**: 17th century by Shivappa Nayaka
- **Size**: 40 acres
- **Material**: Laterite stone
- **Features**: Observation towers, secret tunnels"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'Which is the largest fort in Kerala?', 'difficulty': 'easy', 'choices': [
                {'text': 'Bekal Fort', 'is_correct': True},
                {'text': 'Fort Kochi', 'is_correct': False},
                {'text': 'Padmanabhapuram Palace', 'is_correct': False},
                {'text': 'Koyikkal Palace', 'is_correct': False}
            ]},
            {'question': 'In which district is Bekal Fort located?', 'difficulty': 'easy', 'choices': [
                {'text': 'Kasaragod', 'is_correct': True},
                {'text': 'Kannur', 'is_correct': False},
                {'text': 'Kollam', 'is_correct': False},
                {'text': 'Thiruvananthapuram', 'is_correct': False}
            ]},
            {'question': 'By whom was Bekal Fort built?', 'difficulty': 'easy', 'choices': [
                {'text': 'Shivappa Nayaka', 'is_correct': True},
                {'text': 'Vijayanagara kings', 'is_correct': False},
                {'text': 'Portuguese', 'is_correct': False},
                {'text': 'Dutch', 'is_correct': False}
            ]},
            {'question': 'What is the area covered by Bekal Fort?', 'difficulty': 'medium', 'choices': [
                {'text': '40 acres', 'is_correct': True},
                {'text': '20 acres', 'is_correct': False},
                {'text': '60 acres', 'is_correct': False},
                {'text': '100 acres', 'is_correct': False}
            ]},
            {'question': 'Which material is used in Bekal Fort construction?', 'difficulty': 'medium', 'choices': [
                {'text': 'Laterite stone', 'is_correct': True},
                {'text': 'Granite', 'is_correct': False},
                {'text': 'Marble', 'is_correct': False},
                {'text': 'Sandstone', 'is_correct': False}
            ]},
            {'question': 'In which century was Bekal Fort built?', 'difficulty': 'medium', 'choices': [
                {'text': '17th century', 'is_correct': True},
                {'text': '16th century', 'is_correct': False},
                {'text': '18th century', 'is_correct': False},
                {'text': '15th century', 'is_correct': False}
            ]},
            {'question': 'What is unique about Bekal Fort\'s location?', 'difficulty': 'hard', 'choices': [
                {'text': 'It rises directly from the Arabian Sea', 'is_correct': True},
                {'text': 'It is built on a hilltop', 'is_correct': False},
                {'text': 'It is surrounded by three rivers', 'is_correct': False},
                {'text': 'It is located on an island', 'is_correct': False}
            ]},
            {'question': 'How many observation towers does Bekal Fort have?', 'difficulty': 'hard', 'choices': [
                {'text': 'Multiple', 'is_correct': True},
                {'text': 'One', 'is_correct': False},
                {'text': 'None', 'is_correct': False},
                {'text': 'Five', 'is_correct': False}
            ]},
            {'question': 'Which movie featured Bekal Fort?', 'difficulty': 'hard', 'choices': [
                {'text': 'Kamal (1994)', 'is_correct': True},
                {'text': 'Moothon', 'is_correct': False},
                {'text': 'Bangalore Days', 'is_correct': False},
                {'text': 'Drishyam', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # PADMANABHASWAMY TEMPLE CONTENT
    # ========================================
    def add_padmanabhaswamy_content(self, topic, section):
        content = """# Introduction & Overview

The **Sree Padmanabhaswamy Temple** is a spiritual and architectural landmark in Thiruvananthapuram. It is famous not only for its religious significance but also as the richest temple in the world, following the discovery of its ancient vaults.

## Key Highlights
- **Grand Architecture**: A stunning blend of Kerala and Dravidian styles, featuring a massive 100-foot tall gopuram.
- **The Deity**: Dedicated to Lord Vishnu, who is depicted in the "Anantha Shayanam" (eternal sleep) posture on the serpent Anantha.
- **Royal Patronage**: The temple has been maintained for centuries by the Travancore Royal Family, who consider themselves the "Sree Padmanabha Dasas" (servants of the Lord)."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/padman_temple_mural.png')
        
        content = """# Background / Formation

## Historical Background
- Built during reign of **Maharaja Marthanda Varma**
- **16th century** construction
- Renovated by **Swanthan Marthanda Varma**
- Temple has ancient origins dating to 8th century"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Main Deity
- **Lord Padmanabhaswamy** (Vishnu)
- Lord Vishnu in reclining pose on Anantha
- 18-foot long idol
- Made of Kudappanakunji stones

## Temple Complex
- 7-tiered structure
- 100 feet tall gopuram
- 18 ornate doors
- Golden court (Velliambalam)"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Temple Tanks
- **Krishna Kund**: Sacred bathing tank
- Steps leading to the temple

## Festivals
- **Navaratri**: Nine-night festival
- **Arattu**: Sacred bathing ceremony"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Padmanabhaswamy
Lord Vishnu in his form as "one with lotus (padma) in his navel (nabha)"

## Anantha
The cosmic serpent on which Lord Vishnu reclines

## Gopuram
The monumental tower at the temple entrance"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Religious Importance
- One of 108 Divya Desams (holy temples)
- Important Vaishnavite pilgrimage site
- Associated with Lord Vishnu

## Economic Importance
- World's richest temple
- Tourism revenue"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Sree Padmanabhaswamy Temple is a symbol of Kerala's rich heritage:

- **Built**: 16th century
- **Deity**: Lord Vishnu
- **Treasure**: Discovered in 2011, worth billions
- **Style**: Dravidian architecture"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'To whom is Padmanabhaswamy Temple dedicated?', 'difficulty': 'easy', 'choices': [
                {'text': 'Lord Vishnu', 'is_correct': True},
                {'text': 'Lord Shiva', 'is_correct': False},
                {'text': 'Lord Krishna', 'is_correct': False},
                {'text': 'Lord Ganapati', 'is_correct': False}
            ]},
            {'question': 'In which city is Padmanabhaswamy Temple located?', 'difficulty': 'easy', 'choices': [
                {'text': 'Thiruvananthapuram', 'is_correct': True},
                {'text': 'Kochi', 'is_correct': False},
                {'text': 'Kollam', 'is_correct': False},
                {'text': 'Kottayam', 'is_correct': False}
            ]},
            {'question': 'When was the massive treasure at Padmanabhaswamy Temple discovered?', 'difficulty': 'easy', 'choices': [
                {'text': '2011', 'is_correct': True},
                {'text': '2010', 'is_correct': False},
                {'text': '2005', 'is_correct': False},
                {'text': '2015', 'is_correct': False}
            ]},
            {'question': 'What is the estimated value of the treasure found in Padmanabhaswamy Temple?', 'difficulty': 'medium', 'choices': [
                {'text': '$22 billion', 'is_correct': True},
                {'text': '$1 billion', 'is_correct': False},
                {'text': '$5 billion', 'is_correct': False},
                {'text': '$10 billion', 'is_correct': False}
            ]},
            {'question': 'What architectural style is used in Padmanabhaswamy Temple?', 'difficulty': 'medium', 'choices': [
                {'text': 'Dravidian', 'is_correct': True},
                {'text': 'Indo-Saracenic', 'is_correct': False},
                {'text': 'Mughal', 'is_correct': False},
                {'text': 'Gothic', 'is_correct': False}
            ]},
            {'question': 'What is the height of the gopuram at Padmanabhaswamy Temple?', 'difficulty': 'medium', 'choices': [
                {'text': '100 feet', 'is_correct': True},
                {'text': '50 feet', 'is_correct': False},
                {'text': '150 feet', 'is_correct': False},
                {'text': '75 feet', 'is_correct': False}
            ]},
            {'question': 'Padmanabhaswamy Temple is one of how many Divya Desams?', 'difficulty': 'hard', 'choices': [
                {'text': '108', 'is_correct': True},
                {'text': '50', 'is_correct': False},
                {'text': '200', 'is_correct': False},
                {'text': '75', 'is_correct': False}
            ]},
            {'question': 'On which serpent is Lord Vishnu depicted in Padmanabhaswamy Temple?', 'difficulty': 'hard', 'choices': [
                {'text': 'Anantha', 'is_correct': True},
                {'text': 'Vasuki', 'is_correct': False},
                {'text': 'Shesha', 'is_correct': False},
                {'text': 'Takshaka', 'is_correct': False}
            ]},
            {'question': 'What is the name of the golden hall inside Padmanabhaswamy Temple?', 'difficulty': 'hard', 'choices': [
                {'text': 'Velliambalam', 'is_correct': True},
                {'text': 'Mantrasala', 'is_correct': False},
                {'text': 'Kilmana', 'is_correct': False},
                {'text': 'Nalukettu', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # HILL PALACE CONTENT
    # ========================================
    def add_hill_palace_content(self, topic, section):
        content = """# Introduction & Overview

The **Hill Palace Museum** in Tripunithura is the largest archaeological museum in Kerala. Once the official residence of the Kochi Royal Family, it now stands as a vast heritage complex housing treasures from our royal past.

## Key Highlights
- **Royal Residence**: Built in 1865, the complex originally consisted of 49 buildings in the traditional-colonial style.
- **Heritage Collection**: Houses the royal throne, the diamond-studded crown, and an extensive collection of ancient coins and weapons.
- **Ecosystem**: The palace grounds also feature a deer park and a medicinal plant garden, preserving the natural heritage alongside the historical."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/hill_palace_museum.png')
        
        content = """# Background / Formation

## Historical Background
- Built in **1865** (traditional date)
- Official residence of Cochin royal family
- British-style architecture
- Abandoned after 1970s
- Converted to museum in 1980"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Architecture
- British-style mansion
- 49 original buildings
- Sprawling courtyard
- Traditional Kerala elements

## Collections
- **Antiques**: Furniture, utensils
- **Coins**: Ancient and medieval
- **Weapons**: Swords, daggers
- **Paintings**: Traditional art"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Main Attractions
- **Crown**: Maharaja's ceremonial crown
- **Throne**: Ancient royal throne
- **Weapons Gallery**: Historical arms
- **Epigraphy**: Stone inscriptions"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Hill Palace
The official residence of the Cochin royal family, built in the 19th century.

## Archaeological Museum
A museum displaying ancient artifacts, inscriptions, and historical objects."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Historical Importance
- Preserves Cochin royal heritage
- Evidence of ancient civilization

## Cultural Importance
- Showcases Kerala's past
- Educational value"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Hill Palace Museum is Kerala's window to its royal past:

- **Built**: 1865
- **Type**: Largest archaeological museum in Kerala
- **Original buildings**: 49"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What is Hill Palace known as in Kerala?', 'difficulty': 'easy', 'choices': [
                {'text': 'Largest archaeological museum', 'is_correct': True},
                {'text': 'Oldest temple', 'is_correct': False},
                {'text': 'Biggest fort', 'is_correct': False},
                {'text': 'Highest point', 'is_correct': False}
            ]},
            {'question': 'In which district is Hill Palace located?', 'difficulty': 'easy', 'choices': [
                {'text': 'Ernakulam', 'is_correct': True},
                {'text': 'Thiruvananthapuram', 'is_correct': False},
                {'text': 'Kollam', 'is_correct': False},
                {'text': 'Kottayam', 'is_correct': False}
            ]},
            {'question': 'How many buildings were there in the original Hill Palace complex?', 'difficulty': 'easy', 'choices': [
                {'text': '49', 'is_correct': True},
                {'text': '29', 'is_correct': False},
                {'text': '69', 'is_correct': False},
                {'text': '39', 'is_correct': False}
            ]},
            {'question': 'When was Hill Palace built?', 'difficulty': 'medium', 'choices': [
                {'text': '1865', 'is_correct': True},
                {'text': '1800', 'is_correct': False},
                {'text': '1900', 'is_correct': False},
                {'text': '1850', 'is_correct': False}
            ]},
            {'question': 'To which royal family did Hill Palace belong?', 'difficulty': 'medium', 'choices': [
                {'text': 'Cochin', 'is_correct': True},
                {'text': 'Travancore', 'is_correct': False},
                {'text': 'Malabar', 'is_correct': False},
                {'text': 'Kochi', 'is_correct': False}
            ]},
            {'question': 'In which year was Hill Palace converted into a museum?', 'difficulty': 'medium', 'choices': [
                {'text': '1980', 'is_correct': True},
                {'text': '1970', 'is_correct': False},
                {'text': '1990', 'is_correct': False},
                {'text': '1985', 'is_correct': False}
            ]},
            {'question': 'What is numismatics the study of?', 'difficulty': 'hard', 'choices': [
                {'text': 'Coins', 'is_correct': True},
                {'text': 'Rocks', 'is_correct': False},
                {'text': 'Plants', 'is_correct': False},
                {'text': 'Animals', 'is_correct': False}
            ]},
            {'question': 'Which type of artifacts can be found in Hill Palace Museum?', 'difficulty': 'hard', 'choices': [
                {'text': 'All of the above', 'is_correct': True},
                {'text': 'Only coins', 'is_correct': False},
                {'text': 'Only weapons', 'is_correct': False},
                {'text': 'Only paintings', 'is_correct': False}
            ]},
            {'question': 'What architectural style was used in Hill Palace?', 'difficulty': 'hard', 'choices': [
                {'text': 'British-style with Kerala elements', 'is_correct': True},
                {'text': 'Purely Mughal', 'is_correct': False},
                {'text': 'Temple style', 'is_correct': False},
                {'text': 'Buddhist', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KOYIKKAL PALACE CONTENT
    # ========================================
    def add_koyikkal_palace_content(self, topic, section):
        content = """# Introduction & Overview

**Koyikkal Palace** is more than just a royal residence; it is a time capsule of Kerala's folk traditions. Located in Nedumangad, this 16th-century palace is a beautiful example of the traditional 'Nalukettu' architectural style.

## Key Highlights
- **Folklore Museum**: It houses a rare collection of folk artifacts, musical instruments, and ritual objects used in ancient Kerala.
- **The Architecture**: Known for its gabled roofs and central courtyard that provide natural ventilation—a hallmark of Kerala design.
- **Historical Significance**: Built for the Umayamma Rani of the Venad Royal Family, it tells stories of a bygone era of regional power."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/koyikkal_palace.png')
        
        content = """# Background / Formation

## Historical Background
- Built during **Medieval period**
- Belonged to **Kumaraswamy Pillai**
- Later belonged to **Kottayam Raja**
- Traditional architectural style"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Palace Structure
- Two-storied building
- Central courtyard
- Traditional rooms
- Wooden carvings

## Museum Collections
- **Folk artifacts**: Traditional items
- **Musical instruments**: Kerala folk
- **Costumes**: Traditional dresses"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Folklore Museum
- Largest in Kerala
- 18th-19th century artifacts
- Traditional Kerala items"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Koyikkal Palace
A 16th-century palace near Kottayam, now a folklore museum.

## Nalukettu
Traditional Kerala house with four halls around a central courtyard."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Historical Importance
- Preserves medieval heritage
- Architectural significance

## Cultural Importance
- Folklore preservation
- Educational value"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Koyikkal Palace showcases Kerala's folk heritage:

- **Built**: 16th century
- **Location**: Near Kottayam
- **Type**: Folklore museum"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What is special about Koyikkal Palace?', 'difficulty': 'easy', 'choices': [
                {'text': 'It has the largest folklore museum in Kerala', 'is_correct': True},
                {'text': 'It is the oldest temple', 'is_correct': False},
                {'text': 'It is the biggest fort', 'is_correct': False},
                {'text': 'It is the highest palace', 'is_correct': False}
            ]},
            {'question': 'In which district is Koyikkal Palace located?', 'difficulty': 'easy', 'choices': [
                {'text': 'Kottayam', 'is_correct': True},
                {'text': 'Ernakulam', 'is_correct': False},
                {'text': 'Thiruvananthapuram', 'is_correct': False},
                {'text': 'Kollam', 'is_correct': False}
            ]},
            {'question': 'In which century was Koyikkal Palace built?', 'difficulty': 'easy', 'choices': [
                {'text': '16th century', 'is_correct': True},
                {'text': '18th century', 'is_correct': False},
                {'text': '15th century', 'is_correct': False},
                {'text': '19th century', 'is_correct': False}
            ]},
            {'question': 'What architectural style is used in Koyikkal Palace?', 'difficulty': 'medium', 'choices': [
                {'text': 'Nalukettu', 'is_correct': True},
                {'text': 'Mughal', 'is_correct': False},
                {'text': 'Gothic', 'is_correct': False},
                {'text': 'Dravidian', 'is_correct': False}
            ]},
            {'question': 'What type of museum is in Koyikkal Palace?', 'difficulty': 'medium', 'choices': [
                {'text': 'Folklore museum', 'is_correct': True},
                {'text': 'Science museum', 'is_correct': False},
                {'text': 'Art museum', 'is_correct': False},
                {'text': 'Military museum', 'is_correct': False}
            ]},
            {'question': 'To whom did Koyikkal Palace originally belong?', 'difficulty': 'medium', 'choices': [
                {'text': 'Kumaraswamy Pillai', 'is_correct': True},
                {'text': 'Maharaja', 'is_correct': False},
                {'text': 'British', 'is_correct': False},
                {'text': 'Portuguese', 'is_correct': False}
            ]},
            {'question': 'What is nalukettu?', 'difficulty': 'hard', 'choices': [
                {'text': 'Traditional house with four halls around courtyard', 'is_correct': True},
                {'text': 'A type of temple', 'is_correct': False},
                {'text': 'A type of palace', 'is_correct': False},
                {'text': 'A garden', 'is_correct': False}
            ]},
            {'question': 'How many stories does Koyikkal Palace have?', 'difficulty': 'hard', 'choices': [
                {'text': 'Two', 'is_correct': True},
                {'text': 'One', 'is_correct': False},
                {'text': 'Three', 'is_correct': False},
                {'text': 'Four', 'is_correct': False}
            ]},
            {'question': 'What type of items are displayed in the Koyikkal Palace museum?', 'difficulty': 'hard', 'choices': [
                {'text': 'Folk artifacts and traditional items', 'is_correct': True},
                {'text': 'Modern art', 'is_correct': False},
                {'text': 'Space equipment', 'is_correct': False},
                {'text': 'Electronic devices', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KRISHNAPURAM PALACE CONTENT
    # ========================================
    def add_krishnapuram_content(self, topic, section):
        content = """# Introduction & Overview

**Krishnapuram Palace** is a classic Kerala-style palace famous for its stunning mural paintings. Built in the 18th century by the Travancore kings, it perfectly blends the aesthetics of a royal home with the spiritual energy of its art.

## Key Highlights
- **The Great Mural**: Home to the *Gajendra Moksham*, the largest single piece of mural painting discovered so far in Kerala.
- **Architectural Style**: Features the characteristic gabled roofs, narrow corridors, and dormer windows of Kerala's palace architecture.
- **Surrounding Charm**: Nestled in a garden with a variety of medicinal plants, reflecting the holistic lifestyle of ancient Kerala royalty."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/krishnapuram_palace.png')
        
        content = """# Background / Formation

## Historical Background
- Built in **18th century**
- Residence of **Kayamkulam Raja**
- Architectural blend of Kerala and Colonial
- Near Kayamkulam Lake
- Restored by ASI"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Architecture
- Traditional Kerala style
- Two-storied building
- Central courtyard
- Sloping roof
- Laterite walls

## Famous Murals
- **Gajendra Vargasamohanam**: Famous elephant painting
- Scenes from mythology"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Gajendra Vargasamohanam
- Most famous mural
- 154 square feet
- 48 figures depicted"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Krishnapuram Palace
An 18th-century palace in Alappuzha, famous for its mural paintings.

## Gajendra Vargasamohanam
The famous elephant mural in Krishnapuram Palace."""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Artistic Importance
- Rare mural collection
- Historical paintings

## Historical Importance
- Kayamkulam kingdom
- Regional history"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Krishnapuram Palace is a treasure of mural art:

- **Built**: 18th century
- **Location**: Kayamkulam, Alappuzha
- **Famous for**: Mural paintings"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What is Krishnapuram Palace famous for?', 'difficulty': 'easy', 'choices': [
                {'text': 'Mural paintings', 'is_correct': True},
                {'text': 'Temple', 'is_correct': False},
                {'text': 'Garden', 'is_correct': False},
                {'text': 'Fort', 'is_correct': False}
            ]},
            {'question': 'In which district is Krishnapuram Palace located?', 'difficulty': 'easy', 'choices': [
                {'text': 'Alappuzha', 'is_correct': True},
                {'text': 'Kottayam', 'is_correct': False},
                {'text': 'Ernakulam', 'is_correct': False},
                {'text': 'Kollam', 'is_correct': False}
            ]},
            {'question': 'In which century was Krishnapuram Palace built?', 'difficulty': 'easy', 'choices': [
                {'text': '18th century', 'is_correct': True},
                {'text': '16th century', 'is_correct': False},
                {'text': '19th century', 'is_correct': False},
                {'text': '17th century', 'is_correct': False}
            ]},
            {'question': 'What is the most famous mural in Krishnapuram Palace?', 'difficulty': 'medium', 'choices': [
                {'text': 'Gajendra Vargasamohanam', 'is_correct': True},
                {'text': 'Krishnanattam', 'is_correct': False},
                {'text': 'Ramayana', 'is_correct': False},
                {'text': 'Mahabharata', 'is_correct': False}
            ]},
            {'question': 'Who maintains Krishnapuram Palace now?', 'difficulty': 'medium', 'choices': [
                {'text': 'Archaeological Survey of India', 'is_correct': True},
                {'text': 'Kerala Government', 'is_correct': False},
                {'text': 'Private owner', 'is_correct': False},
                {'text': 'Central Government', 'is_correct': False}
            ]},
            {'question': 'To which royal family did Krishnapuram Palace belong?', 'difficulty': 'medium', 'choices': [
                {'text': 'Kayamkulam Raja', 'is_correct': True},
                {'text': 'Cochin Maharaja', 'is_correct': False},
                {'text': 'Travancore King', 'is_correct': False},
                {'text': 'Vijayanagara Emperor', 'is_correct': False}
            ]},
            {'question': 'How many figures are depicted in the Gajendra Vargasamohanam mural?', 'difficulty': 'hard', 'choices': [
                {'text': '48', 'is_correct': True},
                {'text': '24', 'is_correct': False},
                {'text': '36', 'is_correct': False},
                {'text': '12', 'is_correct': False}
            ]},
            {'question': 'What is the size of the Gajendra Vargasamohanam mural?', 'difficulty': 'hard', 'choices': [
                {'text': '154 square feet', 'is_correct': True},
                {'text': '100 square feet', 'is_correct': False},
                {'text': '200 square feet', 'is_correct': False},
                {'text': '50 square feet', 'is_correct': False}
            ]},
            {'question': 'What architectural style is Krishnapuram Palace known for?', 'difficulty': 'hard', 'choices': [
                {'text': 'Traditional Kerala style with sloping roof', 'is_correct': True},
                {'text': 'Mughal style', 'is_correct': False},
                {'text': 'Colonial style only', 'is_correct': False},
                {'text': 'Temple architecture', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # KATHAKALI CONTENT
    # ========================================
    def add_kathakali_content(self, topic, section):
        content = """# Introduction & Overview

**Kathakali** is one of the oldest theater forms in the world. It is a "story-play" (Katha = story, Kali = play) from Kerala that is distinguished by its colorful makeup, costumes, and face masks. 

## Key Highlights
- **Visual Grandeur**: Known for its massive headgear and billowing skirts.
- **Language of Mudras**: The actors do not speak; the story is told through 24 main hand gestures (*Mudras*) and varied facial expressions (*Navarasas*).
- **Musical Accompaniment**: Driven by the powerful beats of the *Chenda* and *Maddalam* drums."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/kathakali_dance.png')

        content = """# Vesham & Costumes

In Kathakali, the makeup and costumes categorize characters into different types (*Vesham*).

## Makeup Types
- **Pacha (Green)**: Represents noble and virtuous characters like Krishna, Rama, or Arjuna.
- **Katti (Knife)**: Represents characters with some vice, like Ravana or Duryodhana (green with red streaks).
- **Tadi (Beard)**:
    - *Chuvanna Tadi (Red Beard)*: Evil and ferocious characters like Dussasana.
    - *Vella Tadi (White Beard)*: Pious characters like Hanuman.
    - *Karutha Tadi (Black Beard)*: Primal characters like forest dwellers.
- **Minukku (Radiant)**: Used for female characters and sages.

## Materials Used
- **Chutti**: A white fence made of rice paste and lime that frames the actor's face.
- **Natural Pigments**: Manayola (yellow), Shathilingam (red), and Kari (black) mixed with coconut oil."""
        self.create_study_material(topic, 'Vesham & Costumes', content, 2)

        content = """# Festival Calendar 2026-2027

Kathakali is integral to temple festivals (*Utsavams*) across Kerala.

## Major Dates
- **Vishu Kathakali Special**: April 14, 2026.
- **Onam Season Performances**: August 20 - August 30, 2026 (Peak on Thiruvonam, Aug 26).
- **Mandalam Season**: November - December 2026 (Many temple performances).
- **Thrissur Pooram Cultural Fest**: April 27, 2026."""
        self.create_study_material(topic, 'Festival Calendar', content, 3)
        
        content = """# Background / Formation

## Origins
- Evolved from **Krishnanattam** (dance drama)
- Developed in **17th century**
- Under royal patronage of King Manavikraman
- Fusion of dance, drama, and music"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Makeup
- Extremely elaborate
- Takes hours to apply
- Types: **Patti**, **Katti**, **Tadi**
- Represents character traits

## Costumes
- Heavy ornamental headgear
- Large skirts
- Intricate jewelry"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Stories
- **Ramayana**: Dasaratha's sons, Sita's abduction
- **Mahabharata**: Kauravas, Pandavas, Krishna
- **Krishnanattam**: Stories of Lord Krishna"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Kathakali
"Story play" - a classical dance-drama from Kerala

## Pacha
Green makeup used for noble characters and deities

## Chenda
Traditional percussion instrument used in Kathakali"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Cultural Importance
- Symbol of Kerala's heritage
- Classical art form
- Religious storytelling

## Global Recognition
- UNESCO heritage
- International performances
- Cultural ambassador"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Kathakali is Kerala's classical dance drama:

- **Origin**: 17th century
- **Style**: Elaborate makeup and costumes
- **Stories**: From Ramayana and Mahabharata"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
            {'question': 'What type of performance is Kathakali?', 'difficulty': 'easy', 'choices': [
                {'text': 'Classical dance-drama', 'is_correct': True},
                {'text': 'Folk dance', 'is_correct': False},
                {'text': 'Solo dance', 'is_correct': False},
                {'text': 'Musical performance', 'is_correct': False}
            ]},
            {'question': 'What is special about Kathakali makeup?', 'difficulty': 'easy', 'choices': [
                {'text': 'It is extremely elaborate', 'is_correct': True},
                {'text': 'No makeup is used', 'is_correct': False},
                {'text': 'Simple makeup', 'is_correct': False},
                {'text': 'Only white makeup', 'is_correct': False}
            ]},
            {'question': 'From which century did Kathakali originate?', 'difficulty': 'easy', 'choices': [
                {'text': '17th century', 'is_correct': True},
                {'text': '15th century', 'is_correct': False},
                {'text': '19th century', 'is_correct': False},
                {'text': '21st century', 'is_correct': False}
            ]},
            {'question': 'What are the main sources of Kathakali stories?', 'difficulty': 'medium', 'choices': [
                {'text': 'Ramayana and Mahabharata', 'is_correct': True},
                {'text': 'Bible and Quran', 'is_correct': False},
                {'text': 'Vedas only', 'is_correct': False},
                {'text': 'Folk tales', 'is_correct': False}
            ]},
            {'question': 'What is the traditional percussion instrument in Kathakali?', 'difficulty': 'medium', 'choices': [
                {'text': 'Chenda', 'is_correct': True},
                {'text': 'Tabla', 'is_correct': False},
                {'text': 'Mridangam', 'is_correct': False},
                {'text': 'Drums', 'is_correct': False}
            ]},
            {'question': 'What does the term Kathakali mean?', 'difficulty': 'medium', 'choices': [
                {'text': 'Story play', 'is_correct': True},
                {'text': 'Dance only', 'is_correct': False},
                {'text': 'Religious song', 'is_correct': False},
                {'text': 'Folk theater', 'is_correct': False}
            ]},
            {'question': 'What is Pacha in Kathakali?', 'difficulty': 'hard', 'choices': [
                {'text': 'Green makeup for noble characters', 'is_correct': True},
                {'text': 'A dance step', 'is_correct': False},
                {'text': 'A musical instrument', 'is_correct': False},
                {'text': 'A costume', 'is_correct': False}
            ]},
            {'question': 'Where was Kathakali originally performed?', 'difficulty': 'hard', 'choices': [
                {'text': 'Temples', 'is_correct': True},
                {'text': 'Theaters', 'is_correct': False},
                {'text': 'Palaces only', 'is_correct': False},
                {'text': 'Schools', 'is_correct': False}
            ]},
            {'question': 'What is a Kalamandalam?', 'difficulty': 'hard', 'choices': [
                {'text': 'Kathakali training school', 'is_correct': True},
                {'text': 'A type of costume', 'is_correct': False},
                {'text': 'A musical instrument', 'is_correct': False},
                {'text': 'A makeup type', 'is_correct': False}
            ]},
        ]
        self.add_quiz_questions(topic, section, quiz_data)

    # ========================================
    # MOHINIYATTAM CONTENT
    # ========================================
    def add_mohiniyattam_content(self, topic, section):
        content = """# Introduction & Overview

**Mohiniyattam**, the "Dance of the Enchantress," is the classical solo dance of Kerala performed exclusively by women. It is characterized by its graceful, swaying movements that resemble the gentle undulation of palm leaves in the breeze.

## Key Highlights
- **Grace and Elegance**: The dance is known for its *Lasya* (feminine and soft) style.
- **Lyrical Quality**: Most performances are set to the *Sopanam* style of music, which is slow and melodic.
- **Visual Simplicity**: Unlike Kathakali's complexity, Mohiniyattam relies on subtle beauty."""
        self.create_study_material(topic, 'Introduction & Overview', content, 1, image_url='static/images/study/mohiniyattam_grace.png')

        content = """# Costumes & Style

The costume of Mohiniyattam is distinctively simple yet remarkably elegant.

## Costume Elements
- **The Saree**: An off-white or white *Kasavu* saree with a rich gold border. It is draped with a fan-like pleat in the front.
- **The Blouse**: Usually matches the saree's color and border.
- **Waist Belt**: A gold belt (*Oddiyanam*) that accentuates the swaying movements.

## Materials & Adornments
- **Gold Jewelry**: Traditional ornaments including the *Jhimiki* (earrings) and *Moola (nose ring)*.
- **Jasmine Flowers**: Worn in the hair, usually tied in a bun on the left side (*Kondakettu*), adding a fragrant and aesthetic touch."""
        self.create_study_material(topic, 'Costumes & Adornments', content, 2)
        
        content = """# Background / Formation

## Origins
- Ancient dance form from Kerala
- Name from **Mohini** (Vishnu's female form)
- Developed in **16th-18th centuries**
- Temple dance traditions"""
        self.create_study_material(topic, 'Background / Formation', content, 2)
        
        content = """# Key Features

## Dance Style
- Gentle swaying movements
- Subtle footwork
- Graceful hand gestures
- Expressive eye movements

## Costumes
- **White/off-white** saree with gold border
- Flowers in hair
- Minimal jewelry"""
        self.create_study_material(topic, 'Key Features', content, 3)
        
        content = """# Important Examples

## Performers
- Kalamandalam Radhadevi
- Shobana
- Usha Natarajan"""
        self.create_study_material(topic, 'Important Examples', content, 4)
        
        content = """# Key Terms

## Mohiniyattam
" Dance of the enchantress" - the classical solo dance of Kerala

## Sopanam
Traditional Kerala style of music used in dance"""
        self.create_study_material(topic, 'Key Terms', content, 5)
        
        content = """# Importance

## Cultural Importance
- Symbol of feminine grace
- Kerala's classical dance
- Temple heritage"""
        self.create_study_material(topic, 'Importance', content, 6)
        
        content = """# Summary

Mohiniyattam is Kerala's graceful classical dance:

- **Origin**: 16th-18th centuries
- **Style**: Gentle, swaying movements
- **Performer**: Women only"""
        self.create_study_material(topic, 'Summary', content, 7)
        
        quiz_data = [
    {'question': 'Mohiniyattam is the classical dance form of which state?', 'difficulty': 'easy', 'choices': [
        {'text': 'Kerala', 'is_correct': True},
        {'text': 'Tamil Nadu', 'is_correct': False},
        {'text': 'Karnataka', 'is_correct': False},
        {'text': 'Andhra Pradesh', 'is_correct': False}
    ]},
    {'question': 'Who traditionally performs Mohiniyattam?', 'difficulty': 'easy', 'choices': [
        {'text': 'Women', 'is_correct': True},
        {'text': 'Men', 'is_correct': False},
        {'text': 'Children', 'is_correct': False},
        {'text': 'Groups only', 'is_correct': False}
    ]},
    {'question': 'What does Mohini mean?', 'difficulty': 'easy', 'choices': [
        {'text': 'Enchantress', 'is_correct': True},
        {'text': 'Warrior', 'is_correct': False},
        {'text': 'Priest', 'is_correct': False},
        {'text': 'Dancer', 'is_correct': False}
    ]},
    {'question': 'Which god is associated with the Mohini form?', 'difficulty': 'medium', 'choices': [
        {'text': 'Vishnu', 'is_correct': True},
        {'text': 'Shiva', 'is_correct': False},
        {'text': 'Krishna', 'is_correct': False},
        {'text': 'Brahma', 'is_correct': False}
    ]},
    {'question': 'What color costume is commonly worn in Mohiniyattam?', 'difficulty': 'medium', 'choices': [
        {'text': 'White with gold border', 'is_correct': True},
        {'text': 'Red', 'is_correct': False},
        {'text': 'Blue', 'is_correct': False},
        {'text': 'Green', 'is_correct': False}
    ]},
    {'question': 'Which music style accompanies Mohiniyattam?', 'difficulty': 'medium', 'choices': [
        {'text': 'Carnatic', 'is_correct': True},
        {'text': 'Hindustani', 'is_correct': False},
        {'text': 'Western', 'is_correct': False},
        {'text': 'Folk only', 'is_correct': False}
    ]},
    {'question': 'Which institution helped revive Mohiniyattam?', 'difficulty': 'hard', 'choices': [
        {'text': 'Kerala Kalamandalam', 'is_correct': True},
        {'text': 'Kalakshetra', 'is_correct': False},
        {'text': 'Natya Academy', 'is_correct': False},
        {'text': 'Dance Institute', 'is_correct': False}
    ]},
    {'question': 'Mohiniyattam emphasizes what kind of movements?', 'difficulty': 'hard', 'choices': [
        {'text': 'Graceful and slow', 'is_correct': True},
        {'text': 'Fast and aggressive', 'is_correct': False},
        {'text': 'Martial movements', 'is_correct': False},
        {'text': 'Jumping steps', 'is_correct': False}
    ]},
    {'question': 'Mohiniyattam developed mainly between which centuries?', 'difficulty': 'hard', 'choices': [
        {'text': '16th–18th centuries', 'is_correct': True},
        {'text': '10th–12th centuries', 'is_correct': False},
        {'text': '19th–20th centuries', 'is_correct': False},
        {'text': '5th–7th centuries', 'is_correct': False}
    ]}
        ]
        self.add_quiz_questions(topic, section, quiz_data)
        
                                                          
