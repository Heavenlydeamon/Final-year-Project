from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial

class Command(BaseCommand):
    help = 'Add Western Ghats sub-modules with proper content structure'

    def handle(self, *args, **options):
        # Get the Environment section
        env_section, _ = Section.objects.get_or_create(
            name='Environment',
            defaults={
                'description': 'Learn about the environment, climate change, and conservation.',
            }
        )
        
        # Get or create Western Ghats topic
        western_ghats, _ = Topic.objects.get_or_create(
            name='Western Ghats',
            section=env_section,
            defaults={
                'description': 'Explore the biodiversity hotspot of the Western Ghats mountain range.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Kodagu_landscape.jpg/1200px-Kodagu_landscape.jpg',
                'order': 1
            }
        )
        
        # Delete existing study materials for Western Ghats to rebuild
        western_ghats.study_materials.all().delete()
        
        # ========================================
        # WESTERN GHATS MODULE 1: Physical Geography
        # ========================================
        StudyMaterial.objects.create(
            topic=western_ghats,
            title='Module 1: The Great Escarpment of India',
            content_text='''### The Great Escarpment of India

The Western Ghats, also known as the **Sahyadri**, is a majestic mountain range that covers an area of approximately 160,000 square kilometers, stretching for 1,600 kilometers parallel to the western coast of the Indian peninsula. This range is older than the Himalayas and is considered one of the most significant geographic features of the Indian subcontinent.

#### Geological Formation
Unlike the Himalayas, which were formed by the collision of tectonic plates, the Western Ghats are not "true" mountains in the traditional sense. They are the **faulted edge of the Deccan Plateau**, formed during the slow break-up of the ancient supercontinent **Gondwana** nearly 150 million years ago. As India separated from Madagascar and drifted northward, the western edge of the plateau tilted, creating the dramatic escarpment we see today. This ancient lineage makes the Sahyadri one of the oldest and most stable mountain systems in the world.

#### Geographic Extent
The range begins its journey at the **Tapi River in Gujarat** and winds its way south through Maharashtra, Goa, Karnataka, and Kerala, finally reaching its southern tip at **Kanyakumari in Tamil Nadu**. Throughout this journey, the Ghats create a diverse landscape of peaks, plateaus, and deep valleys.

#### The Highest Peak: Anamudi
Standing tall at 2,695 meters, **Anamudi** in Kerala is the highest peak in India south of the Himalayas. Often referred to as the **"Everest of South India"**, it is located within the Eravikulam National Park in the Anamalai hills. Its name literally translates to "Elephant's forehead," a fitting title for its massive, rounded shape.

#### Climate Regulator
The Western Ghats play a crucial role as a **climatic regulator** for the entire Indian peninsula. They act as a massive barrier to the moisture-laden southwest monsoon winds that sweep in from the Arabian Sea. This results in heavy orographic rainfall on the western slopes, nurturing the lush evergreen rainforests for which Kerala is famous. Meanwhile, the eastern side remains in a "rain shadow," receiving significantly less precipitation. The annual rainfall on the windward side can reach staggering levels between 2,000 mm and 7,000 mm, making the Western Ghats one of the wettest regions on our planet.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Kodagu_landscape.jpg/1200px-Kodagu_landscape.jpg',
            order=1
        )
        
        # ========================================
        # WESTERN GHATS MODULE 2: Flora and Fauna
        # ========================================
        StudyMaterial.objects.create(
            topic=western_ghats,
            title='Module 2: A Global Biodiversity Hotspot',
            content_text='''### A Global Biodiversity Hotspot

The Western Ghats is internationally recognized as one of the **eight "hottest" biodiversity hotspots** on Earth. This status is earned due to its extraordinary density of life and the high number of species found nowhere else. The region serves as a sanctuary for over **7,000 species of flowering plants** and hundreds of unique animal species that have evolved in isolation over millions of years.

#### The Magic of Endemism
The most remarkable feature of the Sahyadri is its high rate of **endemism**. Over 1,500 species of flowering plants, 150 species of reptiles, and more than 100 species of amphibians are endemic to these mountains. This means if these habitats are destroyed, these species will vanish from the planet forever.

#### Flagship Species
Among the many treasures of the Ghats, several "flagship" species stand out as symbols of its ecological health:

*   **Nilgiri Tahr:** This endangered mountain goat is found exclusively in the high-altitude montane grasslands (Sholas) of the southern Western Ghats. Eravikulam National Park is one of the few places where they can still be seen in their natural habitat.
*   **Lion-tailed Macaque:** One of the rarest and most endangered primates in the world, this macaque is easily recognizable by the silver-white mane surrounding its face. They are highly dependent on the dense, undisturbed rainforest canopies.
*   **Malabar Giant Squirrel:** A colorful, shy rodent that can grow up to three feet long. Its vibrant fur patterns of purple, maroon, and brown help it blend into the sun-dappled canopy of the rainforest.
*   **Neelakurinji:** This unique shrub is famous for its synchronized blooming cycle. Once every **12 years**, the hills of Munnar and the Nilgiris are blanketed in a sea of purple as millions of Kurinji flowers bloom simultaneously, a spectacle that last occurred in 2018.

#### Wildlife Corridors
The continuity of the Western Ghats is essential for the survival of large mammals like Asian elephants and Bengal tigers. The range provides vital **wildlife corridors** that allow these animals to migrate between different national parks and sanctuaries, ensuring genetic diversity and reducing human-wildlife conflict.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Queen_s_Danaine_Butterfly.jpg/800px-Queen_s_Danaine_Butterfly.jpg',
            order=2
        )
        
        # ========================================
        # WESTERN GHATS MODULE 3: Hydrology
        # ========================================
        StudyMaterial.objects.create(
            topic=western_ghats,
            title='Module 3: The Water Tower of South India',
            content_text='''### The Water Tower of South India

The Western Ghats are often described as the **"Water Tower"** for peninsular India. This title is well-deserved, as the range feeds a vast and complex network of river systems that sustain millions of lives and thousands of hectares of fertile farmland across several states.

#### Major River Origins
Nearly all the major rivers of South India trace their beginnings to the springs and streams of the Western Ghats. In Kerala, the **Periyar**, the state's longest river, originates deep within these mountains, as do the **Bharathapuzha** and the **Pamba**. On a larger scale, the mighty **Godavari**, **Krishna**, and **Kaveri** all begin their journey here, flowing eastward across the Deccan Plateau to reach the Bay of Bengal.

#### Critical Ecosystem Services
Beyond merely providing water, the forests of the Western Ghats offer "ecosystem services" that are vital for the subcontinent's survival:

*   **Carbon Sequestration:** The dense, multi-layered forests act as massive carbon sinks, absorbing significant amounts of carbon dioxide and helping to mitigate the local effects of global warming.
*   **Soil Conservation:** The complex root systems of the mountain forests anchor the soil on steep slopes, preventing erosion and reducing the risk of catastrophic landslides during the monsoon.
*   **Groundwater Recharge:** The forest floor acts like a giant sponge, allowing rainwater to seep into the ground and recharge the aquifers that feed thousands of springs and wells in the surrounding plains.

#### Sustaining a Subcontinent
It is estimated that over **500 million people** depend directly or indirectly on the rivers originating in the Western Ghats for their drinking water, agriculture, and industrial needs. This makes the conservation of the range not just an environmental issue, but a matter of national security and economic stability for South India.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Periyar_River.jpg/1200px-Periyar_River.jpg',
            order=3
        )
        
        # ========================================
        # WESTERN GHATS MODULE 4: Threats and Conservation
        # ========================================
        StudyMaterial.objects.create(
            topic=western_ghats,
            title='Module 4: Preserving the Sahyadri',
            content_text='''### Preserving the Sahyadri

Despite being designated as a **UNESCO World Heritage Site in 2012**, the Western Ghats face unprecedented environmental pressures. The delicate balance of its ecosystems is being tested by human activities and the shifting global climate.

#### Key Threats to the Mountains
Several factors contribute to the degradation of this vital mountain range:
*   **Deforestation and Land Use Change:** Large tracts of original forest have been cleared over the decades to make way for commercial tea, coffee, and rubber plantations. This fragmentation of habitat disrupts wildlife migration and reduces biodiversity.
*   **Mining Activities:** In states like Goa and Karnataka, iron and manganese ore mining have left deep scars on the landscape, causing massive soil erosion and polluting river systems.
*   **Infrastructure Development:** The expansion of highways, the construction of large dams, and the rapid urbanization of hill stations like Munnar and Mahabaleshwar put immense pressure on the fragile mountain ecology.
*   **Climate Change:** Perhaps the most daunting threat is the changing climate. Erratic monsoon patterns have already led to devastating events, such as the **2018 Kerala floods** and subsequent landslides, which caused massive loss of life and property.

#### The Path to Conservation: Gadgil and Kasturirangan Reports
The debate over how to protect the Ghats has been shaped by two landmark reports. The **Gadgil Report (2011)** recommended that the entire range be declared an Ecologically Sensitive Area (ESA) with strict limits on development. The subsequent **Kasturirangan Report (2013)** proposed a more moderate approach, suggesting that 37% of the area be protected while allowing for sustainable development in other parts.

#### The Future of the Ghats
The survival of the Western Ghats depends on our ability to balance human needs with environmental conservation. Ongoing efforts like **'Project Tiger'** and **'Project Elephant'** continue to protect critical habitats, but the long-term health of the Sahyadri requires a collective commitment from governments, local communities, and every citizen who depends on the "Water Tower of India."''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('Western Ghats sub-modules updated with detailed narrative content!'))
        self.stdout.write(self.style.SUCCESS(f'Updated 4 sub-modules for Western Ghats topic'))

