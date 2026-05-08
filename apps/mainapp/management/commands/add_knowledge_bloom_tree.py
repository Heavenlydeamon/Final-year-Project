from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial


class Command(BaseCommand):
    help = 'Add Knowledge Bloom tree structure - parent-child topic relationships for skill tree visualization'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Building Knowledge Bloom tree structure...'))
        
        # Get the Environment section
        env_section = Section.objects.filter(name='Environment').first()
        if not env_section:
            self.stdout.write(self.style.ERROR('Environment section not found! Run add_sample_data first.'))
            return
        
        # ========================================
        # ENVIRONMENT SECTION - Knowledge Tree
        # ========================================
        
        # Root topic 1: Western Ghats (already exists)
        western_ghats = Topic.objects.filter(
            section=env_section, 
            name='Western Ghats'
        ).first()
        
        if western_ghats:
            # Create child topics for Western Ghats
            self._create_child_topic(
                parent=western_ghats,
                name='Physical Geography',
                description='Learn about the formation and geography of the Western Ghats mountain range.',
                order=1,
                content_title='Physical Geography of Western Ghats',
                content_text='''Physical Geography of Western Ghats

The Western Ghats, also known as the Sahyadri, is a mountain range that runs parallel to the western coast of India.

Formation
The Western Ghats were formed during the break-up of the supercontinent Gondwana approximately 150 million years ago. This makes them one of the oldest mountain ranges in the world.

Geographic Extent
The range stretches from the Tapi River in Gujarat to Kanyakumari in Tamil Nadu, covering six states: Gujarat, Maharashtra, Goa, Karnataka, Kerala, and Tamil Nadu.

Highest Peak
Anamudi (2,695m) in Kerala is the highest peak south of the Himalayas, often called the "Everest of South India".

Climate Role
The Western Ghats act as a barrier to the southwest monsoon, causing heavy rainfall on western slopes and creating the lush rainforests Kerala is known for.'''
            )
            
            self._create_child_topic(
                parent=western_ghats,
                name='Biodiversity',
                description='Discover the rich biodiversity and endemic species of the Western Ghats.',
                order=2,
                content_title='Biodiversity of Western Ghats',
                content_text='''Biodiversity of Western Ghats

The Western Ghats is one of the eight hottest biodiversity hotspots in the world, with over 7,000 species of flowering plants.

Endemic Species
The region has incredibly high endemism:
- Over 1,500 species of endemic flowering plants
- Over 150 species of endemic reptiles
- Over 100 species of endemic amphibians

Flagship Species
- Nilgiri Tahr: Endangered mountain goat, state animal of Tamil Nadu and Kerala
- Lion-tailed Macaque: One of the rarest primates, lives exclusively in Western Ghats rainforests
- Malabar Giant Squirrel: One of the largest squirrel species in the world
- Neelakurinji: Blooms once every 12 years, turning hills purple'''
            )
            
            self._create_child_topic(
                parent=western_ghats,
                name='Hydrology',
                description='Explore the rivers and water resources originating from the Western Ghats.',
                order=3,
                content_title='Water Resources of Western Ghats',
                content_text='''Water Resources of Western Ghats

The Western Ghats are the "Water Tower" of peninsular India, feeding major river systems.

Major Rivers
- Periyar: Longest river in Kerala
- Bharatapuzha: Known as River of Heaven
- Pamba River: Flows through the heart of Kerala
- Godavari, Krishna, Kaveri: Major interstate rivers

Ecosystem Services
- Carbon sequestration by forests
- Soil conservation
- Groundwater recharge
- Habitat for aquatic species

Over 500 million people depend on rivers originating from the Western Ghats.'''
            )
            
            self._create_child_topic(
                parent=western_ghats,
                name='Conservation',
                description='Learn about threats to the Western Ghats and conservation efforts.',
                order=4,
                content_title='Conservation of Western Ghats',
                content_text='''Conservation of Western Ghats

Despite UNESCO World Heritage status (2012), the Western Ghats face severe environmental threats.

Key Threats
1. Deforestation for plantations
2. Mining activities
3. Climate change
4. Infrastructure development

Conservation Reports
- Gadgil Report (2011): Called for entire Ghats to be Ecologically Sensitive Area
- Kasturirangan Report (2013): Suggested 37% coverage as ESA

Conservation Efforts
- Project Elephant and Project Tiger
- National parks and wildlife sanctuaries
- Community-based conservation initiatives'''
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created children for Western Ghats'))
        
        # Root topic 2: Climate Change
        climate_change = Topic.objects.filter(
            section=env_section, 
            name='Climate Change'
        ).first()
        
        if climate_change:
            self._create_child_topic(
                parent=climate_change,
                name='Understanding Climate',
                description='Learn the basics of climate change and its causes.',
                order=1,
                content_title='Understanding Climate Change',
                content_text='''Understanding Climate Change

Climate change refers to long-term shifts in global temperatures and weather patterns.

Key Facts
- Global temperature increased by 1.1°C since late 19th century
- CO2 levels over 420 ppm - highest in 2 million years
- Sea levels rising due to melting ice caps

Causes
Natural: Volcanic eruptions, solar variations, ocean currents
Human (Primary): Burning fossil fuels, deforestation, industrial processes

The Greenhouse Effect
Greenhouse gases trap heat in the atmosphere, warming Earth. Human activities have intensified this natural process.'''
            )
            
            self._create_child_topic(
                parent=climate_change,
                name='Climate Impacts',
                description='Discover the environmental and social impacts of climate change.',
                order=2,
                content_title='Impacts of Climate Change',
                content_text='''Impacts of Climate Change

Environmental Impacts
- Ecosystem disruption and species migration
- Coral bleaching
- Extreme weather events
- Sea level rise

Social Impacts
- Food security issues
- Health impacts
- Economic losses
- Population displacement

Future projections indicate these impacts will intensify without mitigation.'''
            )
            
            self._create_child_topic(
                parent=climate_change,
                name='Climate Solutions',
                description='Explore mitigation and adaptation strategies for climate change.',
                order=3,
                content_title='Solutions to Climate Change',
                content_text='''Solutions to Climate Change

Mitigation Strategies
- Transition to renewable energy (solar, wind)
- Energy efficiency improvements
- Carbon capture and storage
- Reforestation

Adaptation Strategies
- Building climate-resilient infrastructure
- Developing drought-resistant crops
- Improving water management
- Disaster preparedness

Individual Actions
- Reduce energy consumption
- Use public transportation
- Reduce, reuse, recycle
- Support renewable energy'''
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created children for Climate Change'))
        
        # Root topic 3: Wildlife Protection
        wildlife_protection = Topic.objects.filter(
            section=env_section, 
            name='Wildlife Protection'
        ).first()
        
        if wildlife_protection:
            self._create_child_topic(
                parent=wildlife_protection,
                name='Conservation efforts',
                description='Learn about wildlife conservation in India.',
                order=1,
                content_title='Wildlife Conservation in India',
                content_text='''Wildlife Conservation in India

India is home to diverse wildlife with extensive conservation measures.

Protected Areas
- Over 550 wildlife sanctuaries
- More than 100 national parks
- Over 50 tiger reserves

Major Projects
Project Tiger (1973): Increased tiger population from 1,400 to over 3,000
Project Elephant (1992): Protects elephant habitats and migration corridors

Iconic Species
- Bengal Tiger: National animal
- Asiatic Lion: Found only in Gir Forest
- Indian Elephant: Endangered species
- Peacock: National bird'''
            )
            
            self._create_child_topic(
                parent=wildlife_protection,
                name='Endangered Species',
                description='Learn about endangered species and conservation success stories.',
                order=2,
                content_title='Endangered Species',
                content_text='''Endangered Species

IUCN Red List Categories
- Extinct (EX)
- Extinct in the Wild (EW)
- Critically Endangered (CR)
- Endangered (EN)
- Vulnerable (VU)

Critically Endangered in India
- Asiatic Lion: About 700 individuals
- Bengal Tiger: About 3,000 individuals
- Snow Leopard: 500-700 individuals
- Great Indian Bustard: Less than 150

Success Stories
- Indian Rhino: Increased from 200 to over 3,500
- Bengal Tiger: Population tripled since 1973'''
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created children for Wildlife Protection'))
        
        # ========================================
        # HERITAGE SECTION - Knowledge Tree
        # ========================================
        
        heritage_section = Section.objects.filter(name='Heritage Sites').first()
        
        if heritage_section:
            # Fort Kochi
            fort_kochi = Topic.objects.filter(
                section=heritage_section, 
                name='Fort Kochi'
            ).first()
            
            if fort_kochi:
                self._create_child_topic(
                    parent=fort_kochi,
                    name='Colonial History',
                    description='Explore the colonial history of Fort Kochi.',
                    order=1,
                    content_title='Colonial History of Fort Kochi',
                    content_text='''Colonial History of Fort Kochi

Fort Kochi has been a center of trade for centuries with a rich colonial heritage.

Timeline
- 1503: Portuguese build first European fort in India
- 1663: Dutch capture and develop the area
- 1795: British take control
- 1947: Indian independence

Key Landmarks
- St. Francis Church (1503): Oldest European church in India
- Santa Cruz Basilica: Gothic architecture
- Chinese Fishing Nets: Introduced by traders'''
                )
                
                self._create_child_topic(
                    parent=fort_kochi,
                    name='Cultural Fusion',
                    description='Discover the unique cultural blend in Fort Kochi.',
                    order=2,
                    content_title='Cultural Fusion in Fort Kochi',
                    content_text='''Cultural Fusion in Fort Kochi

Fort Kochi represents a unique blend of various cultures.

Portuguese Influence
- First European settlement in India
- Introduced Christianity

Dutch Influence
- Built Dutch Palace
- Established spice trade

Jewish Influence
- Paradesi Synagogue: Oldest active synagogue in Commonwealth
- Jew Street and antique markets

Modern Significance
- Kochi-Muziris Biennale
- Blend of colonial and modern architecture'''
                )
                
                self.stdout.write(self.style.SUCCESS(f'Created children for Fort Kochi'))
            
            # Padmanabhapuram Palace
            padmanabhapuram = Topic.objects.filter(
                section=heritage_section, 
                name='Padmanabhapuram Palace'
            ).first()
            
            if padmanabhapuram:
                self._create_child_topic(
                    parent=padmanabhapuram,
                    name='Palace History',
                    description='Learn about the history of Padmanabhapuram Palace.',
                    order=1,
                    content_title='History of Padmanabhapuram Palace',
                    content_text='''History of Padmanabhapuram Palace

Padmanabhapuram Palace is one of the oldest wooden palaces in the world.

Historical Background
- Built around 1550 AD
- Residence of Travancore rulers
- Capital of Venad kingdom before Thiruvananthapuram
- Maintained by Archaeological Survey of India

Notable Rulers
- Marthanda Varma (1729-1758): Founded modern Travancore
- Karthika Thirunal: Known for reforms'''
                )
                
                self._create_child_topic(
                    parent=padmanabhapuram,
                    name='Architecture',
                    description='Discover the unique architecture of the palace.',
                    order=2,
                    content_title='Architecture of Padmanabhapuram Palace',
                    content_text='''Architecture of Padmanabhapuram Palace

The palace represents traditional Kerala architecture at its finest.

Construction
- Made entirely of wood (teak, rosewood, coconut)
- No iron nails - only wooden pins
- Earthquake-resistant design

Notable Features
- Exquisite murals over 400 years old
- Natural cooling systems
- Rainwater harvesting

Sections
- Mantrasala: King's council chamber
- Nalukettu: Traditional four-hall structure
- Theppakavu: Boat house for ceremonies'''
                )
                
                self.stdout.write(self.style.SUCCESS(f'Created children for Padmanabhapuram Palace'))
        
        # ========================================
        # CULTURAL SECTION - Knowledge Tree
        # ========================================
        
        cultural_section = Section.objects.filter(name='Cultural Artforms').first()
        
        if cultural_section:
            # Get existing cultural topics
            cultural_topics = Topic.objects.filter(section=cultural_section)
            
            for topic in cultural_topics:
                # Create a child topic for each main cultural topic
                self._create_child_topic(
                    parent=topic,
                    name='Overview',
                    description=f'Introduction to {topic.name}.',
                    order=1,
                    content_title=f'Introduction to {topic.name}',
                    content_text=f'''{topic.name}

This module provides an introduction to {topic.name} from Kerala's rich cultural heritage.

Learning Objectives
- Understand the historical significance
- Learn about the cultural importance
- Discover the unique characteristics

Key Concepts
- Historical background
- Cultural context
- Modern relevance'''
                )
                
                self._create_child_topic(
                    parent=topic,
                    name='Cultural Significance',
                    description=f'Learn about the cultural significance of {topic.name}.',
                    order=2,
                    content_title=f'Cultural Significance of {topic.name}',
                    content_text=f'''Cultural Significance of {topic.name}

{topic.name} plays an important role in Kerala's cultural identity.

Cultural Importance
- Represents Kerala's artistic heritage
- Preserves traditional knowledge
- Connects past and present

Modern Relevance
- Continues to be performed/celebrated
- Tourism and cultural identity
- Educational value'''
                )
            
            if cultural_topics.count() > 0:
                self.stdout.write(self.style.SUCCESS(f'Created children for {cultural_topics.count()} cultural topics'))
        
        # Summary
        root_topics = Topic.objects.filter(parent_topic__isnull=True, is_general=True).count()
        child_topics = Topic.objects.filter(parent_topic__isnull=False).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nKnowledge Bloom tree created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Root topics: {root_topics}'))
        self.stdout.write(self.style.SUCCESS(f'Child topics: {child_topics}'))
    
    def _create_child_topic(self, parent, name, description, order, content_title, content_text):
        """Helper method to create a child topic with study material"""
        topic, created = Topic.objects.get_or_create(
            name=name,
            parent_topic=parent,
            defaults={
                'section': parent.section,
                'description': description,
                'order': order,
                'is_general': True
            }
        )
        
        if created:
            # Add study material for this child topic
            StudyMaterial.objects.get_or_create(
                topic=topic,
                title=content_title,
                defaults={
                    'content_text': content_text,
                    'order': 1
                }
            )
        
        return topic

