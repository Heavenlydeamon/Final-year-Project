from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial

class Command(BaseCommand):
    help = 'Add Padmanabhapuram Palace topic with detailed narrative content'

    def handle(self, *args, **options):
        # Get the Heritage section
        heritage_section, _ = Section.objects.get_or_create(
            name='Heritage Sites',
            defaults={
                'description': 'Explore the architectural and historical heritage of Kerala.',
            }
        )
        
        # Get or create Padmanabhapuram Palace topic
        palace, _ = Topic.objects.get_or_create(
            name='Padmanabhapuram Palace',
            section=heritage_section,
            defaults={
                'description': 'Discover the largest wooden palace in Asia, a masterpiece of traditional Kerala architecture.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Padmanabhapuram_Palace_Facade.jpg/1200px-Padmanabhapuram_Palace_Facade.jpg',
                'order': 5
            }
        )
        
        # Delete existing study materials to rebuild
        palace.study_materials.all().delete()
        
        # MODULE 1: Introduction and History
        StudyMaterial.objects.create(
            topic=palace,
            title='Module 1: The Wooden Wonder of Asia',
            content_text='''### The Wooden Wonder of Asia

Located in Kanyakumari district (formerly part of the Travancore kingdom), **Padmanabhapuram Palace** is recognized as the largest and most magnificent wooden palace in all of Asia. This sprawling complex is not just a royal residence; it is the ultimate masterpiece of traditional Kerala architecture, known as *Tatchu Shastra* (the science of carpentry). 

#### A Royal Seat of Power
For centuries, Padmanabhapuram served as the capital of the **Kingdom of Travancore** before the seat of power was shifted to Thiruvananthapuram in 1795. The palace was originally constructed around 1601 CE by Iravi Varma Kulasekhara Perumal and was further expanded and refined by the legendary King **Anizham Thirunal Marthanda Varma** in the 18th century. It remains under the administration of the Kerala Government's Archaeology Department, despite being located in the neighboring state of Tamil Nadu.

#### Architectural Harmony
The palace is a complex of several structures, each serving a unique function, yet all unified by a consistent architectural language. The use of dark, polished teakwood and rosewood throughout the palace creates an atmosphere of understated elegance. The design principles emphasize natural light, cross-ventilation, and a seamless integration with the surrounding landscape, featuring numerous courtyards and open corridors that allow the sea breeze to cool the interiors naturally.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Padmanabhapuram_Palace_Facade.jpg/1200px-Padmanabhapuram_Palace_Facade.jpg',
            order=1
        )
        
        # MODULE 2: Architectural Marvels
        StudyMaterial.objects.create(
            topic=palace,
            title='Module 2: Architectural Marvels',
            content_text='''### Architectural Marvels of the Palace

Every room in Padmanabhapuram Palace tells a story of incredible craftsmanship and artistic vision. The palace is famous for its intricate wood carvings, unique flooring, and innovative design features that were ahead of their time.

#### The King's Council Chamber (Poomukham)
The entrance to the palace leads to the **Poomukham**, where the King met with his ministers. The ceiling here is a marvel of carpentry, featuring 90 different floral patterns, each one unique. The dark, glossy floor of the chamber is made from a secret traditional mixture of burnt coconut shells, lime, plant juices, and egg whites, resulting in a finish that is as smooth as marble and remains cool even in the hottest weather.

#### The Queen Mother’s Palace (Thai Kottaram)
The **Thai Kottaram** is the oldest part of the palace, dating back to the early 17th century. It is built in the traditional *Nalukettu* style, with a central open courtyard that allows rain and sunlight to enter the heart of the building. The wooden pillars in this section are carved from single trunks of jackfruit trees, showcasing the durability and beauty of local timber.

#### The Clock Tower and Dining Hall
The palace features a 300-year-old **Clock Tower** with a mechanical clock that still works today, a testament to the advanced engineering of the era. Adjacent to it is the massive **Dining Hall** (Oottupura), which could accommodate over 2,000 people at a time. The hall reflects the kingdom's tradition of large-scale hospitality and community feasts.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Padmanabhapuram_Palace_Facade.jpg/1200px-Padmanabhapuram_Palace_Facade.jpg',
            order=2
        )
        
        # MODULE 3: Artistic Treasures
        StudyMaterial.objects.create(
            topic=palace,
            title='Module 3: Artistic Treasures and Murals',
            content_text='''### Artistic Treasures and Murals

Beyond its structural beauty, Padmanabhapuram Palace is a repository of some of the finest examples of Kerala's traditional art forms. The palace was not just a home but a gallery of the kingdom's cultural achievements.

#### The Mural Paintings
The top floor of the King's residence (Uppirikka Malika) contains a sacred chamber whose walls are covered with exquisite **mural paintings**. These murals, executed using natural pigments derived from plants and minerals, depict scenes from Hindu mythology and the life of the Travancore royals. The level of detail and the vibrancy of the colors, which have survived for centuries without fading, are a source of wonder for art historians.

#### The Navaratri Mandapam
The **Navaratri Mandapam** is a grand hall used for dance and music performances during the nine-day Navaratri festival. The floor is made of polished granite, and the ceiling is supported by carved stone pillars. The hall is designed with incredible acoustics, ensuring that every note of a musical performance could be heard clearly throughout the space without the need for any modern amplification.

#### The Weaponry and Artifacts
The palace museum houses a significant collection of artifacts, including ancient weaponry, royal palanquins, and furniture. Among the most interesting items are the **"Manichithrathazu"**—intricate traditional locks of Kerala—and a solid stone cot given as a gift by a Dutch governor, which contrasts sharply with the delicate wooden furniture of the palace.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Padmanabhapuram_Palace_Facade.jpg/1200px-Padmanabhapuram_Palace_Facade.jpg',
            order=3
        )
        
        # MODULE 4: Preservation and Legacy
        StudyMaterial.objects.create(
            topic=palace,
            title='Module 4: Preservation and Global Legacy',
            content_text='''### Preservation and Global Legacy

Padmanabhapuram Palace is more than just a monument; it is a symbol of Kerala's enduring cultural identity and its sophisticated architectural heritage. Its preservation is a priority for both the government and international heritage organizations.

#### UNESCO World Heritage Aspirations
Due to its exceptional universal value, Padmanabhapuram Palace has been on the **UNESCO World Heritage Tentative List**. It is considered a primary example of "vernacular architecture," where the design is deeply rooted in local traditions, materials, and climate. Modern architects from around the world visit the palace to study its sustainable design principles, particularly its methods for natural cooling and light management.

#### Challenges in Conservation
Maintaining a massive wooden structure in a tropical climate presents significant challenges. The Kerala Archaeology Department employs traditional craftsmen to regularly treat the wood with natural oils and resins to prevent decay and insect damage. These efforts ensure that the "Wooden Wonder" continues to stand as a testament to the skill and wisdom of ancient Kerala's builders.

#### A Cultural Icon
Today, Padmanabhapuram Palace is one of the most visited heritage sites in South India. It serves as a bridge between the past and the present, offering visitors a glimpse into a world where architecture was a harmonious blend of art, science, and nature. It remains a source of immense pride for Keralites and a must-visit destination for anyone seeking to understand the soul of Kerala's heritage.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Padmanabhapuram_Palace_Facade.jpg/1200px-Padmanabhapuram_Palace_Facade.jpg',
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('Padmanabhapuram Palace topic and detailed modules added successfully!'))
