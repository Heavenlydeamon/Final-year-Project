import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StudyMaterial

t = Topic.objects.filter(name__icontains='Fort Kochi').first()

if t:
    print(f"Updating topic: {t.name}")
    # Update topic description
    t.description = "Fort Kochi is not merely a town; it is a living museum. As the first European township in India, it served as the primary gateway for the global spice trade, weaving together a 500-year-old tapestry of Portuguese, Dutch, British, and Arab influences into the local fabric of Kerala."
    t.save()

    StudyMaterial.objects.filter(topic=t).delete()

    StudyMaterial.objects.create(topic=t, title='Historical Genesis', content_text='''### The Living Museum of Fort Kochi

Fort Kochi is a coastal palimpsest where every street corner whispers a different century. Nestled on the reclaimed islands of the Kochi Lake, it remains one of the few places in the world where a Jewish Synagogue, a Dutch Palace, a Portuguese Church, and Chinese fishing nets exist within a three-kilometer radius. This unique geographical and cultural positioning has made it a "living museum," preserving the footprints of global explorers who arrived here seeking the legendary spices of Kerala.

#### Colonial Echoes and Sacred Spaces
The history of Fort Kochi is inextricably linked to the arrival of Europeans in India. It houses the **St. Francis Church**, which was the original burial site of the famed explorer Vasco da Gama before his remains were moved to Lisbon. Nearby, the **Paradesi Synagogue** stands as the oldest active synagogue in the Commonwealth, its floor adorned with hand-painted porcelain tiles from China, reflecting the global connections of the Cochin Jewish community.

#### Iconic Vistas: The Cheenavalai
The shoreline of Fort Kochi is defined by its most iconic sight—the **Cheenavalai**, or Chinese fishing nets. These massive cantilevered structures were introduced by traders from the court of Kublai Khan in the 14th century. To this day, they operate on a complex system of weights and pulleys, requiring at least four fishermen to balance and lift the catch, serving as a silhouette of Kochi's ancient maritime heritage.

#### Artistic Renaissance
In recent years, Fort Kochi has transformed into a global canvas. Since 2012, it has served as the primary host for the **Kochi-Muziris Biennale**, India’s largest contemporary art festival. During this time, the colonial-era warehouses and historical buildings are converted into art galleries, blending the old-world charm with cutting-edge modern expression.''', order=1)

    StudyMaterial.objects.create(topic=t, title='Architecture Highlights', content_text='''### Tropical Colonial Architecture

The architecture of Fort Kochi is a unique "Tropical Colonial" hybrid, representing a fascinating dialogue between European design and Kerala's local craftsmanship. When the Portuguese, Dutch, and British arrived, they brought their own architectural styles—steep tiled roofs, wooden shutters, and high ceilings—but had to adapt them to survive Kerala’s heavy monsoons and tropical heat.

#### Adapting to the Monsoon
Builders used local materials like laterite stone and teakwood, which were better suited for the humid climate than European materials. The Result is a style where European layouts meet Kerala's traditional ventilation techniques. Large windows and open verandas were incorporated to facilitate the flow of sea breezes, a primitive yet highly effective form of natural climate control.

#### A Timeline of Influence
The evolution of the town can be traced through its milestones:
*   **1503 (Portuguese Arrival):** The construction of **Fort Emmanuel**, the first European fort in India, marked the beginning of colonial military architecture in the region.
*   **1663 (Dutch Conquest):** The Dutch modernized the town and built the **Mattancherry Palace** (often called the Dutch Palace), which features stunning murals depicting Hindu epics.
*   **1795 (British Era):** Fort Kochi became a municipality, and the focus shifted from military defense to commercial exports, particularly tea and spices, leading to the construction of massive warehouses.
*   **Post-Independence:** The focus has shifted toward preservation, evolving Fort Kochi into a major global heritage destination that honors all layers of its history.''', order=2)

    StudyMaterial.objects.create(topic=t, title='Folklore and Social Impact', content_text='''### The Fabric of Pluralism

The social fabric of Fort Kochi is defined by a deep-rooted pluralism that has existed for centuries. It is a place where different religions and cultures have not just co-existed, but have influenced each other to create a unique local identity.

#### The Spice Legacy and Local Folklore
Local folklore is rich with stories of the **"Black Gold"** (pepper) that lured explorers across uncharted oceans. It is said that the aroma of spices was so strong in the ancient port that sailors could smell it long before they reached the shore. This legacy is still alive on **Bazaar Road**, where the air remains thick with the scent of ginger, turmeric, and cardamom being traded in bulk, just as it was five hundred years ago.

#### Culinary Fusion
Kochi’s cuisine is a direct result of this European-Malayali fusion. The famous **"Meen Pollichathu"** (fish marinated in spices and grilled in a banana leaf) and the unique bakery culture of Kochi, which introduced European breads and cakes to the local palate, are delicious reminders of this shared history.

#### The Spirit of Tolerance
The history of the **Cochin Jews** is perhaps the most powerful example of Kochi's tolerance. Legends of the "Copper Plates" given by local kings to the Jewish community highlight a history of religious freedom and respect. This spirit of openness continues to define the town, making it a model of cultural harmony.''', order=3)

    StudyMaterial.objects.create(topic=t, title='Living Traditions', content_text='''### Heritage in Motion

Heritage in Fort Kochi is not just about static old buildings; it is about the survival of diverse traditions in everyday life.

#### The Engineering of the Nets
The **Cheenavalai** are a marvel of ancient engineering. Each net is a complex system of bamboo poles and teak wood, balanced by large stones tied to ropes. The operation is rhythmic and collaborative, a dance of physics and teamwork that has remained unchanged for centuries.

#### Laterite Construction: Nature's Cooler
Most colonial buildings in Fort Kochi use red **laterite bricks**, a volcanic rock abundant in Kerala. These stones are porous and have high thermal mass, meaning they absorb heat during the day and release it slowly at night. This traditional building method keeps the interiors of these five-century-old buildings remarkably cool even in the height of summer.

#### The Pulse of Bazaar Road
Walking down **Bazaar Road** is like stepping back in time. It was once the "Wall Street" of the East, and today it remains a bustling hub of commerce. The historical warehouses, or "godowns," still store sacks of spices, and the rhythmic calling of traders reminds us that Fort Kochi’s heart still beats with the pulse of global trade.''', order=4)

    StudyMaterial.objects.create(topic=t, title='Summary', content_text='''### Conclusion: A Global-Local Identity

Fort Kochi stands as the architectural and cultural embodiment of Kerala’s "Global-Local" identity. It is a testament to the fact that heritage is not a relic of the past, but a living tradition that evolves with time. By preserving everything from the way fish is caught to the way contemporary art is celebrated, Fort Kochi proves that diversity is the foundation of a truly resilient and vibrant society.''', order=5)


    print("Success: Fort Kochi content fully extended and formatted in Markdown.")
else:
    print("Error: Fort Kochi topic not found!")
