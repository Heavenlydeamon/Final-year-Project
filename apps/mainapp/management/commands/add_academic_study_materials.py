from django.core.management.base import BaseCommand
from django.db import transaction
from mainapp.models import Section, Topic, StudyMaterial, ConceptTag


class Command(BaseCommand):
    help = 'Add structured academic study materials with AI-ready fields for all sections'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting academic study materials creation...'))
        
        # Get or create concept tags
        concept_tags = self._get_or_create_concept_tags()
        
        # Create Environment Section Materials
        self._create_environment_materials(concept_tags)
        
        # Create Heritage Section Materials
        self._create_heritage_materials(concept_tags)
        
        # Create Cultural Section Materials
        self._create_cultural_materials(concept_tags)
        
        self.stdout.write(self.style.SUCCESS('\n=== Academic Study Materials Creation Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Total Study Materials: {StudyMaterial.objects.count()}'))

    def _get_or_create_concept_tags(self):
        """Get or create concept tags for AI recommendations"""
        tags_data = [
            {'name': 'Carbon Cycle', 'description': 'The process of carbon cycling through the atmosphere, biosphere, and geosphere'},
            {'name': 'Biodiversity', 'description': 'The variety of life in a particular habitat or ecosystem'},
            {'name': 'Ecosystem Balance', 'description': 'The equilibrium state where organisms interact with each other and their environment'},
            {'name': 'Wildlife Conservation', 'description': 'Protecting wild animals and their habitats'},
            {'name': 'Climate Change', 'description': 'Long-term changes in global temperature and weather patterns'},
            {'name': 'Sustainable Development', 'description': 'Development that meets present needs without compromising future generations'},
            {'name': 'Environmental Impact', 'description': 'Effects of human activities on the environment'},
            {'name': 'Heritage Preservation', 'description': 'Protecting and maintaining historical and cultural heritage sites'},
            {'name': 'Cultural Artforms', 'description': 'Traditional arts, crafts, and performing arts'},
            {'name': 'Traditional Knowledge', 'description': 'Indigenous knowledge passed down through generations'},
            {'name': 'Historical Sites', 'description': 'Locations of historical significance'},
            {'name': 'Archaeological Heritage', 'description': 'Physical remains of past human activity'},
            {'name': 'Western Ghats', 'description': 'The mountain range along the western side of India'},
            {'name': 'Endemic Species', 'description': 'Species found only in a specific region'},
            {'name': 'Tropical Forest', 'description': 'Forests in tropical regions with high rainfall'},
            {'name': 'Bio-diversity Hotspot', 'description': 'Regions with high biodiversity and conservation importance'},
            {'name': 'Hydrology', 'description': 'Study of water distribution and movement'},
            {'name': 'Conservation', 'description': 'Protection and careful management of natural resources'},
            {'name': 'Greenhouse Effect', 'description': 'Natural warming process enhanced by greenhouse gases'},
            {'name': 'Mitigation', 'description': 'Actions to reduce greenhouse gas emissions'},
            {'name': 'Adaptation', 'description': 'Adjustments to reduce vulnerability to climate impacts'},
            {'name': 'Endangered Species', 'description': 'Species at risk of extinction'},
            {'name': 'Marine Biology', 'description': 'Study of ocean ecosystems and organisms'},
            {'name': 'Colonial History', 'description': 'Historical period of European colonial rule'},
            {'name': 'Architecture', 'description': 'Design and construction of buildings'},
            {'name': 'Performing Arts', 'description': 'Arts performed in real-time by actors'},
            {'name': 'Martial Arts', 'description': 'Traditional fighting techniques and practices'},
            {'name': 'Ritual Traditions', 'description': 'Religious and ceremonial practices'},
            {'name': 'Classical Dance', 'description': 'Traditional formal dance styles'},
        ]
        
        tags = {}
        for tag_data in tags_data:
            tag, _ = ConceptTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'description': tag_data['description']}
            )
            tags[tag_data['name']] = tag
        
        return tags

    def _create_environment_materials(self, concept_tags):
        """Create Environment section study materials with academic format"""
        
        # Get or create Environment section
        env_section, _ = Section.objects.get_or_create(
            name='Environment',
            defaults={
                'description': 'Learn about the environment, climate change, and conservation.',
                'is_general': True
            }
        )
        
        # ========================================
        # WESTERN GHATS - COMPREHENSIVE
        # ========================================
        western_ghats_topic, _ = Topic.objects.get_or_create(
            name='Western Ghats',
            section=env_section,
            defaults={
                'description': 'Explore the biodiversity hotspot of the Western Ghats mountain range.',
                'order': 1
            }
        )
        
        # Clear existing materials
        western_ghats_topic.study_materials.all().delete()
        
        # Module 1: Physical Geography
        sm1 = StudyMaterial.objects.create(
            topic=western_ghats_topic,
            title='The Great Escarpment of India',
            content_text=self._get_western_ghats_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='The Western Ghats is a 1,600 km mountain range forming the western edge of the Deccan Plateau. Known as Sahyadri, it is one of the oldest mountain ranges in the world and serves as a crucial climate barrier.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Kodagu_landscape.jpg/1200px-Kodagu_landscape.jpg',
            order=1
        )
        sm1.concept_tags.add(concept_tags['Western Ghats'], concept_tags['Tropical Forest'], concept_tags['Biodiversity'])
        
        # Module 2: Biodiversity
        sm2 = StudyMaterial.objects.create(
            topic=western_ghats_topic,
            title='A Global Biodiversity Hotspot',
            content_text=self._get_western_ghats_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='The Western Ghats is one of eight global biodiversity hotspots with over 7,000 flowering plant species and numerous endemic wildlife including the Nilgiri Tahr and Lion-tailed Macaque.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Queen_s_Danaine_Butterfly.jpg/800px-Queen_s_Danaine_Butterfly.jpg',
            order=2
        )
        sm2.concept_tags.add(concept_tags['Biodiversity'], concept_tags['Endemic Species'], concept_tags['Bio-diversity Hotspot'], concept_tags['Wildlife Conservation'])
        
        # Module 3: Hydrology
        sm3 = StudyMaterial.objects.create(
            topic=western_ghats_topic,
            title='The Water Tower of South India',
            content_text=self._get_western_ghats_module3(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='The Western Ghats serves as the "Water Tower" of South India, feeding major river systems that sustain over 500 million people through its complex hydrological network.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Periyar_River.jpg/1200px-Periyar_River.jpg',
            order=3
        )
        sm3.concept_tags.add(concept_tags['Hydrology'], concept_tags['Ecosystem Balance'], concept_tags['Biodiversity'])
        
        # Module 4: Conservation
        sm4 = StudyMaterial.objects.create(
            topic=western_ghats_topic,
            title='Threats and Conservation',
            content_text=self._get_western_ghats_module4(),
            difficulty='advanced',
            estimated_time='long',
            summary='Despite UNESCO World Heritage status, the Western Ghats faces threats from deforestation, mining, and climate change. The Gadgil and Kasturirangan reports provide recommendations for conservation.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
            order=4
        )
        sm4.concept_tags.add(concept_tags['Conservation'], concept_tags['Environmental Impact'], concept_tags['Sustainable Development'], concept_tags['Climate Change'])
        
        # ========================================
        # CLIMATE CHANGE - COMPREHENSIVE
        # ========================================
        climate_topic, _ = Topic.objects.get_or_create(
            name='Climate Change',
            section=env_section,
            defaults={
                'description': 'Learn about the causes and effects of climate change on our planet.',
                'order': 2
            }
        )
        
        climate_topic.study_materials.all().delete()
        
        # Module 1: Understanding Climate Change
        sm5 = StudyMaterial.objects.create(
            topic=climate_topic,
            title='Understanding Climate Change',
            content_text=self._get_climate_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Climate change refers to long-term shifts in global temperatures. While natural factors exist, human activities (especially fossil fuel burning) are the primary driver since the Industrial Revolution.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Carbon_dioxide_levels.svg/1200px-Carbon_dioxide_levels.svg.png',
            order=1
        )
        sm5.concept_tags.add(concept_tags['Climate Change'], concept_tags['Greenhouse Effect'], concept_tags['Carbon Cycle'])
        
        # Module 2: Impact and Mitigation
        sm6 = StudyMaterial.objects.create(
            topic=climate_topic,
            title='Impact and Mitigation Strategies',
            content_text=self._get_climate_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Climate change impacts include ecosystem disruption, extreme weather, and sea level rise. Mitigation involves reducing emissions through renewable energy and carbon capture, while adaptation builds resilience.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Climate_change_impact.jpg/1200px-Climate_change_impact.jpg',
            order=2
        )
        sm6.concept_tags.add(concept_tags['Climate Change'], concept_tags['Mitigation'], concept_tags['Adaptation'], concept_tags['Environmental Impact'])
        
        # Module 3: Kerala Context
        sm7 = StudyMaterial.objects.create(
            topic=climate_topic,
            title='Climate Change Impacts on Kerala',
            content_text=self._get_climate_module3(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Kerala faces unique climate vulnerabilities including sea-level rise, monsoon variability, and ecosystem disruption. The 2018 floods demonstrated the regions extreme climate sensitivity.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Carbon_dioxide_levels.svg/1200px-Carbon_dioxide_levels.svg.png',
            order=3
        )
        sm7.concept_tags.add(concept_tags['Climate Change'], concept_tags['Sustainable Development'], concept_tags['Environmental Impact'])
        
        # ========================================
        # WILDLIFE PROTECTION - COMPREHENSIVE
        # ========================================
        wildlife_topic, _ = Topic.objects.get_or_create(
            name='Wildlife Protection',
            section=env_section,
            defaults={
                'description': 'Discover efforts to protect endangered wildlife and their habitats.',
                'order': 3
            }
        )
        
        wildlife_topic.study_materials.all().delete()
        
        # Module 1: Wildlife Conservation in India
        sm8 = StudyMaterial.objects.create(
            topic=wildlife_topic,
            title='Wildlife Conservation in India',
            content_text=self._get_wildlife_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='India is home to diverse wildlife with over 550 wildlife sanctuaries and 100+ national parks. Project Tiger and Project Elephant are major conservation initiatives.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
            order=1
        )
        sm8.concept_tags.add(concept_tags['Wildlife Conservation'], concept_tags['Conservation'], concept_tags['Biodiversity'])
        
        # Module 2: Endangered Species
        sm9 = StudyMaterial.objects.create(
            topic=wildlife_topic,
            title='Endangered Species of India',
            content_text=self._get_wildlife_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='India has numerous critically endangered species including the Asiatic Lion, Bengal Tiger, and Great Indian Bustard. Conservation efforts have shown success in species recovery.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Asiatic_Lion.jpg/1200px-Asiatic_Lion.jpg',
            order=2
        )
        sm9.concept_tags.add(concept_tags['Endangered Species'], concept_tags['Wildlife Conservation'], concept_tags['Conservation'])
        
        self.stdout.write(self.style.SUCCESS('Environment section materials created'))

    def _create_heritage_materials(self, concept_tags):
        """Create Heritage Sites section study materials"""
        
        # Get or create Heritage section
        heritage_section, _ = Section.objects.get_or_create(
            name='Heritage Sites',
            defaults={
                'description': 'Explore historical heritage sites and their significance.',
                'is_general': True
            }
        )
        
        # ========================================
        # FORT KOCHI
        # ========================================
        fort_kochi_topic, _ = Topic.objects.get_or_create(
            name='Fort Kochi',
            section=heritage_section,
            defaults={
                'description': 'Explore the historic Fort Kochi area with its colonial architecture and cultural blend.',
                'order': 1
            }
        )
        
        fort_kochi_topic.study_materials.all().delete()
        
        # Module 1: Introduction
        sm1 = StudyMaterial.objects.create(
            topic=fort_kochi_topic,
            title='Introduction to Fort Kochi',
            content_text=self._get_fortkochi_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Fort Kochi is a historic port city in Kerala known for its rich colonial heritage. The Portuguese built the first fort in 1503, followed by Dutch and British rule.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/St._Francis_Church_Kochi.jpg/1200px-St._Francis_Church_Kochi.jpg',
            order=1
        )
        sm1.concept_tags.add(concept_tags['Historical Sites'], concept_tags['Colonial History'], concept_tags['Heritage Preservation'])
        
        # Module 2: Cultural Fusion
        sm2 = StudyMaterial.objects.create(
            topic=fort_kochi_topic,
            title='Cultural Fusion in Fort Kochi',
            content_text=self._get_fortkochi_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Fort Kochi represents a unique blend of Portuguese, Dutch, British, Jewish, and Chinese cultures, creating a distinctive multicultural heritage.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Chinese_fishing_nets_Kochi.jpg/1200px-Chinese_fishing_nets_Kochi.jpg',
            order=2
        )
        sm2.concept_tags.add(concept_tags['Cultural Artforms'], concept_tags['Traditional Knowledge'], concept_tags['Heritage Preservation'])
        
        # ========================================
        # PADMANABHAPURAM PALACE
        # ========================================
        padmanabhapuram_topic, _ = Topic.objects.get_or_create(
            name='Padmanabhapuram Palace',
            section=heritage_section,
            defaults={
                'description': 'Discover the ancient wooden palace of the Travancore kings.',
                'order': 2
            }
        )
        
        padmanabhapuram_topic.study_materials.all().delete()
        
        # Module 1: History
        sm3 = StudyMaterial.objects.create(
            topic=padmanabhapuram_topic,
            title='History of Padmanabhapuram Palace',
            content_text=self._get_padmanabhapuram_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Padmanabhapuram Palace is one of the oldest wooden palaces in the world, built in the 16th century as the residence of Travancore rulers.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Padmanabhapuram_Palace.jpg/1200px-Padmanabhapuram_Palace.jpg',
            order=1
        )
        sm3.concept_tags.add(concept_tags['Historical Sites'], concept_tags['Archaeological Heritage'], concept_tags['Heritage Preservation'])
        
        # Module 2: Architecture
        sm4 = StudyMaterial.objects.create(
            topic=padmanabhapuram_topic,
            title='Architecture and Features',
            content_text=self._get_padmanabhapuram_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='The palace showcases exquisite Kerala architecture with intricate woodwork, ancient murals, and unique construction techniques using only wooden pins.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Padmanabhapuram_Palace.jpg/1200px-Padmanabhapuram_Palace.jpg',
            order=2
        )
        sm4.concept_tags.add(concept_tags['Architecture'], concept_tags['Archaeological Heritage'], concept_tags['Traditional Knowledge'])
        
        self.stdout.write(self.style.SUCCESS('Heritage section materials created'))

    def _create_cultural_materials(self, concept_tags):
        """Create Cultural Artforms section study materials"""
        
        # Get or create Cultural section
        cultural_section, _ = Section.objects.get_or_create(
            name='Cultural Artforms',
            defaults={
                'description': 'Discover cultural artforms and traditions.',
                'is_general': True
            }
        )
        
        # ========================================
        # KATHAKALI
        # ========================================
        kathakali_topic, _ = Topic.objects.get_or_create(
            name='Kathakali',
            section=cultural_section,
            defaults={
                'description': 'Learn about the classical dance-drama of Kerala known for its elaborate makeup and costumes.',
                'order': 1
            }
        )
        
        kathakali_topic.study_materials.all().delete()
        
        sm1 = StudyMaterial.objects.create(
            topic=kathakali_topic,
            title='Introduction to Kathakali',
            content_text=self._get_kathakali_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Kathakali is a classical dance-drama from Kerala developed in the 17th century, known for elaborate makeup, colorful costumes, and dramatic storytelling from Hindu epics.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kathakali_performance.jpg/1200px-Kathakali_performance.jpg',
            order=1
        )
        sm1.concept_tags.add(concept_tags['Performing Arts'], concept_tags['Classical Dance'], concept_tags['Traditional Knowledge'])
        
        sm2 = StudyMaterial.objects.create(
            topic=kathakali_topic,
            title='Makeup and Costumes',
            content_text=self._get_kathakali_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Kathakali makeup (Vesham) is a complex art form with distinct types: Pachcha (green for heroes), Kathi (red for villains), Minukku (gold for women), and Kari (black for demons).',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kathakali_performance.jpg/1200px-Kathakali_performance.jpg',
            order=2
        )
        sm2.concept_tags.add(concept_tags['Performing Arts'], concept_tags['Traditional Knowledge'], concept_tags['Cultural Artforms'])
        
        # ========================================
        # MOHINIYATTAM
        # ========================================
        mohiniyattam_topic, _ = Topic.objects.get_or_create(
            name='Mohiniyattam',
            section=cultural_section,
            defaults={
                'description': 'Discover the graceful classical dance form of Kerala.',
                'order': 2
            }
        )
        
        mohiniyattam_topic.study_materials.all().delete()
        
        sm3 = StudyMaterial.objects.create(
            topic=mohiniyattam_topic,
            title='Introduction to Mohiniyattam',
            content_text=self._get_mohiniyattam_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Mohiniyattam is the graceful classical dance form of Kerala, named after Mohini (the enchantress avatar of Vishnu). It features gentle, flowing movements and white costumes with gold borders.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohiniyattam_dance.jpg/1200px-Mohiniyattam_dance.jpg',
            order=1
        )
        sm3.concept_tags.add(concept_tags['Classical Dance'], concept_tags['Performing Arts'], concept_tags['Traditional Knowledge'])
        
        sm4 = StudyMaterial.objects.create(
            topic=mohiniyattam_topic,
            title='Techniques and Performance',
            content_text=self._get_mohiniyattam_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Mohiniyattam features 24 main mudras (hand gestures), subtle expressions, and graceful transitions. The costume (Kasavu) is white with gold border, creating an elegant appearance.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohiniyattam_dance.jpg/1200px-Mohiniyattam_dance.jpg',
            order=2
        )
        sm4.concept_tags.add(concept_tags['Classical Dance'], concept_tags['Performing Arts'], concept_tags['Cultural Artforms'])
        
        # ========================================
        # THEYAM
        # ========================================
        theyyam_topic, _ = Topic.objects.get_or_create(
            name='Theyyam',
            section=cultural_section,
            defaults={
                'description': 'Explore the ritual dance form of North Kerala.',
                'order': 3
            }
        )
        
        theyyam_topic.study_materials.all().delete()
        
        sm5 = StudyMaterial.objects.create(
            topic=theyyam_topic,
            title='Introduction to Theyyam',
            content_text=self._get_theyyam_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Theyyam is a ritual dance form from North Kerala (Kasaragod and Kannur) dating back over 1,500 years. It involves spirit possession where performers become vessels for deities.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Theyyam_performance.jpg/1200px-Theyyam_performance.jpg',
            order=1
        )
        sm5.concept_tags.add(concept_tags['Ritual Traditions'], concept_tags['Traditional Knowledge'], concept_tags['Cultural Artforms'])
        
        sm6 = StudyMaterial.objects.create(
            topic=theyyam_topic,
            title='Makeup and Rituals',
            content_text=self._get_theyyam_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Theyyam makeup uses natural herbs with symbolic colors. The ritual involves fasting, purification, transformation through makeup, and divine possession during performance.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Theyyam_performance.jpg/1200px-Theyyam_performance.jpg',
            order=2
        )
        sm6.concept_tags.add(concept_tags['Ritual Traditions'], concept_tags['Traditional Knowledge'], concept_tags['Performing Arts'])
        
        # ========================================
        # KALARIPAYATTU
        # ========================================
        kalaripayattu_topic, _ = Topic.objects.get_or_create(
            name='Kalaripayattu',
            section=cultural_section,
            defaults={
                'description': 'Discover the ancient martial art form of Kerala, known as the mother of all martial arts.',
                'order': 4
            }
        )
        
        kalaripayattu_topic.study_materials.all().delete()
        
        sm7 = StudyMaterial.objects.create(
            topic=kalaripayattu_topic,
            title='Introduction to Kalaripayattu',
            content_text=self._get_kalaripayattu_module1(),
            difficulty='beginner',
            estimated_time='short',
            summary='Kalaripayattu is the oldest martial art in India, originating from Kerala in the 3rd century CE. Known as the "Mother of All Martial Arts," it includes strikes, kicks, grappling, and weapon training.',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kalaripayattu.jpg/1200px-Kalaripayattu.jpg',
            order=1
        )
        sm7.concept_tags.add(concept_tags['Martial Arts'], concept_tags['Traditional Knowledge'], concept_tags['Cultural Artforms'])
        
        sm8 = StudyMaterial.objects.create(
            topic=kalaripayattu_topic,
            title='Training and Techniques',
            content_text=self._get_kalaripayattu_module2(),
            difficulty='intermediate',
            estimated_time='medium',
            summary='Kalaripayattu training involves physical conditioning, flexibility exercises, and weapon training. It follows the Gurukula system with a master (Guru) teaching students in a traditional Kalari (training center).',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kalaripayattu.jpg/1200px-Kalaripayattu.jpg',
            order=2
        )
        sm8.concept_tags.add(concept_tags['Martial Arts'], concept_tags['Traditional Knowledge'], concept_tags['Cultural Artforms'])
        
        self.stdout.write(self.style.SUCCESS('Cultural section materials created'))

    # ========================================
    # CONTENT METHODS - WESTERN GHATS
    # ========================================
    
    def _get_western_ghats_module1(self):
        return '''# The Great Escarpment of India

## 1. Introduction

The Western Ghats, also known as the **Sahyadri**, is a mountain range that covers an area of 160,000 km² in a stretch of 1,600 km parallel to the western coast of the Indian peninsula.

## 2. Formation

Unlike the Himalayas, the Western Ghats are not "true" mountains. They are the **faulted edge of the Deccan Plateau**, formed during the break-up of the supercontinent **Gondwana** approximately 150 million years ago. This makes them one of the oldest mountain ranges in the world.

## 3. Geographic Extent

The Western Ghats stretches from the **Tapi River in Gujarat** to **Kanyakumari in Tamil Nadu**, running through the states of:
- Gujarat
- Maharashtra
- Goa
- Karnataka
- Kerala
- Tamil Nadu

## 4. Highest Peak

**Anamudi** (2,695 m) in Kerala is the highest peak in India south of the Himalayas. It is often called the **"Everest of South India"** and is located in the Anamalai hills of Kerala.

## 5. Climate Regulator

The Western Ghats act as a **key barrier to the moisture-laden southwest monsoon winds**. This geographical feature causes:
- Heavy rainfall on the western slopes
- Creates the lush rainforests Kerala is known for
- Results in a rain shadow effect on the eastern side

The mountains intercept the monsoon clouds, resulting in annual rainfall ranging from 2,000 mm to 7,000 mm on the windward side, making this region one of the wettest places on Earth.

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Escarpment | A steep slope or long cliff that separates two relatively level areas |
| Gondwana | Ancient supercontinent that included India, Africa, and South America |
| Rain Shadow | Dry area caused by mountains blocking moisture |
| Fault | A fracture in Earths crust where blocks of land move |

## 7. Summary

The Western Ghats represents one of Indias most significant geographical features, serving as a biodiversity hotspot, climate regulator, and water tower for millions of people.

## 8. Assessment

### Easy Questions
1. What is another name for the Western Ghats?
2. How long is the Western Ghats mountain range?
3. Which is the highest peak in the Western Ghats?

### Medium Questions
1. Explain how the Western Ghats influences Keralas climate.
2. Describe the geological formation of the Western Ghats.

### Analytical Question
1. How does the Western Ghats act as a climate barrier, and what are its effects?

## 9. Learning Outcomes

- Define the Western Ghats and its geographical extent
- Explain the formation of the Western Ghats
- Analyze the role of Western Ghats in climate regulation
- Compare Western Ghats with other mountain ranges in India
- Evaluate the importance of the Western Ghats for South India'''

    def _get_western_ghats_module2(self):
        return '''# A Global Biodiversity Hotspot

## 1. Introduction

The Western Ghats is recognized as one of the **eight hottest biodiversity hotspots** in the world. It is home to over **7,000 species of flowering plants** and hundreds of animal species, many of which are found nowhere else on Earth.

## 2. Endemic Species

The region has an incredibly high rate of **endemism** - species found only here and nowhere else:
- Over 1,500 species of endemic flowering plants
- Over 150 species of endemic reptiles
- Over 100 species of endemic amphibians

## 3. Flagship Species

**Nilgiri Tahr**
An endangered mountain goat found in the high-altitude grasslands of **Eravikulam National Park**. The Nilgiri Tahr is the state animal of Tamil Nadu and Kerala.

**Lion-tailed Macaque**
One of the **rarest primates in the world**, recognizable by its silver-white mane. These primates live exclusively in the rainforests of the Western Ghats.

**Malabar Giant Squirrel**
A colorful canopy-dwelling rodent found in the forests of the Western Ghats. It is one of the largest squirrel species in the world.

**Neelakurinji**
A unique shrub found in the Shola forests that blooms only once every **12 years**, turning the hillsides purple. The last major bloom was in 2018.

## 4. Wildlife Corridors

The Western Ghats serves as an important wildlife corridor connecting various national parks and wildlife sanctuaries, allowing for the movement of elephants, tigers, and other large mammals.

## 5. Ecosystem Types

The Western Ghats contains:
- Tropical rainforests
- Semi-evergreen forests
- Moist deciduous forests
- Shola grasslands
- Montane forests

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Endemic | Species found only in a specific region |
| Biodiversity Hotspot | Areas with high biodiversity under threat |
| Shola | High-altitude evergreen forests in Western Ghats |
| Montane | Mountain ecosystems |

## 7. Kerala Example

Keralas portion of the Western Ghats includes:
- **Eravikulam National Park** - Home to Nilgiri Tahr
- **Silent Valley National Park** - Pristine rainforests
- **Periyar Tiger Reserve** - Famous for elephants

## 8. Summary

The Western Ghats biodiversity is of global significance, with numerous endemic species and unique ecosystems requiring conservation.

## 9. Assessment

### Easy Questions
1. What is the Western Ghats known as?
2. Name one endemic species of the Western Ghats.
3. How often does Neelakurinji bloom?

### Medium Questions
1. Explain the concept of endemism with examples.
2. Describe the wildlife corridors in the Western Ghats.

### Analytical Question
1. Why is the Western Ghats considered a biodiversity hotspot, and what are the conservation challenges?

## 10. Learning Outcomes

- Define biodiversity hotspot and endemic species
- Explain the significance of endemic species
- Analyze conservation challenges
- Compare different ecosystem types
- Evaluate conservation efforts in the Western Ghats'''

    def _get_western_ghats_module3(self):
        return '''# The Water Tower of South India

## 1. Introduction

The Western Ghats are essentially the **"Water Tower"** for peninsular India. They feed a complex network of river systems that sustain millions of people and thousands of hectares of farmland.

## 2. Major River Origins

**Rivers in Kerala**
- **Periyar**: The longest river in Kerala, originating from the Western Ghats
- **Bharatapuzha**: Also known as River of Heaven, major river in Kerala
- **Pamba River**: Flows through the heart of Kerala, originating from the Ghats

**Interstate Rivers**
- **Godavari**: Originates from the Western Ghats in Maharashtra, flows across central India
- **Krishna**: Another major river originating from the Ghats, flowing through Maharashtra, Karnataka, and Andhra Pradesh
- **Kaveri**: Known as the Ganga of the South, originates from Karnataka and flows through Tamil Nadu

## 3. Ecosystem Services

Beyond water supply, the forests of the Western Ghats provide:

**Carbon Sequestration**
The forests act as **massive carbon sinks**, helping mitigate the effects of global warming in the Indian subcontinent. The dense vegetation absorbs significant amounts of carbon dioxide.

**Soil Conservation**
The steep slopes and dense vegetation prevent soil erosion and landslides.

**Groundwater Recharge**
The forests help recharge groundwater aquifers that feed springs and wells in the surrounding plains.

**Biodiversity Habitat**
The rivers originating from the Ghats support diverse aquatic ecosystems and fish species.

## 4. Importance for South India

Over **500 million people** depend on the rivers originating from the Western Ghats for their water needs, making this region crucial for the ecological and economic well-being of South India.

## 5. Key Terminology

| Term | Definition |
|------|------------|
| Carbon Sink | Natural reservoir that absorbs carbon dioxide |
| Groundwater Recharge | Process of water entering underground aquifers |
| Ecosystem Services | Benefits humans derive from ecosystems |
| Watershed | Area of land where water drains to a common outlet |

## 6. Classification

**Rivers by Origin:**
- West-flowing (into Arabian Sea)
- East-flowing (into Bay of Bengal)

## 7. Summary

The Western Ghats hydrological system is vital for water security, agriculture, and ecosystems across South India.

## 8. Assessment

### Easy Questions
1. What is the Western Ghats called?
2. Name one river originating from the Western Ghats.
3. How many people depend on Ghats rivers?

### Medium Questions
1. Explain the ecosystem services provided by Western Ghats forests.
2. Describe the difference between west-flowing and east-flowing rivers.

### Analytical Question
1. How does the Western Ghats contribute to water security in South India?

## 9. Learning Outcomes

- Define ecosystem services and carbon sequestration
- Explain the rivers originating from Western Ghats
- Analyze the importance of watershed management
- Compare west-flowing and east-flowing rivers
- Evaluate water security challenges'''

    def _get_western_ghats_module4(self):
        return '''# Threats and Conservation

## 1. Introduction

Despite their **UNESCO World Heritage status** (inscribed in 2012), the Western Ghats face severe environmental pressures that threaten its unique ecosystems.

## 2. Key Threats

**1. Deforestation**
- Conversion of forest land into **tea, coffee, and rubber plantations**
- Illegal logging for timber and firewood
- Expansion of agricultural activities in forest areas

**2. Mining**
- **Iron and manganese ore mining** has caused massive soil erosion in some regions
- Mining activities in Goa, Karnataka, and Maharashtra have devastated large forest areas
- Illegal sand mining along river beds

**3. Climate Change**
- Erratic rainfall patterns leading to landslides and floods
- As seen in the **2018 Kerala floods** that caused massive destruction
- Changing temperature patterns affecting endemic species
- Shifting of vegetation zones up the mountains

**4. Infrastructure Development**
- Highway expansion through forest areas
- Dam construction disrupting natural water flow
- Urbanization in hill stations

## 3. Conservation Reports

**Gadgil Report (2011)**
Led by ecologist Madhav Gadgil, this report recommended:
- Classification of the entire Western Ghats as an Ecologically Sensitive Area (ESA)
- Strict regulations on development activities
- Community-based forest management

**Kasturirangan Report (2013)**
Led by environmentalist Sri K. Kasturirangan, this report was more moderate:
- Suggested covering about 37% of the Western Ghats as ESA
- Focused on balancing development with conservation
- Called for sustainable development practices

## 4. Conservation Efforts

- **Project Elephant** and **Project Tiger** continue to protect wildlife
- Several national parks and wildlife sanctuaries
- Community-based conservation initiatives
- Research and monitoring programs

## 5. Advantages of Conservation

1. Preservation of biodiversity
2. Water security for millions
3. Climate regulation
4. Tourism and economic benefits
5. Cultural preservation

## 6. Challenges

1. Balancing development needs
2. Managing human-wildlife conflict
3. Addressing climate change impacts
4. Enforcement of regulations

## 7. Key Terminology

| Term | Definition |
|------|------------|
| Ecologically Sensitive Area | Regions requiring special protection |
| Sustainable Development | Meeting needs without compromising future |
| Deforestation | Clearing of forests for other uses |
| Biodiversity | Variety of life in an area |

## 8. Summary

The survival of the Western Ghats depends on balancing human development needs with environmental conservation through scientific management and community participation.

## 9. Assessment

### Easy Questions
1. When was the Western Ghats inscribed as UNESCO World Heritage?
2. Name one threat to the Western Ghats.
3. What is Project Tiger?

### Medium Questions
1. Compare the Gadgil and Kasturirangan reports.
2. Explain three major threats to the Western Ghats.

### Analytical Question
1. How can development and conservation be balanced in the Western Ghats region?

## 10. Learning Outcomes

- Define ecological sensitivity and sustainable development
- Explain major threats to Western Ghats
- Analyze conservation recommendations
- Compare different conservation approaches
- Evaluate the effectiveness of conservation efforts'''

    # ========================================
    # CONTENT METHODS - CLIMATE CHANGE
    # ========================================
    
    def _get_climate_module1(self):
        return '''# Understanding Climate Change

## 1. Introduction

Climate change refers to **long-term shifts in global temperatures and weather patterns**. While natural factors can cause climate variations, human activities have been the primary driver since the Industrial Revolution.

## 2. Definition

Climate change is a significant and lasting change in the statistical distribution of weather patterns over periods ranging from decades to millions of years. It may be a change in the average weather conditions or in the distribution of weather around the average conditions.

## 3. Key Facts

- **Global average temperature** has increased by about 1.1°C since the late 19th century
- **CO2 levels** have reached over 420 ppm (parts per million) - the highest in 2 million years
- **Sea levels** are rising due to melting ice caps and thermal expansion
- **Weather extremes** are becoming more frequent and intense

## 4. Causes of Climate Change

**Natural Causes**
- Volcanic eruptions
- Solar radiation variations
- Ocean current changes

**Human Causes (Primary Driver)**
- **Burning fossil fuels** - coal, oil, and natural gas
- **Deforestation** - reduces carbon absorption
- **Industrial processes** - release greenhouse gases
- **Agriculture** - methane from livestock and rice paddies

## 5. The Greenhouse Effect

The greenhouse effect is a natural process that warms the Earth's surface. When sunlight reaches Earth, some is reflected back to space, and some is absorbed and re-radiated as heat. Greenhouse gases in the atmosphere trap some of this heat, keeping the Earth warm enough to support life.

However, human activities have increased greenhouse gas concentrations, intensifying the natural greenhouse effect and causing global warming.

## 6. Evidence of Climate Change

1. **Rising temperatures** - Each decade since 1980 has been warmer than the preceding one
2. **Melting ice caps** - Arctic sea ice is declining
3. **Sea level rise** - Oceans are expanding as they warm
4. **Changing precipitation** - Some areas getting wetter, others drier
5. **Ocean acidification** - CO2 dissolving in oceans making them more acidic

## 7. Key Terminology

| Term | Definition |
|------|------------|
| Greenhouse Gases | Gases that trap heat in the atmosphere |
| Carbon Footprint | Total GHG emissions caused by an individual or entity |
| Greenhouse Effect | Natural warming process enhanced by GHGs |
| ppm | Parts per million - measurement unit |

## 8. Summary

Climate change is primarily driven by human activities, particularly greenhouse gas emissions from fossil fuels and deforestation.

## 9. Assessment

### Easy Questions
1. What is climate change?
2. Name one greenhouse gas.
3. What is the greenhouse effect?

### Medium Questions
1. Explain the difference between natural and human causes of climate change.
2. Describe three evidences of climate change.

### Analytical Question
1. How does the greenhouse effect work, and how have human activities intensified it?

## 10. Learning Outcomes

- Define climate change and greenhouse effect
- Explain causes of climate change
- Analyze evidence of climate change
- Compare natural and anthropogenic factors
- Evaluate the role of human activities'''

    def _get_climate_module2(self):
        return '''# Impact and Mitigation Strategies

## 1. Introduction

Climate change impacts span environmental, social, and economic dimensions. Understanding these impacts helps in developing effective response strategies.

## 2. Environmental Impacts

**Ecosystem Disruption**
- Species forced to migrate to cooler areas
- Coral bleaching due to warmer oceans
- Loss of biodiversity as habitats change faster than species can adapt

**Extreme Weather Events**
- More frequent and intense hurricanes and cyclones
- Increased flooding in some regions
- More severe droughts in other areas

**Sea Level Rise**
- Threat to coastal cities and islands
- Saltwater intrusion into freshwater sources
- Loss of coastal wetlands

## 3. Social Impacts

**Food Security**
- Changes in agricultural patterns
- Crop failures due to extreme weather
- Water scarcity affecting food production

**Health Impacts**
- Spread of diseases to new areas
- Heat-related illnesses
- Air quality deterioration

**Economic Impacts**
- Damage to infrastructure from extreme weather
- Costs of adaptation and mitigation
- Displacement of populations

## 4. Mitigation Strategies

**Reducing Emissions**

1. **Transition to Renewable Energy**
   - Solar power
   - Wind energy
   - Hydroelectric power
   - Nuclear energy

2. **Energy Efficiency**
   - Better insulation in buildings
   - Efficient appliances and vehicles
   - Public transportation

3. **Carbon Capture and Storage**
   - Technology to capture CO2 from atmosphere
   - Storage in underground formations

## 5. Adaptation Strategies

1. **Infrastructure Resilience**
   - Building flood defenses
   - Heat-resistant buildings
   - Storm-resistant structures

2. **Agricultural Adaptation**
   - Developing climate-resilient crops
   - Changing planting schedules
   - Improving irrigation systems

3. **Water Management**
   - Rainwater harvesting
   - Water recycling
   - Desalination plants

## 6. Individual Actions

- Reduce energy consumption
- Use public transportation
- Plant trees
- Reduce, reuse, recycle
- Support renewable energy
- Educate others about climate change

## 7. Key Terminology

| Term | Definition |
|------|------------|
| Mitigation | Actions to reduce GHG emissions |
| Adaptation | Adjusting to climate change impacts |
| Carbon Capture | Technology to remove CO2 from atmosphere |
| Climate Resilience | Capacity to anticipate and respond to hazards |

## 8. Summary

Addressing climate change requires both mitigation (reducing emissions) and adaptation (coping with impacts) at individual, national, and international levels.

## 9. Assessment

### Easy Questions
1. What is mitigation?
2. Name one renewable energy source.
3. What is adaptation?

### Medium Questions
1. Explain the difference between mitigation and adaptation with examples.
2. Describe three environmental impacts of climate change.

### Analytical Question
1. How can individuals contribute to climate action while maintaining economic development?

## 10. Learning Outcomes

- Define mitigation and adaptation strategies
- Explain environmental and social impacts
- Analyze response strategies
- Compare mitigation and adaptation
- Evaluate the role of individual actions'''

    def _get_climate_module3(self):
        return '''# Climate Change Impacts on Kerala

## 1. Introduction

Kerala, located on Indias southwestern coast, exemplifies climate change impacts on tropical coastal regions. The states narrow coastal strip and dependency on monsoons make it particularly vulnerable.

## 2. Vulnerabilities

**Sea-Level Rise**
Keralas 580 km coastline faces erosion and inundation risks. Coastal communities numbering millions are threatened by sea-level rise and storm surges.

**Monsoon Variability**
Irregular rainfall patterns affect agriculture and water resources. The 2018 floods caused estimated damages of over ₹30,000 crores.

**Western Ghats Ecosystem**
Biodiversity hotspots face habitat disruption, affecting endemic species and forest-dependent communities.

**Coastal Communities**
Fishing communities experience livelihood threats from declining fish stocks and extreme weather events.

## 3. The 2018 Kerala Floods

The 2018 floods were one of the worst natural disasters in Keralas history:
- Caused by extremely heavy monsoon rainfall
- Over 1 million people displaced
- Significant loss of life and property
- Demonstrated climate vulnerability

## 4. Adaptation Initiatives

**Coastal Zone Management**
- Sea wall construction
- Mangrove restoration
- Relocation of vulnerable communities

**Climate-Resilient Agriculture**
- Drought-resistant crop varieties
- Organic farming practices
- Water conservation techniques

**Renewable Energy**
- Solar power initiatives
- Wind energy projects
- State solar energy policy

**Community-Based Approaches**
- Disaster management training
- Early warning systems
- Local knowledge integration

## 5. Advantages of Climate Action in Kerala

1. Extensive coastline for renewable energy
2. Strong institutional framework
3. High literacy rate for awareness
4. Successful disaster management experience
5. Tourism sector motivation

## 6. Challenges

1. High population density
2. Limited land for large projects
3. Balancing development with conservation
4. Funding constraints
5. Climate justice for coastal communities

## 7. Key Terminology

| Term | Definition |
|------|------------|
| Sea-Level Rise | Increase in average sea level due to warming |
| Mangrove | Coastal wetland trees important for protection |
| Climate Resilience | Ability to anticipate and recover from climate impacts |
| Early Warning Systems | Technologies to predict and alert about disasters |

## 8. Summary

Keralas experience demonstrates both the urgent need for climate action and the potential for localized adaptation strategies in vulnerable regions.

## 9. Assessment

### Easy Questions
1. What makes Kerala vulnerable to climate change?
2. When did the major Kerala floods occur?
3. Name one adaptation initiative in Kerala.

### Medium Questions
1. Explain the causes and impacts of the 2018 Kerala floods.
2. Describe three climate vulnerabilities of Kerala.

### Analytical Question
1. How can Kerala balance development needs with climate resilience?

## 10. Learning Outcomes

- Define climate vulnerabilities specific to Kerala
- Explain the 2018 floods and their implications
- Analyze adaptation initiatives
- Compare Keralas approach with other regions
- Evaluate challenges and opportunities'''

    # ========================================
    # CONTENT METHODS - WILDLIFE
    # ========================================
    
    def _get_wildlife_module1(self):
        return '''# Wildlife Conservation in India

## 1. Introduction

India is home to diverse wildlife and has implemented various conservation measures to protect its rich biodiversity. The country contains about 7-8% of all species on Earth.

## 2. Conservation Network

**Protected Areas**
- **Wildlife Sanctuaries**: Over 550 wildlife sanctuaries
- **National Parks**: More than 100 national parks covering various ecosystems
- **Tiger Reserves**: Over 50 tiger reserves under Project Tiger
- **Conservation Reserves**: Over 100 conservation reserves

**Major National Parks**
- **Kanha National Park** - Madhya Pradesh
- **Jim Corbett National Park** - Uttarakhand (oldest national park in India)
- **Kaziranga National Park** - Assam (one-horned rhinoceros)
- **Sundarbans National Park** - West Bengal (Bengal tigers)
- **Periyar National Park** - Kerala
- **Bandipur National Park** - Karnataka

## 3. Conservation Projects

**Project Tiger**
Launched in **1973**, Project Tiger is one of the most successful conservation programs in the world:
- Aims to save the endangered Bengal tiger
- Covers over 50 tiger reserves across India
- Focuses on habitat protection and anti-poaching measures
- Has helped increase tiger population from about 1,400 in 1973 to over 3,000 today

**Project Elephant**
Launched in **1992** to protect elephants:
- Covers elephant reserves across India
- Focuses on habitat conservation
- Addresses human-elephant conflict
- Protects migration corridors

## 4. Indias Iconic Wildlife

**Mammals**
- **Bengal Tiger** - National animal
- **Asiatic Lion** - Found only in Gir Forest
- **Indian Elephant** - Endangered species
- **One-horned Rhinoceros** - Found in Assam
- **Snow Leopard** - Found in Himalayan regions

**Birds**
- **Peacock** - National bird
- **Great Indian Bustard** - Critically endangered
- **Sarus Crane** - State bird of Uttar Pradesh

**Reptiles**
- **King Cobra** - Worlds longest venomous snake
- **Indian Python**
- **Marine Turtle**

## 5. Key Terminology

| Term | Definition |
|------|------------|
| Protected Areas | Regions designated for wildlife protection |
| Endemic Species | Species found only in specific regions |
| Conservation Project | Organized efforts to protect species/habitats |
| Habitat | Natural environment where species live |

## 6. Summary

India has developed one of the worlds most comprehensive wildlife conservation networks through protected areas and species-specific projects.

## 7. Assessment

### Easy Questions
1. When was Project Tiger launched?
2. What is Indias national animal?
3. Name one national park in Kerala.

### Medium Questions
1. Explain the achievements of Project Tiger.
2. Describe the major protected area categories in India.

### Analytical Question
1. How has Indias conservation approach evolved, and what are its challenges?

## 8. Learning Outcomes

- Define protected areas and conservation projects
- Explain Project Tiger and Project Elephant
- Analyze conservation achievements
- Compare different protected area categories
- Evaluate conservation challenges'''

    def _get_wildlife_module2(self):
        return '''# Endangered Species of India

## 1. Introduction

An endangered species is a species at risk of becoming extinct because of low population numbers or threats to its habitat. Conservation efforts focus on protecting these species from extinction.

## 2. IUCN Red List Categories

1. **Extinct (EX)** - No individuals remain
2. **Extinct in the Wild (EW)** - Only survives in captivity
3. **Critically Endangered (CR)** - Extremely high risk of extinction
4. **Endangered (EN)** - Very high risk of extinction
5. **Vulnerable (VU)** - High risk of extinction
6. **Near Threatened (NT)** - Likely to become threatened
7. **Least Concern (LC)** - Lowest risk

## 3. Critically Endangered Species in India

**Mammals**
- **Asiatic Lion** - Only about 700 individuals left, found only in Gujarat
- **Bengal Tiger** - About 3,000 individuals, endangered due to habitat loss
- **Snow Leopard** - About 500-700 individuals in Himalayas
- **One-horned Rhinoceros** - About 3,500 individuals, recovering due to conservation

**Birds**
- **Great Indian Bustard** - Less than 150 individuals
- **White-rumped Vulture** - Near total extinction from diclofenac poisoning
- **Himalayan Quail** - Possibly extinct, not seen since 1900

**Marine Species**
- **Hawksbill Turtle** - Threatened by habitat loss
- **Whale Shark** - Largest fish, threatened by fishing
- **Ganges River Dolphin** - About 1,200-1,500 individuals

## 4. Threats to Wildlife

**Habitat Loss**
- Deforestation for agriculture
- Urban expansion
- Mining activities

**Poaching**
- Illegal wildlife trade
- Trophy hunting
- Traditional medicine

**Pollution**
- Plastic waste in oceans
- Chemical contamination
- Climate change

**Human-Wildlife Conflict**
- Crop raiding by elephants
- Livestock predation by leopards
- Human casualties leading to retaliatory killings

## 5. Conservation Success Stories

**Indian Rhino**
- Population has increased from 200 in 1975 to over 3,500 today
- Successfully translocated to new habitats

**Bengal Tiger**
- Population increased from 1,400 in 1973 to over 3,000 today
- India now has 70% of worlds tigers

**Olive Ridley Turtle**
- Mass nesting protection programs
- Reduced mortality from fishing nets

## 6. Key Terminology

| Term | Definition |
|------|------------|
| IUCN | International Union for Conservation of Nature |
| Poaching | Illegal hunting or capturing of wildlife |
| Translocation | Moving species to new habitats |
| Endemic | Found only in one location |

## 7. Summary

While many species face extinction threats, successful conservation stories demonstrate that targeted efforts can reverse population declines.

## 8. Assessment

### Easy Questions
1. What does "critically endangered" mean?
2. Name one critically endangered species in India.
3. What is poaching?

### Medium Questions
1. Explain the IUCN Red List categories.
2. Describe three major threats to wildlife.

### Analytical Question
1. How can conservation efforts be improved to protect endangered species more effectively?

## 9. Learning Outcomes

- Define endangered species and IUCN categories
- Explain threats to wildlife
- Analyze conservation success stories
- Compare different threats
- Evaluate conservation strategies'''

    # ========================================
    # CONTENT METHODS - HERITAGE
    # ========================================
    
    def _get_fortkochi_module1(self):
        return '''# Introduction to Fort Kochi

## 1. Introduction

Fort Kochi is a historic port city in Kerala known for its rich colonial heritage and cultural diversity. It represents a unique blend of Indian and European cultures.

## 2. Location and History

Located in the **Ernakulam district**, Fort Kochi has been a center of trade for centuries. The area gets its name from the Fort of Kochi, which was built by the **Portuguese in 1503**.

**Historical Timeline**
- **1503**: Portuguese build the first European fort in India
- **1663**: Dutch capture Kochi and develop the area
- **1795**: British take control of Kochi
- **1947**: Independence of India

## 3. Key Landmarks

**St. Francis Church**
Built in **1503**, St. Francis Church is one of the oldest European churches in India:
- Originally built by the Portuguese
- Rebuilt by the Dutch in 1779
- Famous poet Samoothiri Ravi Varma was buried here
- Known for its simple yet elegant architecture

**Chinese Fishing Nets**
Known locally as **"Cheenavalai"**, these iconic fishing nets:
- Were introduced by Chinese traders during the 14th century
- Are a unique sight along the coastline
- Still used by local fishermen today
- Create a stunning visual against sunset

**Indo-Portuguese Museum**
Showcases the fusion of cultures:
- Historical artifacts
- Religious sculptures
- Cultural memorabilia

## 4. Key Terminology

| Term | Definition |
|------|------------|
| Colonial | Relating to rule by foreign power |
| Heritage | Inherited culture and traditions |
| Port | City for ship trading |
| Architecture | Building design and style |

## 5. Summary

Fort Kochi represents a unique historical destination where multiple cultures have left their mark over five centuries.

## 6. Assessment

### Easy Questions
1. When was the first fort built in Kochi?
2. Who built the first fort?
3. What are Chinese fishing nets called locally?

### Medium Questions
1. Describe the historical timeline of Fort Kochi.
2. Explain the significance of St. Francis Church.

### Analytical Question
1. How has Fort Kochi preserved its multicultural heritage?

## 7. Learning Outcomes

- Define colonial history and heritage
- Explain Fort Kochis historical significance
- Analyze cultural influences
- Compare different colonial periods
- Evaluate heritage preservation efforts'''

    def _get_fortkochi_module2(self):
        return '''# Cultural Fusion in Fort Kochi

## 1. Introduction

Fort Kochi is a unique blend of various cultures that have settled here over centuries, creating a distinctive multicultural heritage.

## 2. Portuguese Influence

The Portuguese were the first Europeans to establish trade relations with Kerala:
- Built the first fort in 1503
- Introduced Christianity to the region
- Created the first European settlement in India
- Left behind churches and colonial bungalows

## 3. Dutch Influence

The Dutch who captured Kochi in **1663** developed the area significantly:
- Built the famous **Dutch Palace** (Mattancherry Palace)
- Established spice trade
- Created the famous Jew Street
- Introduced architectural styles

## 4. British Influence

The British established their presence later:
- Added colonial architectural elements
- Developed the harbor
- Established administrative systems

## 5. Jewish Influence

The Jewish community settled here, creating:
- **Jew Street** (Jew Town)
- **Paradesi Synagogue** - the oldest active synagogue in the Commonwealth
- Jewish cemetery
- Spice and antique markets

## 6. Chinese Influence

Chinese traders left a unique legacy:
- **Chinese Fishing Nets** - Cheenavalai
- Trade in silk and spices
- Cultural exchange in maritime activities

## 7. Modern Fort Kochi

Today, Fort Kochi is known for:
- **Kochi-Muziris Biennale** - International art exhibition
- Colonial architecture blending with modern facilities
- Spice markets
- Antique shops
- Cafés and art galleries

## 8. Key Terminology

| Term | Definition |
|------|------------|
| Multicultural | Having multiple cultural influences |
| Synagogue | Jewish place of worship |
| Biennale | Art exhibition held every two years |
| Spice Trade | Historical trade in aromatic plants |

## 9. Summary

Fort Kochi exemplifies successful cultural integration, where diverse communities have coexisted and created a unique identity.

## 10. Assessment

### Easy Questions
1. Which community built the Dutch Palace?
2. What is the Paradesi Synagogue?
3. What is the Kochi-Muziris Biennale?

### Medium Questions
1. Explain the multicultural influences in Fort Kochi.
2. Describe the Jewish contribution to Fort Kochi.

### Analytical Question
1. How does Fort Kochi serve as a model for cultural coexistence?

## 11. Learning Outcomes

- Define multicultural heritage
- Explain different cultural influences
- Analyze cultural integration
- Compare various community contributions
- Evaluate cultural preservation'''

    def _get_padmanabhapuram_module1(self):
        return '''# History of Padmanabhapuram Palace

## 1. Introduction

Padmanabhapuram Palace is one of the oldest wooden palaces in the world, located in Kanyakumari district but historically part of the **Travancore kingdom**.

## 2. Historical Background

**Establishment**
- Built in the **16th century** (around 1550 AD)
- Served as the residence of the **Travancore rulers**
- Was the capital of the Venad kingdom before Thiruvananthapuram
- Remained the royal residence until 1795

**Notable Rulers**
- **Marthanda Varma** (1729-1758) - Founded modern Travancore
- **Karthika Thirunal** - Known for reforms
- **Rama Varma** - Expanded the kingdom

## 3. Location

Although located in **Kanyakumari district, Tamil Nadu**, the palace historically belonged to the Travancore kingdom:
- Now maintained by the **Archaeological Survey of India**
- One of the most visited heritage sites in South India
- About 50 km from Thiruvananthapuram

## 4. Architectural Significance

The palace represents the zenith of **traditional Kerala architecture**:
- Entirely made of wood (teak, rosewood, and coconut wood)
- Beautiful murals depicting mythological stories
- Unique ventilation system using copper plates

## 5. Notable Features

**Murals**
The palace has exquisite murals:
- Scenes from Ramayana and Mahabharata
- Portraits of kings and queens
- Nature and floral designs
- Some murals over 400 years old

**The Clock Tower**
- Known as "Kallanai"
- Still functional after centuries
- Shows blend of Indian and European styles

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Archaeological | Related to ancient cultures and ruins |
| Murals | Wall paintings |
| Travancore | Historical kingdom in Kerala |
| Palace | Royal residence |

## 7. Summary

Padmanabhapuram Palace stands as a testament to the architectural brilliance of traditional Kerala and the grandeur of the Travancore kingdom.

## 8. Assessment

### Easy Questions
1. When was Padmanabhapuram Palace built?
2. Which kingdom did it belong to?
3. What is it known for?

### Medium Questions
1. Describe the historical significance of the palace.
2. Explain its architectural features.

### Analytical Question
1. How does the palace reflect Travancore history and culture?

## 9. Learning Outcomes

- Define historical heritage and archaeology
- Explain palace history
- Analyze architectural features
- Compare with other palaces
- Evaluate conservation efforts'''

    def _get_padmanabhapuram_module2(self):
        return '''# Architecture and Features

## 1. Introduction

Padmanabhapuram Palace is a masterpiece of traditional Kerala architecture, showcasing exceptional craftsmanship and innovative design.

## 2. Construction Techniques

**Woodwork**
- Made primarily of **Teak wood** (Theku)
- **Rosewood** for intricate carvings
- **Coconut wood** for certain sections
- No iron nails - only wooden pegs

**Unique Features**
- Earthquake-resistant design
- Natural cooling systems
- Ventilation through copper plates
- Rainwater harvesting system

## 3. Palace Sections

**Mantrasala (Kings Council Chamber)**
- Where the king held meetings
- Beautiful wooden carvings
- Historical murals

**Nalukettu (Four-Hall Structure)**
- Traditional Kerala architectural style
- Central courtyard
- Surrounding rooms

**Theppakavu (Boat House)**
- Used for royal ceremonies
- Located near the palace pond

**Sthalapura (Royal Bedchamber)**
- Ornate wooden beds
- Ivory decorations
- Historical artifacts

## 4. The Famous Thiruvathira Dance Hall

This hall is renowned for its acoustic perfection:
- Circular design
- Perfect sound projection
- Where classical dance performances were held
- Features of the hall enhance musical sounds

## 5. Cultural Significance

**Murals**
The palace contains murals that are:
- Over 400 years old
- Depicting mythological stories
- Using natural pigments
- Preserved by ASI

**Impact on Architecture**
- Influenced later Travancore architecture
- Documented architectural techniques
- Preserved traditional craftsmanship

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Nalukettu | Traditional Kerala house style |
| Murals | Wall paintings |
| Vastu | Traditional Indian architecture |
| Carpentry | Woodworking craft |

## 7. Summary

The palaces architecture represents the pinnacle of traditional Kerala craftsmanship, with innovative features that continue to amply visitors.

## 8. Assessment

### Easy Questions
1. What materials were used in construction?
2. What is the Nalukettu?
3. How were the wooden pieces joined?

### Medium Questions
1. Explain the unique construction techniques.
2. Describe the palace sections and their purposes.

### Analytical Question
1. How does the architecture reflect traditional Kerala wisdom?

## 9. Learning Outcomes

- Define traditional architecture
- Explain construction techniques
- Analyze palace features
- Compare architectural styles
- Evaluate preservation challenges'''

    # ========================================
    # CONTENT METHODS - CULTURAL ARTFORMS
    # ========================================

    def _get_kathakali_module1(self):
        return '''# Introduction to Kathakali

## 1. Introduction

Kathakali is a classical dance-drama from Kerala, known for its elaborate makeup, colorful costumes, and dramatic storytelling. It is one of the most visually spectacular Indian classical art forms.

## 2. Origins

Kathakali developed in the **17th century** from Krishnanattam, a dance drama composed by Mani Madhava Chaotic. It evolved from temple arts and became a refined performing art over centuries.

## 3. Key Features

**Dramatic Storytelling**
- Blend of dance, acting, and music
- Stories from Ramayana, Mahabharata, and Puranas
- Expressive hand gestures (Mudras)
- Eye movements and facial expressions

**Traditional Orchestra**
- **Chenda** - Main percussion instrument
- **Ilathalam** - Cymbals
- **Veena** - String instrument
- **Vocals** - Traditional singing

**Performance Time**
- Usually performed at night
- Can last from sunset to dawn

## 4. Character Types

**Heroes (Pachcha)**
- Noble and divine characters
- Green makeup with white beard
- Represents divine characters

**Villains (Kathi)**
- Evil characters
- Red makeup with fiery expressions
- Represents aggressive characters

**Females (Minukku)**
- Gentle and graceful
- Radiant golden makeup
- Represents women and sacred characters

**Demons (Kari)**
- Dark evil characters
- Black makeup with fierce expressions
- Represents evil characters

## 5. Key Terminology

| Term | Definition |
|------|------------|
| Mudras | Symbolic hand gestures |
| Vesham | Makeup or costume |
| Chenda | Traditional percussion drum |
| Kathakali | Story-play (Katha + Kali) |

## 6. Summary

Kathakali represents the rich theatrical tradition of Kerala, combining dance, drama, music, and elaborate visual design.

## 7. Assessment

### Easy Questions
1. When did Kathakali develop?
2. What are the main character types?
3. What is the main percussion instrument?

### Medium Questions
1. Explain the key features of Kathakali.
2. Describe the different character types in Kathakali.

### Analytical Question
1. How does Kathakali combine various art forms to create a unique theatrical experience?

## 8. Learning Outcomes

- Define Kathakali and its origins
- Explain the key features and performance
- Analyze character types
- Compare with other dance forms
- Evaluate the artistic significance'''

    def _get_kathakali_module2(self):
        return '''# Makeup and Costumes

## 1. Introduction

Kathakali makeup (Vesham) is a complex art form that transforms performers into mythical characters. It requires skilled practitioners and takes several hours to complete.

## 2. Types of Makeup (Vesham)

**Pachcha (Green)**
- Used for noble heroes and deities
- Green face with white beard
- Represents divine and righteous characters

**Kathi (Knife)**
- Used for villains and hunters
- Red face with sharp features
- Represents aggressive and evil characters

**Minukku (Radiant)**
- Used for women and brahmin characters
- Golden/yellowish makeup
- Represents gentle and sacred characters

**Kari (Black)**
- Used for demon characters
- Black face with fierce expressions
- Represents evil characters

## 3. Costumes

**Headgear (Mukuthi)**
- Elaborate ornamental headpieces
- Made of metal and colorful decorations
- Can weigh several kilograms

**Skirts (Chakku)**
- Large colorful skirts
- Layered fabric
- Creates dramatic movement

**Body Ornaments**
- Chest plates (Chandadi)
- Arm ornaments (Kappu)
- Decorative belts

## 4. Face Paint

- Natural colors from plants and minerals
- Takes hours to apply
- Requires skilled practitioners

## 5. Training

**Physical Requirements**
- Years of rigorous training
- Flexibility exercises
- Dance techniques

**Learning Process**
- Begins at young age
- 7-10 years to become proficient
- Traditional Gurukula system

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Vesham | Makeup and costume |
| Mukuthi | Ornamental headgear |
| Chakku | Large decorative skirt |
| Chandadi | Chest plate decoration |

## 7. Summary

Kathakali makeup and costumes are integral to the art form, requiring specialized skills and transforming performers into larger-than-life characters.

## 8. Assessment

### Easy Questions
1. What are the types of Kathakali makeup?
2. What does Pachcha represent?
3. How long does training take?

### Medium Questions
1. Explain the different types of Vesham.
2. Describe the costume components.

### Analytical Question
1. How does the elaborate makeup and costume system enhance the storytelling in Kathakali?

## 9. Learning Outcomes

- Define the types of Kathakali makeup
- Explain costume components
- Analyze training requirements
- Compare character types
- Evaluate the artistic elements'''

    def _get_mohiniyattam_module1(self):
        return '''# Introduction to Mohiniyattam

## 1. Introduction

Mohiniyattam is the classical dance form of Kerala, known for its graceful, gentle, and flowing movements. It is one of the eight Indian classical dances.

## 2. Etymology

The name derives from:
- **Mohini** - The enchantress avatar of Vishnu
- **Attam** - Dance
Together meaning "Dance of the Enchantress"

## 3. Historical Background

**Origins**
- Mentioned in historical texts from the **16th century**
- Traditionally performed in temples
- Developed as a solo dance form

**Revival**
- Revived in the 19th century
- Recognized as one of the Indian classical dances
- Now performed on stage worldwide

## 4. Key Features

**Gentle Movements**
- Swaying movement (Sway)
- Graceful transitions
- Subtle expressions

**Costume**
- White with gold border (Kasavu)
- Traditional Kerala style
- Jasmine flowers in hair

**Makeup**
- Subtle and natural
- Emphasis on eyes
- Traditional application

## 5. Themes

**Religious Stories**
- Stories from Hindu mythology
- Themes of love and devotion
- Nature-inspired compositions

**Techniques**
- Hand gestures (Mudras)
- Eye expressions
- Body movements

## 6. Music

**Instruments**
- **Veena** - Primary melody
- **Mridangam** - Percussion
- **Idakka** - Drum
- **Cymbals**

**Vocal Style**
- Carnatic music tradition
- Malayalam lyrics
- Slow and graceful compositions

## 7. Key Terminology

| Term | Definition |
|------|------------|
| Mohini | Enchantress avatar of Vishnu |
| Kasavu | Gold border saree |
| Attam | Dance movement |
| Mudras | Hand gestures |

## 8. Summary

Mohiniyattam represents the gentle and graceful tradition of Kerala dance, characterized by flowing movements and elegant costumes.

## 9. Assessment

### Easy Questions
1. What does Mohiniyattam mean?
2. What is the costume called?
3. When did it originate?

### Medium Questions
1. Explain the key features of Mohiniyattam.
2. Describe the musical accompaniment.

### Analytical Question
1. How does Mohiniyattam differ from other Indian classical dance forms?

## 10. Learning Outcomes

- Define Mohiniyattam and its etymology
- Explain historical background
- Analyze key features
- Compare with Kathakali
- Evaluate the artistic significance'''

    def _get_mohiniyattam_module2(self):
        return '''# Techniques and Performance

## 1. Introduction

Mohiniyattam features specific techniques that create its distinctive graceful appearance. The dance form emphasizes subtle expressions and fluid movements.

## 2. Dance Techniques

**Body Positions**
- **Samapada** - Straight position
- **Aindala** - Diagonal stance
- **Pakka** - Side position

**Footwork**
- Subtle foot movements
- Rhythmic patterns
- Silent footwork

**Hand Gestures**
- 24 main Mudras
- Expressive storytelling
- Graceful transitions

**Expressions**
- **Abhinaya** - Expression
- Eye movements
- Subtle facial expressions

## 3. Performance

**Solo Performance**
- Duration: 1-2 hours
- One dancer on stage
- Live music accompaniment

**Costume Details**
- **Kasavu** - Golden border saree
- White and gold colors
- Traditional jewelry
- Jasmine flower garlands

**Hair**
- Traditional bun
- Jasmine flowers
- Traditional hair accessories

## 4. Training

**Physical Preparation**
- Flexibility exercises
- Body conditioning
- Strength building

**Years of Training**
- Minimum 7-10 years
- Begins at young age
- Under experienced teachers

**Certification**
- Recognized by government
- Cultural universities offer degrees
- Professional performing artists

## 5. Key Terminology

| Term | Definition |
|------|------------|
| Samapada | Straight body position |
| Abhinaya | Expression and emotion |
| Kasavu | Gold border saree |
| Mudras | Hand gestures |

## 6. Summary

Mohiniyattam requires years of dedicated training to master its subtle techniques and graceful expressions.

## 7. Assessment

### Easy Questions
1. What are the main body positions?
2. How many Mudras are there?
3. What is the costume called?

### Medium Questions
1. Explain the training process.
2. Describe the performance elements.

### Analytical Question
1. How do the techniques of Mohiniyattam reflect the aesthetic ideals of Kerala?

## 8. Learning Outcomes

- Define dance techniques
- Explain training requirements
- Analyze performance elements
- Compare with other dance forms
- Evaluate the artistry involved'''

    def _get_theyyam_module1(self):
        return '''# Introduction to Theyyam

## 1. Introduction

Theyyam is a ritual dance form performed in North Kerala, particularly in Kasaragod and Kannur districts. It is considered a **living tradition** dating back over 1,500 years.

## 2. Etymology

The word "Theyyam" comes from:
- **Daivam** - Meaning God
- Represents divine spirit possession

## 3. Historical Background

**Origins**
- Pre-historic ritual art form
- Over 1,500 years old
- Connected to tribal traditions

**Regional Significance**
- Performed in North Kerala
- Mainly in Kasaragod and Kannur
- Connected to village temples

## 4. Key Features

**Ritual Nature**
- Performed as a ritual to honor ancestral spirits
- Medium of communication with the divine
- Performed mainly during night in temples

**Spirit Possession**
- Performers become vessels for deities
- Divine spirit enters the performer
- Sacred ritual process

**Characters**
- **Sthanu** - Lord Shiva
- **Nair** - Warrior class
- **Kalari** - Temple guards
- **Vishu** - Lord Vishnu

## 5. Performance Season

**Theyyam Season**
- October to May
- During temple festivals
- Full moon nights important

**Types**
- **Sthana Theyyam** - Standing pose
- **Vartha Theyyam** - Moving pose
- **Pooththara Theyyam** - With props

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Daivam | God or divine |
| Theyyam | Divine spirit |
| Kalari | Temple or training center |
| Thappu | Traditional drum |

## 7. Summary

Theyyam is a unique ritual art form that combines dance, music, and spiritual possession in a living tradition.

## 8. Assessment

### Easy Questions
1. What does Theyyam mean?
2. Where is it performed?
3. How old is the tradition?

### Medium Questions
1. Explain the ritual nature of Theyyam.
2. Describe the spirit possession aspect.

### Analytical Question
1. How does Theyyam preserve the ancient traditions of North Kerala?

## 9. Learning Outcomes

- Define Theyyam and its origins
- Explain key features
- Analyze the ritual aspects
- Compare with other dance forms
- Evaluate cultural significance'''

    def _get_theyyam_module2(self):
        return '''# Makeup and Rituals

## 1. Introduction

Theyyam makeup and rituals are central to the performance, transforming ordinary individuals into divine vessels through elaborate processes.

## 2. Theyyam Makeup

**Process**
- Takes several hours
- Natural colors from herbs
- Traditional techniques

**Colors**
- White - Purity
- Red - Valor
- Black - Power
- Yellow - Divinity

**Props**
- Headdresses
- Body decorations
- Traditional weapons

## 3. Ritual Process

**Preparation**
- Fasting by performer
- Purification rituals
- Prayers to deities

**Transformation**
- Makeup application
- Costume wearing
- Ritual prayers

**Performance**
- Entering trance state
- Dancing to drums
- Blessing devotees

## 4. Music and Drums

**Instruments**
- **Thappu** - Main drum
- **Elathalam** - Cymbals
- **Kuzhal** - Wind instrument

**Rhythms**
- Traditional patterns
- Hypnotic beats
- Sacred rhythms

## 5. Cultural Significance

**Community Role**
- Brings community together
- Preserves ancient traditions
- Connects people with roots

**Preservation**
- Government recognition
- Cultural festivals
- Documentation efforts

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Thappu | Main percussion drum |
| Elathalam | Cymbals |
| Kuzhal | Wind instrument |
| Thottam | Sacred chants |

## 7. Summary

Theyyam makeup and rituals represent a complex system of transformation that bridges the human and divine realms.

## 8. Assessment

### Easy Questions
1. What colors are used in Theyyam?
2. How long does makeup take?
3. What is the main drum?

### Medium Questions
1. Explain the ritual process.
2. Describe the music accompaniment.

### Analytical Question
1. How do the elaborate makeup and rituals of Theyyam serve the spiritual needs of the community?

## 9. Learning Outcomes

- Define the makeup process
- Explain ritual procedures
- Analyze cultural significance
- Compare with other art forms
- Evaluate preservation efforts'''

    def _get_kalaripayattu_module1(self):
        return '''# Introduction to Kalaripayattu

## 1. Introduction

Kalaripayattu is the oldest martial art form in India, originating from Kerala. It is often called the **"Mother of All Martial Arts."**

## 2. Historical Background

**Origins**
- Origins dating back to **3rd century CE**
- Developed in Kerala's ancient martial training centers called "Kalaris"
- Mentioned in ancient texts like the Vedas and Ramayana

**Regional Spread**
- Originated in Kerala
- Spread to Tamil Nadu and Karnataka
- Influenced Southeast Asian martial arts

## 3. Key Features

**Comprehensive System**
- Strikes and kicks
- Grappling techniques
- Weapon training
- Self-defense

**Physical Training**
- Flexibility exercises
- Strength training
- Endurance building
- Mental discipline

**Weapons Training**
- **Sword** - Vel
- **Spear** - Kol
- **Shield** - Pa
- **Mace** - Gada

## 4. The Kalari

**Training Center**
- Traditional martial arts school
- Sacred space
- Gurukula system

**Guru**
- Master teacher
- Transfers knowledge
- Spiritual guide

## 5. Philosophy

**Mind-Body Connection**
- Mental discipline
- Spiritual development
- Character building

**Varmakalai**
- Study of vital points
- Pressure point attacks
- Healing techniques

## 6. Key Terminology

| Term | Definition |
|------|------------|
| Kalari | Martial arts training center |
| Guru | Master teacher |
| Vel | Sword |
| Varmakalai | Art of vital points |

## 7. Summary

Kalaripayattu represents Indias ancient martial tradition, combining physical combat with spiritual development.

## 8. Assessment

### Easy Questions
1. When did Kalaripayattu originate?
2. What is the training center called?
3. What are the weapons?

### Medium Questions
1. Explain the key features.
2. Describe the philosophy.

### Analytical Question
1. How does Kalaripayattu influence modern martial arts?

## 9. Learning Outcomes

- Define Kalaripayattu and origins
- Explain key features
- Analyze the philosophical aspects
- Compare with other martial arts
- Evaluate historical significance'''

    def _get_kalaripayattu_module2(self):
        return '''# Training and Techniques

## 1. Introduction

Kalaripayattu training is a comprehensive system that develops physical fitness, combat skills, and mental discipline through traditional methods.

## 2. Training System

**Beginner's Level**
- Physical conditioning
- Basic movements
- Flexibility exercises

**Intermediate Level**
- Advanced techniques
- Weapon training
- Sparring practice

**Advanced Level**
- Mastery of all techniques
- Teaching skills
- Spiritual advancement

## 3. Techniques

**Strikes**
- Punches
- Elbow strikes
- Knee strikes
- Palm strikes

**Kicks**
- Front kick
- Roundhouse kick
- Side kick
- Spinning kicks

**Grappling**
- Joint locks
- Throws
- Ground fighting
- Escapes

**Weapons**
- Single sword
- Double swords
- Spear
- Shield and sword

## 4. Modern Relevance

**Fitness**
- Full body workout
- Flexibility
- Self-defense

**Wellness**
- Stress relief
- Mental clarity
- Physical health

**Cultural Preservation**
- UNESCO recognition
- Global awareness
- Traditional schools

## 5. Key Terminology

| Term | Definition |
|------|------------|
| Meipayattu | Body exercises |
| Verumkai | Empty hand techniques |
| Aagaram | Stances |
| Kalari | Training center |

## 6. Summary

Kalaripayattu training encompasses a comprehensive system that prepares practitioners for combat while promoting overall wellness.

## 7. Assessment

### Easy Questions
1. What are the training levels?
2. What are the weapon types?
3. What are the striking techniques?

### Medium Questions
1. Explain the training progression.
2. Describe the modern applications.

### Analytical Question
1. How does Kalaripayattu training promote both physical and mental well-being?

## 8. Learning Outcomes

- Define training techniques
- Explain progression system
- Analyze modern applications
- Compare with other martial arts
- Evaluate the comprehensive nature'''
