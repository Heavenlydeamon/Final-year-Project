from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial

class Command(BaseCommand):
    help = 'Add Heritage Sites sub-modules with proper content structure'

    def handle(self, *args, **options):
        # Get the Heritage section
        heritage_section, _ = Section.objects.get_or_create(
            name='Heritage Sites',
            defaults={
                'description': 'Explore historical heritage sites and their significance.',
            }
        )
        
        # ========================================
        # BEKAL FORT - 2 MODULES
        # ========================================
        bekal_fort, _ = Topic.objects.get_or_create(
            name='Bekal Fort',
            section=heritage_section,
            defaults={
                'description': 'Learn about the largest fort in Kerala, built by the Shivappa Nayaka.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Bekal_Fort.jpg/1200px-Bekal_Fort.jpg',
                'order': 3
            }
        )
        
        bekal_fort.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=bekal_fort,
            title='Module 1: Bekal Fort - History',
            content_text='''# Bekal Fort - The Largest Fort in Kerala

Bekal Fort is the **largest fort in Kerala**, spanning 40 acres along the Arabian Sea coast in Kasaragod district.

## Historical Background

### Construction
- Built by **Shivappa Nayaka** of the Keladi Nayaka dynasty in the **17th century**
- Originally constructed as a key defense outpost
- Later modified by the British during their rule

### Location
- Located in **Kasaragod district**, northernmost district of Kerala
- Situated on the Arabian Sea coast
- About 12 km from Kasaragod town

## Historical Significance

### Strategic Importance
- Key defense outpost against invading forces
- Protected the northern trade routes
- Offered panoramic views of the Arabian Sea
- Had underground tunnels and secret passages

### Cultural Significance
- Featured in the famous Malayalam movie "Kamal" (1994)
- Symbol of Kerala's martial tradition
- Important archaeological site

## Features of the Fort

### Architecture
- Built using laterite stones
- Massive walls rising from the sea
- Observation towers
- Secret tunnels
- Storehouses for weapons

### Surroundings
- Beautiful beach
- Rocky coastline
- Lush green surroundings
- Scenic views

## Today

The fort is maintained by the Archaeological Survey of India:
- Popular tourist destination
- Sunrise and sunset point
- Photography hotspot
- Historical significance''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Bekal_Fort.jpg/1200px-Bekal_Fort.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=bekal_fort,
            title='Module 2: Bekal Fort - Architecture',
            content_text='''# Architecture of Bekal Fort

Bekal Fort showcases the architectural brilliance of the Keladi Nayakas.

## Construction Materials

### Laterite Stone
- Primary building material
- Known for durability
- Reddish-brown color
- Abundant in the region

## Structural Features

### Walls
- Massive fort walls
- About 30-40 feet high
- Thick base for stability

### Towers
- Multiple observation towers
- Strategic placement
- Sea view vantage points

### Underground Features
- Secret tunnels
- Underground chambers
- Escape routes

## Preservation

The Archaeological Survey of India maintains the fort:
- Regular restoration
- Protected monument
- Tourist facilities

## Visitor Information

- Open to public
- Best time to visit: October to March
- Photography allowed
- Guide services available''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Bekal_Fort.jpg/1200px-Bekal_Fort.jpg',
            order=2
        )
        
        # ========================================
        # SREE PADMANABHASWAMY TEMPLE - 2 MODULES
        # ========================================
        padmanabhaswamy, _ = Topic.objects.get_or_create(
            name='Sree Padmanabhaswamy Temple',
            section=heritage_section,
            defaults={
                'description': 'Explore the magnificent temple known for its rich architecture and massive treasure.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Padmanabhaswamy_Temple_TVM.jpg/1200px-Padmanabhaswamy_Temple_TVM.jpg',
                'order': 4
            }
        )
        
        padmanabhaswamy.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=padmanabhaswamy,
            title='Module 1: History and Significance',
            content_text='''# Sree Padmanabhaswamy Temple

Sree Padmanabhaswamy Temple is a famous Hindu temple located in **Thiruvananthapuram**, the capital city of Kerala.

## Historical Background

### Origin
- Built in the **16th century** by the Venad kingdom
- The current structure was renovated by Marthanda Varma
- Named after Lord Vishnu who is seen reclining on Anantha (the cosmic serpent)

### Royal Connection
- The temple is the spiritual center of the Travancore royal family
- The maharaja of Travancore is the chief trustee
- Temple has deep connections with the royal family

## Discovery of Treasure

In 2011, the temple gained international attention when massive treasure was discovered in its vaults:
- Estimated value: Over $22 billion
- Included gold, diamonds, rubies, and ancient coins
- Largest temple treasure find in Indian history

## Key Features

### Architecture
- Classic Kerala architectural style
- Massive gopuram (tower)
- Stone carvings
- Beautiful murals

### Deities
- **Lord Vishnu** - Main deity (Anantha Padmanabhaswamy)
- **Lord Shiva** - Subsidiary deity
- **Goddess Parvati** - Subsidiary deity''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Padmanabhaswamy_Temple_TVM.jpg/1200px-Padmanabhaswamy_Temple_TVM.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=padmanabhaswamy,
            title='Module 2: Architecture and Worship',
            content_text='''# Architecture and Worship

## Temple Architecture

### The Sanctum Sanctorum
- The innermost chamber where Lord Vishnu is enshrined
- Known as the "Anantha Shayanam" posture
- Vishnu is seen lying on the cosmic serpent Anantha

### The Gopuram
- Massive entrance tower
- Intricate carvings
- Colorful paintings

### The Corridor
- Famous 100-pillared corridor
- Each pillar has intricate carvings
- Perfect acoustics

## Religious Significance

### Important Festival
- **Arattu** - The annual ritual bathing ceremony
- **Navaratri** - Nine nights of goddess worship
- **Thiruvanchikulam** - Monthly ritual

### Worship Practices
- devotees offer various items
- Traditional Kerala rituals
- Special poojas on auspicious days

## Management

### Trust Structure
- Travancore royal family as chief trustees
- Temple trust manages finances
- Archaeological Survey of India monitors preservation

## Visitor Information

- Non-Hindus not allowed inside
- Strict dress code
- Photography prohibited inside
- Best time to visit: Morning hours''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Padmanabhaswamy_Temple_TVM.jpg/1200px-Padmanabhaswamy_Temple_TVM.jpg',
            order=2
        )
        
        # ========================================
        # HILL PALACE MUSEUM - 2 MODULES
        # ========================================
        hill_palace, _ = Topic.objects.get_or_create(
            name='Hill Palace Museum',
            section=heritage_section,
            defaults={
                'description': 'Visit the largest archaeological museum in Kerala, once the royal house of the Cochin royal family.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Hill_Palace_Museum.jpg/1200px-Hill_Palace_Museum.jpg',
                'order': 5
            }
        )
        
        hill_palace.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=hill_palace,
            title='Module 1: History of Hill Palace',
            content_text='''# Hill Palace Museum

The Hill Palace Museum in Tripunithura is the **largest archaeological museum in Kerala**.

## Historical Background

### Construction
- Built in **1865** by the Cochin royal family
- Served as the residence of the Cochin Maharaja
- Later converted into a museum in 1980

### Royal Connection
- Residence of the Cochin royal family
- Witnessed many historical events
- Center of cultural activities

## Location
- Located in **Tripunithura**, Ernakulam district
- About 10 km from Ernakulam
- Situated on a small hillock

## Significance

### Historical Importance
- One of the oldest heritage buildings in Kerala
- Preserves Cochin royal history
- Archaeological treasure trove

### Cultural Hub
- Houses rare artifacts
- Preserves traditional art forms
- Educational center for students''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Hill_Palace_Museum.jpg/1200px-Hill_Palace_Museum.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=hill_palace,
            title='Module 2: Collections and Features',
            content_text='''# Collections and Features

## Museum Collections

### Artifacts
- Ancient jewelry
- Traditional costumes
- Rare paintings
- Historical weapons
- Ivory carvings

### Manuscripts
- Ancient manuscripts
- Old royal decrees
- Historical documents

### Paintings
- Traditional Kerala murals
- Portrait gallery
- Rare artwork

## Building Architecture

### Structure
- Traditional Kerala architecture
- Teak wood construction
- Beautiful courtyard
- Spacious rooms

### Gardens
- Lush green surroundings
- Rare medicinal plants
- Beautiful landscape

## Visitor Information

### Timings
- Open all days except Monday
- 9:00 AM to 12:30 PM
- 2:00 PM to 4:30 PM

### Entry Fee
- Nominal fee for Indians
- Free for students
- Additional fee for camera''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Hill_Palace_Museum.jpg/1200px-Hill_Palace_Museum.jpg',
            order=2
        )
        
        self.stdout.write(self.style.SUCCESS('Heritage Sites sub-modules added successfully!'))
