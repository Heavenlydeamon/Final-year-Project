from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial

class Command(BaseCommand):
    help = 'Add Cultural Artforms sub-modules with proper content structure'

    def handle(self, *args, **options):
        # Get the Cultural section
        cultural_section, _ = Section.objects.get_or_create(
            name='Cultural Artforms',
            defaults={
                'description': 'Discover cultural artforms and traditions.',
            }
        )
        
        # ========================================
        # KATHAKALI - 2 MODULES
        # ========================================
        kathakali, _ = Topic.objects.get_or_create(
            name='Kathakali',
            section=cultural_section,
            defaults={
                'description': 'Discover the world-renowned classical dance-drama of Kerala, famous for its grand costumes and expressive storytelling.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kathakali_performance.jpg/1200px-Kathakali_performance.jpg',
                'order': 1
            }
        )
        
        kathakali.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=kathakali,
            title='Module 1: The Poetry of Performance',
            content_text='''### Kathakali: The Poetry of Performance

Kathakali, which literally translates to "Story-Play," is one of the most sophisticated and visually stunning classical dance-dramas in the world. Originating in Kerala during the **17th century**, it is a unique blend of dance, music, acting, and ritual. Unlike other dance forms, Kathakali is a total theater experience, where the performer becomes a mythical character through a combination of stylized movements and intense facial expressions.

#### Origins and Evolution
Kathakali evolved from earlier folk and temple arts like *Krishnanattam* and *Ramanattam*. It was historically performed in temple courtyards or the palaces of local kings, often lasting from sunset until the break of dawn. The stories are primarily drawn from the great Indian epics—the **Ramayana, Mahabharata, and the Puranas**—bringing gods, demons, and heroes to life on a stage lit by a single large oil lamp (*Nilavilakku*).

#### The Language of Gestures
In Kathakali, the actors do not speak. Instead, they communicate through a complex language of hand gestures known as **Mudras** and incredible facial expressions (*Bhava*). A skilled performer can express the most subtle emotions—from deep sorrow to explosive anger—using only their eyes and facial muscles. This requires years of rigorous training, often beginning in childhood, to master the physical discipline and emotional depth required for the art.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kathakali_performance.jpg/1200px-Kathakali_performance.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=kathakali,
            title='Module 2: The Art of Transformation',
            content_text='''### The Art of Transformation: Makeup and Costumes

One of the most striking features of Kathakali is its elaborate makeup (*Vesham*) and grand costumes, which transform human actors into larger-than-life mythical beings. This process of transformation is a ritual in itself, often taking several hours before the performance begins.

#### A Palette of Character
The makeup is not just decorative; it is a code that reveals the nature of the character to the audience. The colors are derived from natural minerals and plants:
*   **Pachcha (Green):** This is used for noble heroes, kings, and divine beings like Rama or Krishna. It represents virtue and inner calm, often accompanied by a white paste border (*Chutti*) that accentuates the facial expressions.
*   **Kathi (Knife):** Characters who are brave but have a streak of evil or arrogance, like Ravana, wear green makeup but with red markings on the nose and forehead, symbolizing their "knife-like" nature.
*   **Minukku (Radiant):** Used for female characters and sages, this makeup is a soft, warm orange or yellow, symbolizing grace, spirituality, and gentle beauty.
*   **Kari (Black):** This is the makeup of the primitive and the evil. Forest dwellers and demonesses wear black faces, representing raw power and untamed nature.

#### Grandeur in Attire
The costumes of Kathakali are designed to create a sense of awe. The actors wear massive, colorful skirts made of many layers of cloth, which expand like a bell during movement. The headgear (*Kireedam*) is exceptionally ornate, made of wood and decorated with mirrors and beads. These heavy costumes, sometimes weighing over 20 kilograms, require the actors to have immense physical strength and balance, making the performance a true feat of endurance.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kathakali_performance.jpg/1200px-Kathakali_performance.jpg',
            order=2
        )
        
        # ========================================
        # MOHINIYATTAM - 2 MODULES
        # ========================================
        mohiniyattam, _ = Topic.objects.get_or_create(
            name='Mohiniyattam',
            section=cultural_section,
            defaults={
                'description': 'Discover the graceful classical dance form of Kerala, known as the "Dance of the Enchantress."',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohiniyattam_dance.jpg/1200px-Mohiniyattam_dance.jpg',
                'order': 2
            }
        )
        
        mohiniyattam.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=mohiniyattam,
            title='Module 1: The Dance of the Enchantress',
            content_text='''### Mohiniyattam: The Dance of the Enchantress

Mohiniyattam is the classical dance form of Kerala, known for its extreme grace, fluid movements, and subtle expressions. The name itself is derived from the words *Mohini*, meaning a woman who enchants onlookers, and *Attam*, meaning dance. In Hindu mythology, Mohini is the female avatar of Lord Vishnu, who appeared to protect the world from evil through her beauty and grace.

#### Fluidity and Grace
The hallmark of Mohiniyattam is its swaying movement of the torso from side to side, reminiscent of the gently waving palm trees or the rhythmic flow of the Kerala backwaters. The dance is traditionally performed solo by women and is characterized by its lyrical and feminine nature. The movements are never jerky; they flow into one another like a continuous stream of poetry in motion.

#### Traditional Attire: The White and Gold
The costume of Mohiniyattam is as elegant as the dance itself. Dancers wear a traditional Kerala saree, which is off-white or cream-colored with a rich golden border (*Kasavu*). The hair is gathered into a distinctive bun on the side of the head and adorned with garlands of fresh white jasmine flowers. This simple yet stunning aesthetic reflects the natural beauty and purity associated with the art form.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohiniyattam_dance.jpg/1200px-Mohiniyattam_dance.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=mohiniyattam,
            title='Module 2: Expressions of Devotion',
            content_text='''### Expressions of Devotion: Music and Abhinaya

While the physical movements of Mohiniyattam are beautiful, the soul of the dance lies in its emotional depth and the performer's ability to express complex feelings through *Abhinaya* (acting).

#### The Music of Sopanam
The music used in Mohiniyattam is based on the *Sopana Sangeetham* tradition of Kerala, which is slow, melodic, and deeply emotional. The lyrics are often in *Manipravalam*, a poetic blend of Malayalam and Sanskrit. The accompanying instruments, such as the **Edakka** (a sensitive pressure drum) and the **Veena**, create a soothing atmosphere that perfectly complements the dancer's graceful movements.

#### Subtle Storytelling
Unlike the dramatic and explosive expressions of Kathakali, Mohiniyattam focuses on *Lasya*—the gentle and graceful aspect of dance. Dancers use subtle eye movements and delicate hand gestures (*Mudras*) to tell stories of love, devotion, and longing. Most performances revolve around themes of *Bhakti* (devotion to God), where the dancer expresses the soul's yearning for the divine. Through years of training, a dancer learns to make even the smallest movement of the eyebrow or a slight tilt of the head convey a world of meaning to the audience.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mohiniyattam_dance.jpg/1200px-Mohiniyattam_dance.jpg',
            order=2
        )
        
        # ========================================
        # THEYAM - 2 MODULES
        # ========================================
        theyyam, _ = Topic.objects.get_or_create(
            name='Theyyam',
            section=cultural_section,
            defaults={
                'description': 'Explore the ancient ritual dance form of North Kerala, where man transforms into a living deity.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Theyyam_performance.jpg/1200px-Theyyam_performance.jpg',
                'order': 3
            }
        )
        
        theyyam.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=theyyam,
            title='Module 1: The Living Tradition of the North',
            content_text='''### Theyyam: The Living Tradition of North Kerala

Theyyam is an ancient and powerful ritual dance form performed primarily in the northern districts of Kerala, such as Kannur and Kasaragod. It is considered a "living tradition" that dates back over **1,500 years**, rooted in tribal and agrarian customs. The word *Theyyam* is a corruption of the word *Daivam*, which means "God."

#### From Man to Deity
The most profound aspect of Theyyam is the belief that during the performance, the dancer actually becomes the deity they are representing. This transformation is not just theatrical; it is a spiritual process. Once the dancer dons the final piece of their costume and looks into a mirror, the spirit of the god is believed to enter their body. From that moment on, they are no longer a human but a living deity who can bless the devotees, settle disputes, and offer prophecies.

#### A Seasonal Ritual
Theyyam is not performed on a stage but in the sacred groves (*Kavus*) and temple courtyards of North Malabar. The season typically lasts from October to May. Each performance is a massive community event, bringing together people of all castes and backgrounds. There are over 400 different types of Theyyam, each representing a specific deity, a hero from local folklore, or an ancestral spirit, each with its own unique story and ritual significance.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Theyyam_performance.jpg/1200px-Theyyam_performance.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=theyyam,
            title='Module 2: Rituals of Fire and Rhythm',
            content_text='''### Rituals of Fire and Rhythm: Makeup and Performance

A Theyyam performance is a breathtaking spectacle of color, sound, and energy, designed to create a sense of divine presence and awe.

#### Elaborate Artistry
The makeup and costumes of Theyyam are among the most intricate in the world. Dancers spend hours lying on the ground while artists paint their faces with vibrant natural colors—primarily red, orange, and black. Each pattern is specific to the deity being represented. The costumes include massive headdresses (*Mudi*), sometimes standing several feet tall, made of bamboo, cloth, and peacock feathers. Some Theyyams also involve "fire-walking" or wearing costumes made of lit coconut fronds, symbolizing the deity's power over the elements.

#### The Power of the Drum
The rhythm of Theyyam is driven by the **Chenda** and the **Thappu** (percussion drums). The beats start slowly and gradually build to a hypnotic, frantic pace as the dancer enters a trance-like state. The dancer moves with explosive energy, performing acrobatic feats and high jumps that reflect the raw power of the divine spirit.

#### Social and Cultural Impact
Historically, Theyyam has played a crucial role in the social life of North Kerala. It provided a platform for marginalized communities, as the performers often come from lower-caste groups but are revered as gods by everyone, including the highest-ranking members of society, during the ritual. This unique tradition remains a powerful symbol of Kerala's complex and inclusive cultural heritage.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Theyyam_performance.jpg/1200px-Theyyam_performance.jpg',
            order=2
        )
        
        # ========================================
        # KALARIPAYATTU - 2 MODULES
        # ========================================
        kalaripayattu, _ = Topic.objects.get_or_create(
            name='Kalaripayattu',
            section=cultural_section,
            defaults={
                'description': 'Discover the ancient martial art of Kerala, the "Mother of All Martial Arts," which balances physical combat with spiritual healing.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kalaripayattu.jpg/1200px-Kalaripayattu.jpg',
                'order': 4
            }
        )
        
        kalaripayattu.study_materials.all().delete()
        
        StudyMaterial.objects.create(
            topic=kalaripayattu,
            title='Module 1: The Mother of All Martial Arts',
            content_text='''### Kalaripayattu: The Mother of All Martial Arts

Kalaripayattu is widely considered the oldest surviving martial art in the world, with roots tracing back over **2,000 years** to the ancient battlefields of Kerala. It is a comprehensive system that encompasses physical training, weapon mastery, and a deep understanding of the human body’s vital points. Legend has it that the sage Parasurama, the mythological creator of Kerala, was the first teacher of this sacred art.

#### The Kalari: A Sacred Space
The word *Kalari* refers to the traditional training ground, which is often a pit dug into the earth to provide a cool environment for practice. More than just a gym, the Kalari is a sacred space where the student (*Shishya*) begins their journey with a prayer to the presiding deity and the Guru. The training follows the *Gurukula* system, where knowledge is passed down from master to student through years of disciplined practice.

#### A Legacy of Warriors
During the medieval period, Kalaripayattu was the backbone of Kerala's social and military structure. Every village had its own Kalari, and young men and women were trained in self-defense and combat. The heroic tales of warriors like **Thacholi Othenan** and the legendary woman warrior **Unniyarcha**, immortalized in the *Vadakkan Pattukal* (Northern Ballads), highlight the honor and valor associated with this martial art.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kalaripayattu.jpg/1200px-Kalaripayattu.jpg',
            order=1
        )
        
        StudyMaterial.objects.create(
            topic=kalaripayattu,
            title='Module 2: Discipline of Mind and Body',
            content_text='''### Discipline of Mind and Body: Techniques and Healing

Kalaripayattu is unique because it is not just about combat; it is a holistic system designed to achieve a perfect balance between the mind and the body. The training is divided into several stages, each building upon the previous one.

#### The Stages of Training
The journey begins with **Meythari**, or body conditioning. These exercises involve intense stretching, jumps, and twists to make the body as flexible as a snake. Once the body is ready, the student moves on to **Kolthari**, training with wooden sticks of various lengths. This is followed by **Ankathari**, the mastery of metal weapons like the sword, shield, spear, and the deadly *Urumi* (the flexible long sword). The final stage is **Verumkai**, or unarmed combat, where the student learns to use their body as a weapon.

#### The Science of Marma
The most advanced and secretive part of Kalaripayattu is the study of **Marma Vidya**—the knowledge of 107 vital points in the human body. A master can use these points to disable an opponent with a single touch, but more importantly, this knowledge is used for healing. Kalaripayattu is closely linked to Ayurveda, and masters often practice traditional massage and orthopedic treatments to heal injuries and maintain the health of their students.

#### Modern Global Impact
Today, Kalaripayattu is experiencing a global revival. It is no longer just for warriors but is practiced by dancers, actors, and fitness enthusiasts worldwide to improve their agility and focus. Its influence can be seen in many East Asian martial arts, which are believed to have been influenced by monks who traveled from India to China and Japan, carrying the seeds of this ancient Kerala tradition.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Kalaripayattu.jpg/1200px-Kalaripayattu.jpg',
            order=2
        )

        # ========================================
        # ONAM - 2 MODULES
        # ========================================
        onam, _ = Topic.objects.get_or_create(
            name='Onam',
            section=cultural_section,
            defaults={
                'description': 'Kerala’s grandest harvest festival, celebrating the return of King Mahabali and the spirit of equality and abundance.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Onam_Pookalam.jpg/1200px-Onam_Pookalam.jpg',
                'order': 5
            }
        )

        onam.study_materials.all().delete()

        StudyMaterial.objects.create(
            topic=onam,
            title='Module 1: The Legend of the Golden Age',
            content_text='''### Onam: The Legend of the Golden Age

Onam is the most important cultural festival of Kerala, a ten-day celebration that transcends religious boundaries and unites the entire state in a spirit of joy and abundance. Falling in the Malayalam month of *Chingam* (August-September), it marks the end of the monsoon and the beginning of the harvest season.

#### The Homecoming of King Mahabali
At the heart of Onam is the beloved legend of **King Mahabali** (Maveli), an Asura king whose reign was considered the "Golden Age" of Kerala. Under his rule, there was absolute equality, and the land was free from poverty, crime, and dishonesty. Although the gods grew jealous and Mahabali was eventually sent to the underworld by Lord Vishnu in his *Vamana* avatar, the King was granted a boon to visit his people once every year. Onam is the celebration of his annual homecoming.

#### The Ten Days of Celebration
The festival begins on the day of *Atham* and culminates on the grand day of **Thiruvonam**. Each day has its own significance, marked by the creation of the **Pookalam**—intricate flower carpets laid out in front of homes to welcome the King. As the days progress, the Pookalams grow larger and more complex, reflecting the increasing excitement and devotion of the community.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Onam_Pookalam.jpg/1200px-Onam_Pookalam.jpg',
            order=1
        )

        StudyMaterial.objects.create(
            topic=onam,
            title='Module 2: A Tapestry of Traditions',
            content_text='''### A Tapestry of Traditions: Feast, Boats, and Tigers

The celebration of Onam is a grand display of Kerala's cultural richness, featuring a variety of unique traditions that engage every sense.

#### The Grand Onasadya
No Onam is complete without the **Onasadya**, a spectacular vegetarian feast served on a fresh banana leaf. It traditionally consists of 26 or more dishes, ranging from the creamy *Avial* to the sweet *Payasam*. The meal is a masterpiece of culinary balance, featuring all six tastes and symbolizing the abundance of the harvest. Families gather together to share this feast, reinforcing bonds of love and community.

#### Thrills on the Water and in the Streets
Onam is also the season of the **Vallam Kali** (snake boat races). Hundreds of rowers synchronize their movements to the rhythmic *Vanchipattu* (boat songs), competing for glory on the backwaters. Meanwhile, in the streets of Thrissur, the vibrant **Pulikali** (Tiger Dance) takes place. Men painted as tigers and hunters dance to the beat of traditional drums, a playful and energetic performance that draws thousands of spectators.

#### A Festival of Unity
What makes Onam truly special is its secular nature. It is a festival celebrated by Hindus, Muslims, and Christians alike, embodying the spirit of communal harmony and the shared dream of a world where everyone is treated with equality and respect. It is a reminder of Kerala’s resilient cultural fabric and its commitment to the values of the legendary King Mahabali.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Pulikali_Thrissur_2013.jpg/1200px-Pulikali_Thrissur_2013.jpg',
            order=2
        )

        # ========================================
        # VISHU - 2 MODULES
        # ========================================
        vishu, _ = Topic.objects.get_or_create(
            name='Vishu',
            section=cultural_section,
            defaults={
                'description': 'The Malayalam New Year, symbolizing the start of a new agricultural cycle and the hope for a prosperous future.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Vishukkani_arrangements.jpg/1200px-Vishukkani_arrangements.jpg',
                'order': 6
            }
        )

        vishu.study_materials.all().delete()

        StudyMaterial.objects.create(
            topic=vishu,
            title='Module 1: The Sacred First Sight',
            content_text='''### Vishu: The Sacred First Sight

Vishu is the Malayalam New Year, celebrated on the first day of the month of *Medam* (usually April 14th or 15th). It marks the sun's transit into the zodiac sign of Aries and coincides with the spring equinox. For the people of Kerala, Vishu is not just a change on the calendar; it is a time of renewal, symbolizing the beginning of a fresh agricultural cycle.

#### The Vishukkani: An Auspicious Beginning
The most important ritual of the festival is the **Vishukkani**, which literally means "the first thing seen on Vishu morning." Families arrange a collection of auspicious items in a brass vessel (*Uruli*) the night before. This includes golden **Kani Konna** (Laburnum) flowers, rice, fruits, a mirror, gold ornaments, and a lit oil lamp. Keralites believe that the first sight of these symbols of abundance and prosperity will ensure good fortune for the entire year ahead.

#### A Morning of Devotion
The tradition is for the elders to lead the younger family members, often blindfolded, to the room where the Vishukkani is arranged, so that it is the very first thing their eyes behold. This is often followed by a visit to the local temple, where people pray for health and prosperity in the coming year.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Vishukkani_arrangements.jpg/1200px-Vishukkani_arrangements.jpg',
            order=1
        )

        StudyMaterial.objects.create(
            topic=vishu,
            title='Module 2: Rituals of Abundance',
            content_text='''### Rituals of Abundance: Kaineetam and Cuisine

Beyond the morning ritual, Vishu is a day filled with traditions that emphasize sharing, community, and the simple joys of life.

#### Vishukaineetam: The Gift of Sharing
One of the most anticipated parts of the day, especially for children, is **Vishukaineetam**. Elders of the family give small amounts of money to the younger members as a blessing. This practice is not just about the money itself; it represents the sharing of wealth and the passing of responsibility and goodwill from one generation to the next.

#### The Flavors of Vishu
The **Vishu Sadya** is the culinary highlight of the day. Unlike the Onam feast, the Vishu meal often includes special items like **Vishu Kanji** (a rice porridge with coconut milk) and dishes that combine all six tastes. A key dish is the *Veppampoorasam*—a mixture of bitter neem flowers, sweet jaggery, and sour mango. This unique combination serves as a philosophical reminder that the coming year will bring a mix of both joy and sorrow, and one must learn to embrace them both.

#### Fireworks and New Beginnings
The day is also marked by the bursting of firecrackers (*Vishuppada*), filling the air with sound and color. As families wear new clothes (*Puthukodi*) and visit neighbors, the spirit of Vishu serves as a powerful reminder of hope and the eternal cycle of nature, encouraging everyone to look forward to the future with optimism.''',
            image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Vishukkani_arrangements.jpg/1200px-Vishukkani_arrangements.jpg',
            order=2
        )

        self.stdout.write(self.style.SUCCESS('Cultural Artforms modules expanded with detailed narrative content!'))

