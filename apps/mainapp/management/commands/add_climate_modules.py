from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial

class Command(BaseCommand):
    help = 'Add Climate Change and Wildlife Protection sub-modules'

    def handle(self, *args, **options):
        # Get the Environment section
        env_section = Section.objects.get(name='Environment')
        
        # ========================================
        # CLIMATE CHANGE - MODULE 1: Understanding
        # ========================================
        climate_change, _ = Topic.objects.get_or_create(
            name='Climate Change',
            section=env_section,
            defaults={
                'description': 'Learn about the causes and effects of climate change on our planet.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Global_warming_map.jpg/1200px-Global_warming_map.jpg',
                'order': 2
            }
        )
        
        # Delete existing study materials for Climate Change to rebuild
        climate_change.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=climate_change,
            title='Module 1: Understanding Climate Change',
            content_text='''Understanding Climate Change

Climate change refers to **long-term shifts in global temperatures and weather patterns**. While natural factors can cause climate variations, human activities have been the primary driver since the Industrial Revolution.

 What is Climate Change?

Climate change is a significant and lasting change in the statistical distribution of weather patterns over periods ranging from decades to millions of years. It may be a change in the average weather conditions or in the distribution of weather around the average conditions.

 Key Facts

- **Global average temperature** has increased by about 1.1°C since the late 19th century
- **CO2 levels** have reached over 420 ppm (parts per million) - the highest in 2 million years
- **Sea levels** are rising due to melting ice caps and thermal expansion
- **Weather extremes** are becoming more frequent and intense

 Causes of Climate Change

 Natural Causes
- Volcanic eruptions
- Solar radiation variations
- Ocean current changes

 Human Causes (Primary Driver)
- **Burning fossil fuels** - coal, oil, and natural gas
- **Deforestation** - reduces carbon absorption
- **Industrial processes** - release greenhouse gases
- **Agriculture** - methane from livestock and rice paddies

 The Greenhouse Effect

The greenhouse effect is a natural process that warms the Earth's surface. When sunlight reaches Earth, some is reflected back to space, and some is absorbed and re-radiated as heat. Greenhouse gases in the atmosphere trap some of this heat, keeping the Earth warm enough to support life.

However, human activities have increased greenhouse gas concentrations, intensifying the natural greenhouse effect and causing global warming.

## Evidence of Climate Change

1. **Rising temperatures** - Each decade since 1980 has been warmer than the preceding one
2. **Melting ice caps** - Arctic sea ice is declining
3. **Sea level rise** - Oceans are expanding as they warm
4. **Changing precipitation** - Some areas getting wetter, others drier
5. **Ocean acidification** - CO2 dissolving in oceans making them more acidic''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Pasterze_Glacier_2015.jpg/1200px-Pasterze_Glacier_2015.jpg',
            order=1
        )
        
        # Climate Change Module 2: Impact and Mitigation
        StudyMaterial.objects.create(
            topic=climate_change,
            title='Module 2: Impact and Mitigation',
            content_text='''Impact and Mitigation

 Impacts of Climate Change

 Environmental Impacts

 Ecosystem Disruption
- Species forced to migrate to cooler areas
- Coral bleaching due to warmer oceans
- Loss of biodiversity as habitats change faster than species can adapt

 Extreme Weather Events
- More frequent and intense hurricanes and cyclones
- Increased flooding in some regions
- More severe droughts in other areas

 Sea Level Rise
- Threat to coastal cities and islands
- Saltwater intrusion into freshwater sources
- Loss of coastal wetlands

 Social Impacts

 Food Security
- Changes in agricultural patterns
- Crop failures due to extreme weather
- Water scarcity affecting food production

 Health Impacts
- Spread of diseases to new areas
- Heat-related illnesses
- Air quality deterioration

 Economic Impacts
- Damage to infrastructure from extreme weather
- Costs of adaptation and mitigation
- Displacement of populations

 Mitigation Strategies

 Reducing Emissions

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

 Adaptation Strategies

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

 What Can Individuals Do?

- Reduce energy consumption
- Use public transportation
- Plant trees
- Reduce, reuse, recycle
- Support renewable energy
- Educate others about climate change''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Climate_change_impact.jpg/1200px-Climate_change_impact.jpg',
            order=2
        )
        
        # ========================================
        # WILDLIFE PROTECTION - EXPANDED TOPICS
        # ========================================
        wildlife_protection, _ = Topic.objects.get_or_create(
            name='Wildlife Protection',
            section=env_section,
            defaults={
                'description': 'Discover efforts to protect endangered wildlife and their habitats.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
                'order': 3
            }
        )
        
        # Delete existing study materials for Wildlife Protection to rebuild
        wildlife_protection.study_materials.all().delete()
        
        # Wildlife Protection Module 1
        StudyMaterial.objects.create(
            topic=wildlife_protection,
            title='Module 1: Wildlife Conservation in India',
            content_text='''Wildlife Conservation in India

India is home to diverse wildlife and has implemented various conservation measures to protect its rich biodiversity.

 Conservation Network

 Protected Areas
- **Wildlife Sanctuaries**: Over 550 wildlife sanctuaries
- **National Parks**: More than 100 national parks covering various ecosystems
- **Tiger Reserves**: Over 50 tiger reserves under Project Tiger
- **Conservation Reserves**: Over 100 conservation reserves

 Major National Parks
- **Kanha National Park** - Madhya Pradesh
- **Jim Corbett National Park** - Uttarakhand (oldest national park in India)
- **Kaziranga National Park** - Assam (one-horned rhinoceros)
- **Sundarbans National Park** - West Bengal (Bengal tigers)
- **Periyar National Park** - Kerala
- **Bandipur National Park** - Karnataka
- **Silent Valley National Park** - Kerala

 Conservation Projects

 Project Tiger
Launched in **1973**, Project Tiger is one of the most successful conservation programs in the world:
- Aims to save the endangered Bengal tiger
- Covers over 50 tiger reserves across India
- Focuses on habitat protection and anti-poaching measures
- Has helped increase tiger population from about 1,400 in 1973 to over 3,000 today

 Project Elephant
Launched in **1992** to protect elephants:
- Covers elephant reserves across India
- Focuses on habitat conservation
- Addresses human-elephant conflict
- Protects migration corridors

 India's Iconic Wildlife

 Mammals
- **Bengal Tiger** - National animal
- **Asiatic Lion** - Found only in Gir Forest
- **Indian Elephant** - Endangered species
- **One-horned Rhinoceros** - Found in Assam
- **Snow Leopard** - Found in Himalayan regions

 Birds
- **Peacock** - National bird
- **Great Indian Bustard** - Critically endangered
- **Sarus Crane** - State bird of Uttar Pradesh

 Reptiles
- **King Cobra** - World's longest venomous snake
- **Indian Python**
- **Marine Turtle**''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
            order=1
        )
        
        # Wildlife Protection Module 2
        StudyMaterial.objects.create(
            topic=wildlife_protection,
            title='Module 2: Endangered Species',
            content_text='''Endangered Species

An endangered species is a species that is at risk of becoming extinct because of low population numbers or threats to its habitat.

## IUCN Red List Categories

1. **Extinct (EX)** - No individuals remain
2. **Extinct in the Wild (EW)** - Only survives in captivity
3. **Critically Endangered (CR)** - Extremely high risk of extinction
4. **Endangered (EN)** - Very high risk of extinction
5. **Vulnerable (VU)** - High risk of extinction
6. **Near Threatened (NT)** - Likely to become threatened
7. **Least Concern (LC)** - Lowest risk

 Critically Endangered Species in India

 Mammals
- **Asiatic Lion** - Only about 700 individuals left, found only in Gujarat
- **Bengal Tiger** - About 3,000 individuals, endangered due to habitat loss
- **Snow Leopard** - About 500-700 individuals in Himalayas
- **One-horned Rhinoceros** - About 3,500 individuals, recovering due to conservation

 Birds
- **Great Indian Bustard** - Less than 150 individuals
- **White-rumped Vulture** - Near total extinction from diclofenac poisoning
- **Himalayan Quail** - Possibly extinct, not seen since 1900

 Marine Species
- **Hawksbill Turtle** - Threatened by habitat loss
- **Whale Shark** - Largest fish, threatened by fishing
- **Ganges River Dolphin** - About 1,200-1,500 individuals

 Threats to Wildlife

 Habitat Loss
- Deforestation for agriculture
- Urban expansion
- Mining activities

 Poaching
- Illegal wildlife trade
- Trophy hunting
- Traditional medicine

 Pollution
- Plastic waste in oceans
- Chemical contamination
- Climate change

 Human-Wildlife Conflict
- Crop raiding by elephants
- Livestock predation by leopards
- Human casualties leading to retaliatory killings

Conservation Success Stories

 Indian Rhino
- Population has increased from 200 in 1975 to over 3,500 today
- Successfully translocated to new habitats

 Bengal Tiger
- Population increased from 1,400 in 1973 to over 3,000 today
- India now has 70% of world's tigers

 Olive Ridley Turtle
- Mass nesting protection programs
- Reduced mortality from fishing nets

 How to Help

- Support wildlife conservation organizations
- Report poaching incidents
- Reduce consumption of wildlife products
- Support sustainable practices
- Educate others about wildlife conservation''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Asiatic_Lion.jpg/1200px-Asiatic_Lion.jpg',
            order=2
        )
        
        self.stdout.write(self.style.SUCCESS('Climate Change and Wildlife Protection sub-modules added successfully!'))
