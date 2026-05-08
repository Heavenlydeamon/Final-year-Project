"""
Kerala Content & Quiz Expansion Seed Script
Run: python seed_kerala_content.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from django.contrib.auth.models import User
from content.models import Topic as ContentTopic
from mainapp.models import Topic as MainTopic, Section, StudyMaterial
from quiz.models import Quiz, MCQQuestion

admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()

def get_or_create_section(name, description=""):
    sec, _ = Section.objects.get_or_create(name=name, defaults={'description': description, 'is_general': True})
    return sec

def seed_topic(title, category, section_name, description, sections_json, study_materials, mcqs):
    """Create or update a full topic with content + quiz."""
    section = get_or_create_section(section_name)
    
    # Content Topic
    ct, created = ContentTopic.objects.get_or_create(
        title=title,
        defaults={
            'category': category, 'class_level': 'higher',
            'description': description, 'is_published': True,
            'created_by': admin_user, 'thumbnail': 'topics/default.jpg'
        }
    )
    if not created and not ct.sections:
        ct.description = description
    ct.sections = sections_json
    ct.save()
    
    # Mainapp Topic
    mt, _ = MainTopic.objects.get_or_create(
        name=title, section=section,
        defaults={'description': description, 'is_general': True}
    )
    
    # Study Materials
    if StudyMaterial.objects.filter(topic=mt).count() <= 1:
        StudyMaterial.objects.filter(topic=mt).delete()
        for i, sm in enumerate(study_materials):
            StudyMaterial.objects.create(topic=mt, title=sm['title'], content_text=sm['text'], order=i+1)
    
    # Quiz
    if not Quiz.objects.filter(topic=ct).exists():
        quiz = Quiz.objects.create(
            title=f"{title} Assessment", topic=ct,
            created_by=admin_user, source='admin', is_challenge_eligible=True
        )
        for q in mcqs:
            MCQQuestion.objects.create(quiz=quiz, **q)
        print(f"  + Quiz created ({len(mcqs)} MCQs)")
    else:
        print(f"  ~ Quiz already exists")
    
    print(f"{'Created' if created else 'Updated'}: {title}")

def add_extra_mcqs(topic_title, mcqs):
    """Add extra MCQs to an existing quiz."""
    ct = ContentTopic.objects.filter(title=topic_title).first()
    if not ct: return
    quiz = Quiz.objects.filter(topic=ct).first()
    if not quiz: return
    existing = set(MCQQuestion.objects.filter(quiz=quiz).values_list('question_text', flat=True))
    added = 0
    for q in mcqs:
        if q['question_text'] not in existing:
            MCQQuestion.objects.create(quiz=quiz, **q)
            added += 1
    print(f"  + {added} new MCQs added to {topic_title}")


# ============================================================
# PART 1: Enrich 7 existing topics with 0 sections
# ============================================================
print("\n" + "="*60)
print("PART 1: Enriching existing empty topics")
print("="*60)

# --- Kerala Cultural Heritage ---
seed_topic(
    title="Kerala Cultural Heritage",
    category="heritage", section_name="Traditional Folklore (Aithihyamala)",
    description="An overview of Kerala's rich cultural tapestry spanning 3000 years of art, architecture, cuisine, and spiritual traditions.",
    sections_json=[
        {"id": "origins", "label": "Ancient Origins"},
        {"id": "temple-culture", "label": "Temple Culture"},
        {"id": "social-reforms", "label": "Social Reform Movements"},
        {"id": "literary-tradition", "label": "Literary Tradition"},
        {"id": "performing-arts", "label": "Performing Arts Overview"},
        {"id": "modern-identity", "label": "Modern Cultural Identity"},
    ],
    study_materials=[
        {"title": "Ancient Origins", "text": "Kerala's cultural history traces back to the Sangam Age (300 BCE\u2013300 CE). The region was known as 'Chera Nadu', ruled by the Chera dynasty. Ancient Tamil-Brahmi inscriptions in Edakkal Caves prove human habitation dating back over 5,000 years.\n\n**Key Points:**\n* Trade connections with Rome, Greece, and China via the Muziris port\n* Buddhism and Jainism flourished before the 8th century\n* The Parasurama legend: Kerala is said to have been reclaimed from the sea by the axe-wielding sage"},
        {"title": "Temple Culture", "text": "Kerala's temple architecture is unique in India. Unlike North Indian Nagara or South Indian Dravidian styles, Kerala temples feature sloped roofs, wooden carvings, and copper-clad gopurams designed to withstand heavy monsoons.\n\n**Notable Temples:**\n* Guruvayur Temple \u2013 The 'Dwarka of the South'\n* Sabarimala \u2013 One of the world's largest annual pilgrimages\n* Vadakkunnathan Temple, Thrissur \u2013 A masterpiece of Kerala architecture"},
        {"title": "Social Reform Movements", "text": "Kerala's modern identity was forged through powerful social reform movements against caste discrimination.\n\n**Key Reformers:**\n* **Sree Narayana Guru** (1856\u20131928): 'One Caste, One Religion, One God for Man'\n* **Ayyankali** (1863\u20131941): Fought for Dalit rights and education access\n* **V.T. Bhattathiripad**: Led the Yogakshema Sabha reform movement\n\nThese movements made Kerala a model of social equity in India."},
        {"title": "Literary Tradition", "text": "Malayalam literature spans over 1,000 years. The oldest known work is Ramacharitam (12th century).\n\n**Literary Milestones:**\n* Thunchaththu Ezhuthachan \u2013 Father of Malayalam literature (Adhyatma Ramayanam)\n* Kumaran Asan, Vallathol, Ulloor \u2013 The 'Triumvirate of Modern Malayalam Poetry'\n* **Jnanpith Award Winners:** S.K. Pottekkatt, Thakazhi, O.V. Vijayan, M.T. Vasudevan Nair, O.N.V. Kurup, Akkitham"},
        {"title": "Performing Arts Overview", "text": "Kerala is home to some of India's most sophisticated performing art forms, many of which are UNESCO-recognized.\n\n**Classical Forms:**\n* Kathakali \u2013 Dance-drama with elaborate costumes\n* Mohiniyattam \u2013 Graceful 'dance of the enchantress'\n* Koodiyattam \u2013 The oldest surviving Sanskrit theatre (UNESCO)\n\n**Martial & Ritual:**\n* Kalaripayattu \u2013 Ancient martial art\n* Theyyam \u2013 Ritual dance worship of North Malabar"},
        {"title": "Modern Cultural Identity", "text": "Today, Kerala is known globally for its unique blend of tradition and progressiveness.\n\n**Modern Markers:**\n* **Kerala Model of Development:** Highest literacy rate (96.2%), best healthcare indicators in India\n* **IFFK:** International Film Festival of Kerala\u2014one of Asia's most prestigious\n* **Kochi-Muziris Biennale:** India's largest contemporary art exhibition\n* **Gulf Migration:** The diaspora has shaped Kerala's economy and cosmopolitan culture"},
    ],
    mcqs=[
        {"question_text": "What was Kerala known as during the Sangam Age?", "option_a": "Malabar", "option_b": "Chera Nadu", "option_c": "Travancore", "option_d": "Kochi", "correct_option": "B", "explanation": "Kerala was called Chera Nadu, ruled by the Chera dynasty."},
        {"question_text": "Who is known as the Father of Malayalam literature?", "option_a": "Kumaran Asan", "option_b": "Vallathol", "option_c": "Thunchaththu Ezhuthachan", "option_d": "Cherusseri", "correct_option": "C", "explanation": "Ezhuthachan wrote Adhyatma Ramayanam."},
        {"question_text": "Which is the oldest surviving Sanskrit theatre form?", "option_a": "Kathakali", "option_b": "Koodiyattam", "option_c": "Theyyam", "option_d": "Thullal", "correct_option": "B", "explanation": "Koodiyattam is UNESCO-recognized as the oldest."},
        {"question_text": "Who said 'One Caste, One Religion, One God for Man'?", "option_a": "Ayyankali", "option_b": "Mahatma Gandhi", "option_c": "Sree Narayana Guru", "option_d": "V.T. Bhattathiripad", "correct_option": "C", "explanation": "Sree Narayana Guru's famous teaching."},
        {"question_text": "What is unique about Kerala temple architecture?", "option_a": "Nagara-style towers", "option_b": "Sloped roofs and wooden carvings", "option_c": "Dravidian gopurams", "option_d": "Mughal domes", "correct_option": "B", "explanation": "Kerala temples use sloped roofs designed for monsoons."},
        {"question_text": "What is the Kochi-Muziris Biennale?", "option_a": "A music festival", "option_b": "A boat race", "option_c": "India's largest contemporary art exhibition", "option_d": "A temple festival", "correct_option": "C", "explanation": "It's held in Kochi and is India's largest art biennale."},
        {"question_text": "Which ancient port connected Kerala to Rome and China?", "option_a": "Calicut", "option_b": "Muziris", "option_c": "Quilon", "option_d": "Alleppey", "correct_option": "B", "explanation": "Muziris was the ancient global trading port."},
        {"question_text": "What is Kerala's literacy rate?", "option_a": "82%", "option_b": "88%", "option_c": "96.2%", "option_d": "75%", "correct_option": "C", "explanation": "Kerala has India's highest literacy rate at 96.2%."},
    ]
)

# --- Folklore in keralam ---
seed_topic(
    title="Folklore in keralam", category="heritage",
    section_name="Traditional Folklore (Aithihyamala)",
    description="The oral traditions, myths, and legends that form the backbone of Kerala's cultural memory.",
    sections_json=[
        {"id": "oral-traditions", "label": "Oral Traditions"},
        {"id": "aithihyamala", "label": "Aithihyamala Collection"},
        {"id": "folk-heroes", "label": "Folk Heroes & Legends"},
        {"id": "supernatural", "label": "Supernatural Beliefs"},
        {"id": "folk-music", "label": "Folk Music & Dance"},
        {"id": "preservation", "label": "Modern Preservation"},
    ],
    study_materials=[
        {"title": "Oral Traditions", "text": "Kerala's folklore was passed down orally for centuries through Pattu (songs), Kadha (stories), and Thottam Pattu (ritual songs). Villages had designated storytellers called Panars and Pulluvas who kept legends alive.\n\n**Key Oral Forms:**\n* Vadakkan Pattukal (Northern Ballads) \u2013 Heroic sagas of Malabar warriors\n* Thekkan Pattukal (Southern Ballads) \u2013 Tales from Travancore\n* Mappila Pattukal \u2013 Songs of the Malabar Muslim community"},
        {"title": "Aithihyamala Collection", "text": "The Aithihyamala ('Garland of Legends') is Kerala's most famous folklore collection, compiled by Kottarathil Sankunni in 1909.\n\n**Famous Stories:**\n* Kadamattathu Kathanar \u2013 The sorcerer priest who battled demons\n* Kayamkulam Kochunni \u2013 The Robin Hood of Kerala\n* Parayi Petta Panthirukulam \u2013 The twelve children of a lower-caste woman who became legends"},
        {"title": "Folk Heroes & Legends", "text": "**Thacholi Othenan:** The legendary Malabar warrior whose tales of valor, honor, and romance are still sung in Vadakkan Pattukal.\n\n**Unniyarcha:** A fierce woman warrior from the Northern Ballads who fought invaders with her urumi (flexible sword).\n\n**Aromal Chekavar:** A duel-fighting hero from Vadakkan Pattukal known for his tragic betrayal."},
        {"title": "Supernatural Beliefs", "text": "Kerala folklore is rich with supernatural entities:\n* **Yakshi** \u2013 A beautiful female spirit that lures travelers\n* **Gandharvan** \u2013 A celestial musician spirit\n* **Madan** \u2013 Mischievous tree spirits\n* **Kuttichathan** \u2013 A playful demon\n\nMany of these beings are still part of rural Kerala's cultural consciousness."},
        {"title": "Folk Music & Dance", "text": "**Oppana** \u2013 A Muslim wedding celebration dance\n**Margam Kali** \u2013 A Syrian Christian folk dance\n**Pulluvan Pattu** \u2013 Songs sung during serpent worship rituals\n**Duffmuttu** \u2013 Rhythmic Mappila art using the duff drum\n\nThese forms reflect Kerala's pluralistic society through folk expression."},
        {"title": "Modern Preservation", "text": "Kerala Folklore Academy (est. 1995) actively documents vanishing traditions. Universities now offer degrees in Folklore Studies.\n\n**Modern Adaptations:**\n* Films like 'Oru Vadakkan Veeragatha' brought Vadakkan Pattukal to mainstream\n* The Kochi Biennale incorporates folk art installations\n* Digital archives are preserving Pulluva songs and Theyyam chants"},
    ],
    mcqs=[
        {"question_text": "Who compiled the Aithihyamala?", "option_a": "Thunchaththu Ezhuthachan", "option_b": "Kottarathil Sankunni", "option_c": "Kumaran Asan", "option_d": "Vallathol", "correct_option": "B", "explanation": "Kottarathil Sankunni compiled it in 1909."},
        {"question_text": "What is a Yakshi in Kerala folklore?", "option_a": "A warrior queen", "option_b": "A snake deity", "option_c": "A beautiful female spirit", "option_d": "A river goddess", "correct_option": "C", "explanation": "Yakshi is a supernatural female spirit."},
        {"question_text": "What are Vadakkan Pattukal?", "option_a": "Temple songs", "option_b": "Southern ballads", "option_c": "Northern heroic ballads", "option_d": "Wedding songs", "correct_option": "C", "explanation": "Vadakkan Pattukal are heroic ballads from Malabar."},
        {"question_text": "Who is Unniyarcha?", "option_a": "A folklore compiler", "option_b": "A legendary woman warrior", "option_c": "A Yakshi", "option_d": "A queen", "correct_option": "B", "explanation": "Unniyarcha is a fierce woman warrior from Northern Ballads."},
        {"question_text": "What is Oppana?", "option_a": "A temple ritual", "option_b": "A Muslim wedding dance", "option_c": "A martial art", "option_d": "A harvest song", "correct_option": "B", "explanation": "Oppana is celebrated during Muslim weddings."},
        {"question_text": "When was the Kerala Folklore Academy established?", "option_a": "1975", "option_b": "1985", "option_c": "1995", "option_d": "2005", "correct_option": "C", "explanation": "Kerala Folklore Academy was established in 1995."},
        {"question_text": "What is Margam Kali?", "option_a": "A Hindu temple dance", "option_b": "A Syrian Christian folk dance", "option_c": "A Muslim art form", "option_d": "A tribal ritual", "correct_option": "B", "explanation": "Margam Kali is a traditional Syrian Christian dance."},
        {"question_text": "What weapon did Unniyarcha use?", "option_a": "Sword and shield", "option_b": "Urumi (flexible sword)", "option_c": "Bow and arrow", "option_d": "Spear", "correct_option": "B", "explanation": "She wielded the urumi, a flexible sword."},
    ]
)

# --- The legend of Mahabali ---
seed_topic(
    title="The legend of Mahabali", category="heritage",
    section_name="story of mahabali ",
    description="The beloved legend of the Asura King Mahabali, whose reign represents Kerala's golden age of equality.",
    sections_json=[
        {"id": "golden-age", "label": "The Golden Age of Mahabali"},
        {"id": "vamana-avatar", "label": "Vamana Avatar"},
        {"id": "sacrifice", "label": "The Great Sacrifice"},
        {"id": "onam-connection", "label": "Connection to Onam"},
        {"id": "cultural-meaning", "label": "Cultural Significance"},
        {"id": "modern-relevance", "label": "Modern Relevance"},
    ],
    study_materials=[
        {"title": "The Golden Age", "text": "King Mahabali (Maveli) was an Asura king who ruled Kerala during a legendary golden age. Under his rule, there was absolute equality \u2013 no theft, no dishonesty, no caste discrimination.\n\n**The People's Song:**\n*'Maveli naadu vaneedum kaalam, Manushyarellarum onnu pole'*\n(When Maveli ruled the land, all people were equal)"},
        {"title": "Vamana Avatar", "text": "The gods grew jealous of Mahabali's popularity. Lord Vishnu took the form of Vamana, a dwarf Brahmin boy, and visited Mahabali's court during a grand yajna (fire ritual).\n\nVamana asked for just three paces of land. Mahabali, known for his generosity, agreed despite warnings from his guru Shukracharya."},
        {"title": "The Great Sacrifice", "text": "Vamana grew to cosmic proportions. With his first step he covered the Earth, with his second the Heavens. For the third step, Mahabali offered his own head.\n\nImpressed by his devotion and selflessness, Vishnu granted Mahabali a boon: he could return to visit his people once every year."},
        {"title": "Connection to Onam", "text": "Onam is the annual celebration of Mahabali's homecoming. Keralites believe he visits during the festival to see if his people are happy.\n\n**Onam Traditions:**\n* Pookalam (flower carpet) \u2013 To welcome Maveli\n* Onasadya (feast) \u2013 26-course vegetarian meal\n* Vallam Kali \u2013 Snake boat races\n* Pulikali \u2013 Tiger dance performances"},
        {"title": "Cultural Significance", "text": "Mahabali's legend is unique because an Asura (demon king) is celebrated as the hero, not the deity who defeated him. This reflects Kerala's values of:\n* **Social Equality** \u2013 Mahabali's rule had no caste\n* **Generosity** \u2013 His willingness to sacrifice everything\n* **People over Power** \u2013 The people's love transcended divine authority"},
        {"title": "Modern Relevance", "text": "The Mahabali legend continues to shape Kerala's identity:\n* Social reform movements invoked Mahabali's egalitarian rule\n* Politicians reference 'Maveli's Kerala' as an ideal\n* The story is taught in schools as a lesson in humility and generosity\n* Onam unites all religions in Kerala \u2013 celebrated by Hindus, Christians, and Muslims alike"},
    ],
    mcqs=[
        {"question_text": "What was special about Mahabali's rule?", "option_a": "Military power", "option_b": "Absolute equality", "option_c": "Wealth accumulation", "option_d": "Religious dominance", "correct_option": "B", "explanation": "His rule represented a golden age of equality."},
        {"question_text": "Which avatar did Vishnu take to visit Mahabali?", "option_a": "Rama", "option_b": "Krishna", "option_c": "Vamana", "option_d": "Narasimha", "correct_option": "C", "explanation": "Vishnu took the form of Vamana, a dwarf Brahmin."},
        {"question_text": "What did Vamana ask for?", "option_a": "Gold", "option_b": "A kingdom", "option_c": "Three paces of land", "option_d": "An army", "correct_option": "C", "explanation": "Vamana asked for just three paces of land."},
        {"question_text": "What boon was granted to Mahabali?", "option_a": "Immortality", "option_b": "Return to visit his people yearly", "option_c": "A new kingdom", "option_d": "Divine powers", "correct_option": "B", "explanation": "He was allowed to visit Kerala once a year (Onam)."},
        {"question_text": "What is a Pookalam?", "option_a": "A traditional meal", "option_b": "A flower carpet", "option_c": "A boat race", "option_d": "A temple ritual", "correct_option": "B", "explanation": "Pookalam is a flower carpet made to welcome Maveli."},
        {"question_text": "How many courses are in a traditional Onasadya?", "option_a": "12", "option_b": "18", "option_c": "26", "option_d": "32", "correct_option": "C", "explanation": "Onasadya traditionally has 26 courses."},
        {"question_text": "Why is Mahabali's legend unique?", "option_a": "A god is the hero", "option_b": "An Asura is celebrated as the hero", "option_c": "It's about war", "option_d": "It's a creation myth", "correct_option": "B", "explanation": "Unusually, the Asura king is the hero, not the deity."},
        {"question_text": "Who warned Mahabali about Vamana?", "option_a": "Indra", "option_b": "Shukracharya", "option_c": "Brahma", "option_d": "Narada", "correct_option": "B", "explanation": "His guru Shukracharya warned him."},
    ]
)

# --- Lowlands (Coastal Plains) ---
seed_topic(
    title="Lowlands (Coastal Plains)", category="environment",
    section_name="Environment",
    description="The narrow coastal strip of Kerala stretching 580 km along the Arabian Sea, home to fishing communities and coconut groves.",
    sections_json=[
        {"id": "geography", "label": "Geography & Formation"},
        {"id": "marine-life", "label": "Marine Ecosystems"},
        {"id": "fishing-communities", "label": "Fishing Communities"},
        {"id": "coconut-economy", "label": "Coconut Economy"},
        {"id": "coastal-threats", "label": "Coastal Erosion & Threats"},
        {"id": "conservation", "label": "Conservation Efforts"},
    ],
    study_materials=[
        {"title": "Geography & Formation", "text": "Kerala's coastal plains stretch 580 km from Kasaragod to Thiruvananthapuram, rarely exceeding 25 km in width. The coastline was formed by alluvial deposits and marine regression over millennia.\n\n**Key Features:**\n* 44 rivers drain into the Arabian Sea\n* Laterite cliffs alternate with sandy beaches\n* Barrier islands and spits create lagoons (kayals)"},
        {"title": "Marine Ecosystems", "text": "The coastal waters support rich biodiversity:\n* **Coral Reefs** near Lakshadweep fringes\n* **Mangrove Forests** in Kannur, Kochi, and Vypeen\n* **Sea Turtle Nesting** sites along Kozhikode and Kannur\n* Over 300 species of marine fish sustain Kerala's fishing industry"},
        {"title": "Fishing Communities", "text": "Fishing is the lifeblood of coastal Kerala. The main communities are:\n* **Mukkuvar** \u2013 Traditional Catholic fishing community\n* **Dheevara** \u2013 Hindu fishing community\n* **Mappila fishermen** \u2013 Muslim coastal communities\n\nTraditional fishing methods include Cheena Vala (Chinese nets), country boats (vallam), and net casting."},
        {"title": "Coconut Economy", "text": "Kerala literally means 'Land of Coconuts'. The coastal belt is the heartland of coconut cultivation.\n\n**Economic Impact:**\n* Kerala produces 45% of India's coconuts\n* Coir (coconut fiber) industry employs over 500,000 people\n* Coconut oil is central to Kerala cuisine and Ayurvedic medicine\n* Toddy (palm wine) tapping is a traditional coastal occupation"},
        {"title": "Coastal Erosion & Threats", "text": "Kerala's coastline faces severe erosion:\n* Over 60% of the coast experiences erosion\n* Chellanam village near Kochi is critically threatened\n* Rising sea levels due to climate change\n* Sand mining has destabilized coastal formations\n\nThe 2018 floods devastated coastal communities, displacing millions."},
        {"title": "Conservation Efforts", "text": "Active conservation initiatives:\n* **Shoreline Management Plans** by Kerala State Coastal Zone Management Authority\n* **Mangrove restoration** in Kannur district\n* **Marine Protected Areas** near Vizhinjam\n* **Community-based fishing regulations** to prevent overfishing\n* The Pulicat Lake Bird Sanctuary model is being replicated"},
    ],
    mcqs=[
        {"question_text": "How long is Kerala's coastline?", "option_a": "380 km", "option_b": "480 km", "option_c": "580 km", "option_d": "680 km", "correct_option": "C", "explanation": "Kerala's coast stretches 580 km."},
        {"question_text": "What does 'Kerala' literally mean?", "option_a": "Land of Rivers", "option_b": "Land of Coconuts", "option_c": "God's Country", "option_d": "Land of Spices", "correct_option": "B", "explanation": "Kerala means Land of Coconuts."},
        {"question_text": "What percentage of India's coconuts does Kerala produce?", "option_a": "25%", "option_b": "35%", "option_c": "45%", "option_d": "55%", "correct_option": "C", "explanation": "Kerala produces 45% of India's coconuts."},
        {"question_text": "What is Cheena Vala?", "option_a": "A boat type", "option_b": "Chinese fishing nets", "option_c": "A fish species", "option_d": "A coastal village", "correct_option": "B", "explanation": "Cheena Vala are Chinese fishing nets."},
        {"question_text": "How many rivers drain into the Arabian Sea from Kerala?", "option_a": "34", "option_b": "44", "option_c": "54", "option_d": "64", "correct_option": "B", "explanation": "44 rivers drain into the Arabian Sea."},
        {"question_text": "What is coir?", "option_a": "Palm wine", "option_b": "A fish variety", "option_c": "Coconut fiber", "option_d": "A type of boat", "correct_option": "C", "explanation": "Coir is coconut fiber used in many industries."},
        {"question_text": "Which coastal village near Kochi is critically threatened by erosion?", "option_a": "Marari", "option_b": "Chellanam", "option_c": "Vypeen", "option_d": "Ponnani", "correct_option": "B", "explanation": "Chellanam faces critical coastal erosion."},
        {"question_text": "What are kayals?", "option_a": "Boats", "option_b": "Fish traps", "option_c": "Coastal lagoons", "option_d": "Sand dunes", "correct_option": "C", "explanation": "Kayals are lagoons formed by barrier islands."},
    ]
)

# --- Midlands ---
seed_topic(
    title="Midlands (The Transition Belt)", category="environment",
    section_name="Environment",
    description="The undulating midland region between the coast and the Western Ghats, known for rubber, spice plantations, and paddy fields.",
    sections_json=[
        {"id": "terrain", "label": "Terrain & Landscape"},
        {"id": "agriculture", "label": "Agricultural Economy"},
        {"id": "spice-gardens", "label": "Spice Gardens"},
        {"id": "rivers", "label": "Rivers & Water Systems"},
        {"id": "biodiversity", "label": "Midland Biodiversity"},
        {"id": "urbanization", "label": "Urbanization Challenges"},
    ],
    study_materials=[
        {"title": "Terrain & Landscape", "text": "The midlands lie between 7.5m and 75m above sea level, forming a transition belt of rolling hills, valleys, and laterite plateaus.\n\n**Key Features:**\n* Laterite soil ideal for rubber and cashew\n* Paddy fields (puncha) in river valleys\n* Elevation gradually increases eastward toward the Ghats"},
        {"title": "Agricultural Economy", "text": "The midlands are Kerala's agricultural heartland:\n* **Rubber** \u2013 Kerala produces 90% of India's natural rubber\n* **Cashew** \u2013 Kollam district is the cashew capital\n* **Paddy** \u2013 Palakkad (the 'Granary of Kerala') has extensive rice fields\n* **Tapioca** \u2013 A staple food crop for midland communities"},
        {"title": "Spice Gardens", "text": "The eastern midlands transition into spice-growing zones:\n* **Pepper** \u2013 'Black Gold' that attracted global traders\n* **Cardamom** \u2013 'Queen of Spices', grown in Idukki hills\n* **Ginger & Turmeric** \u2013 Essential to Kerala cuisine\n* **Cinnamon & Cloves** \u2013 Concentrated in Wayanad and Idukki"},
        {"title": "Rivers & Water Systems", "text": "44 west-flowing rivers originate in the Western Ghats and flow through the midlands:\n* **Periyar** (244 km) \u2013 Kerala's longest river\n* **Bharathapuzha** (209 km) \u2013 Second longest, 'Lifeline of Palakkad'\n* **Pamba** \u2013 Sacred river associated with Sabarimala\n\nTraditional water management includes surangams (horizontal wells) in Kasaragod."},
        {"title": "Midland Biodiversity", "text": "The midlands host diverse ecosystems:\n* **Sacred Groves (Kavus)** \u2013 Protected forest patches around temples\n* **Wetland paddy ecosystems** with frogs, snakes, and migratory birds\n* **Laterite rock pools** harbor unique aquatic species\n\nKavus are among India's oldest community conservation models."},
        {"title": "Urbanization Challenges", "text": "Rapid urbanization threatens midland ecosystems:\n* **Laterite mining** for construction destroys habitats\n* **Paddy field conversion** to residential plots\n* **River pollution** from domestic and industrial waste\n* **Hill cutting** destabilizes slopes (2018 Landslides)\n\nKerala's ribbon development pattern means cities sprawl along roads, fragmenting habitats."},
    ],
    mcqs=[
        {"question_text": "What percentage of India's rubber does Kerala produce?", "option_a": "70%", "option_b": "80%", "option_c": "90%", "option_d": "60%", "correct_option": "C", "explanation": "Kerala produces 90% of India's natural rubber."},
        {"question_text": "Which is Kerala's longest river?", "option_a": "Pamba", "option_b": "Bharathapuzha", "option_c": "Periyar", "option_d": "Chaliyar", "correct_option": "C", "explanation": "Periyar (244 km) is the longest."},
        {"question_text": "What is Palakkad known as?", "option_a": "Spice Capital", "option_b": "Granary of Kerala", "option_c": "Cashew Capital", "option_d": "Rubber Hub", "correct_option": "B", "explanation": "Palakkad is called the Granary of Kerala."},
        {"question_text": "What are Kavus?", "option_a": "Rice fields", "option_b": "Sacred groves", "option_c": "Fishing ponds", "option_d": "Spice gardens", "correct_option": "B", "explanation": "Kavus are sacred groves protected around temples."},
        {"question_text": "What is pepper known as in the spice trade?", "option_a": "Queen of Spices", "option_b": "Black Gold", "option_c": "King of Flavors", "option_d": "Green Diamond", "correct_option": "B", "explanation": "Pepper was called Black Gold."},
        {"question_text": "What is a surangam?", "option_a": "A spice", "option_b": "A horizontal well", "option_c": "A boat", "option_d": "A temple", "correct_option": "B", "explanation": "Surangams are horizontal wells in Kasaragod."},
        {"question_text": "Which district is the cashew capital of Kerala?", "option_a": "Palakkad", "option_b": "Idukki", "option_c": "Kollam", "option_d": "Wayanad", "correct_option": "C", "explanation": "Kollam is the cashew capital."},
        {"question_text": "What spice is called the Queen of Spices?", "option_a": "Pepper", "option_b": "Cinnamon", "option_c": "Cardamom", "option_d": "Turmeric", "correct_option": "C", "explanation": "Cardamom is the Queen of Spices."},
    ]
)

# --- Below Sea Level (Kuttanad) ---
seed_topic(
    title="Below Sea Level (Kuttanad)", category="environment",
    section_name="Environment",
    description="Kuttanad is one of the few places in the world where farming is done below sea level, a unique agricultural marvel.",
    sections_json=[
        {"id": "geography", "label": "Geography & Formation"},
        {"id": "below-sea-farming", "label": "Below Sea Level Farming"},
        {"id": "polders", "label": "The Polder System"},
        {"id": "ecology", "label": "Wetland Ecology"},
        {"id": "challenges", "label": "Environmental Challenges"},
        {"id": "fao-recognition", "label": "FAO GIAHS Recognition"},
    ],
    study_materials=[
        {"title": "Geography & Formation", "text": "Kuttanad, in Alappuzha district, lies 0.6 to 2.2 meters below sea level. It is one of only two regions in India (and few in the world) where farming happens below sea level. The region was formed by the sedimentation of five rivers: Pamba, Achankovil, Manimala, Meenachil, and Muvattupuzha."},
        {"title": "Below Sea Level Farming", "text": "Kuttanad is called the 'Rice Bowl of Kerala'. Farmers have practiced below-sea-level rice cultivation for centuries using ingenious water management:\n* **Kayal Farming** \u2013 Reclaiming lake beds for paddy\n* **Punja Cultivation** \u2013 Rice farming in the dry season (Dec-May)\n* The unique Pokkali rice variety is salt-tolerant and organic"},
        {"title": "The Polder System", "text": "Like the Netherlands, Kuttanad uses a polder system:\n* Bunds (embankments) keep water out of fields\n* Pettis (sluice gates) control water flow\n* Chakkrams (water wheels) were traditionally used for drainage\n\nThis centuries-old engineering is entirely community-managed."},
        {"title": "Wetland Ecology", "text": "Kuttanad is part of the Vembanad-Kol wetland, a Ramsar site (internationally important wetland).\n\n**Biodiversity:**\n* Habitat for 100+ bird species including migratory species\n* Freshwater fish diversity\n* Mangrove patches along waterways\n* The Vembanad Lake is Kerala's largest lake (2,033 sq km)"},
        {"title": "Environmental Challenges", "text": "Kuttanad faces severe threats:\n* **Saltwater intrusion** from Vembanad Lake\n* **Pesticide pollution** from rice farming\n* **Flooding** \u2013 Devastated in 2018 Kerala floods\n* **Loss of paddy land** to fish farming (prawn culture)\n* **Climate change** is raising water levels further"},
        {"title": "FAO GIAHS Recognition", "text": "In 2013, the Food and Agriculture Organization (FAO) designated Kuttanad as a Globally Important Agricultural Heritage System (GIAHS).\n\nThis recognizes:\n* The ingenuity of below-sea-level farming\n* Community-managed water infrastructure\n* Traditional rice varieties and organic practices\n* The sustainable coexistence of farming and fishing"},
    ],
    mcqs=[
        {"question_text": "How far below sea level is Kuttanad?", "option_a": "0.1 to 0.5m", "option_b": "0.6 to 2.2m", "option_c": "3 to 5m", "option_d": "5 to 8m", "correct_option": "B", "explanation": "Kuttanad lies 0.6 to 2.2 meters below sea level."},
        {"question_text": "What is Kuttanad called?", "option_a": "Spice Garden", "option_b": "Rice Bowl of Kerala", "option_c": "God's Own Country", "option_d": "Venice of the East", "correct_option": "B", "explanation": "Kuttanad is known as the Rice Bowl of Kerala."},
        {"question_text": "What recognition did FAO give Kuttanad in 2013?", "option_a": "World Heritage Site", "option_b": "GIAHS", "option_c": "Biosphere Reserve", "option_d": "National Park", "correct_option": "B", "explanation": "FAO designated it a Globally Important Agricultural Heritage System."},
        {"question_text": "How many rivers form Kuttanad?", "option_a": "3", "option_b": "4", "option_c": "5", "option_d": "6", "correct_option": "C", "explanation": "Five rivers: Pamba, Achankovil, Manimala, Meenachil, Muvattupuzha."},
        {"question_text": "What is the Pokkali variety?", "option_a": "A fish species", "option_b": "A salt-tolerant rice", "option_c": "A boat type", "option_d": "A water wheel", "correct_option": "B", "explanation": "Pokkali is a salt-tolerant organic rice variety."},
        {"question_text": "What is the Vembanad-Kol wetland designated as?", "option_a": "UNESCO site", "option_b": "National Park", "option_c": "Ramsar site", "option_d": "Tiger Reserve", "correct_option": "C", "explanation": "It is an internationally important Ramsar site."},
        {"question_text": "What is a petti in the Kuttanad system?", "option_a": "A rice variety", "option_b": "A sluice gate", "option_c": "A fishing net", "option_d": "A boat", "correct_option": "B", "explanation": "Pettis are sluice gates that control water flow."},
        {"question_text": "What is the area of Vembanad Lake?", "option_a": "1,033 sq km", "option_b": "2,033 sq km", "option_c": "3,033 sq km", "option_d": "500 sq km", "correct_option": "B", "explanation": "Vembanad Lake covers 2,033 sq km."},
    ]
)

# --- Geographic History of Kerala ---
seed_topic(
    title="The Geographic History of Kerala: From Gondwana to the Arabian Sea", category="heritage",
    section_name="Kerala history",
    description="The geological and geographic evolution of Kerala from the ancient supercontinent Gondwana to its present-day form.",
    sections_json=[
        {"id": "gondwana", "label": "Gondwana Origins"},
        {"id": "western-ghats", "label": "Rise of the Western Ghats"},
        {"id": "parasurama", "label": "The Parasurama Legend"},
        {"id": "coastline", "label": "Coastline Formation"},
        {"id": "rivers-lakes", "label": "Rivers & Lake Systems"},
        {"id": "modern-geography", "label": "Modern Geographic Identity"},
    ],
    study_materials=[
        {"title": "Gondwana Origins", "text": "Kerala's geological story begins 130 million years ago when the Indian plate broke off from ancient Gondwana.\n\n**Key Events:**\n* India drifted northward at ~15 cm/year\n* The Western Ghats formed through tectonic uplift\n* The coastal strip emerged from marine regression\n* Laterite rocks (60\u201370 million years old) form much of Kerala's landscape"},
        {"title": "Rise of the Western Ghats", "text": "The Western Ghats, older than the Himalayas, formed during the Cretaceous period.\n\n* They run 1,600 km along India's western edge\n* Anamudi (2,695m) in Kerala is the highest peak in South India\n* The Ghats create a 'rain shadow' effect\u2014Kerala gets heavy monsoons while Tamil Nadu stays dry\n* UNESCO World Heritage Site since 2012"},
        {"title": "The Parasurama Legend", "text": "According to mythology, Kerala was created when the sage Parasurama threw his axe from Gokarnam into the sea. The land rose from the ocean.\n\nThis legend may reflect actual geological processes:\n* Marine regression did expose new land\n* Ancient temples are found near the coast, suggesting progressive land formation\n* The legend explains Kerala's narrow, linear geography"},
        {"title": "Coastline Formation", "text": "Kerala's 580 km coast was shaped by:\n* Alluvial deposits from 44 rivers\n* Marine regression over millennia\n* Formation of barrier beaches and lagoons\n* Tectonic activity along the Konkan-Kerala coast\n\nThe result is a unique geography: mountains, midlands, coast, and below-sea-level regions in just 120 km width."},
        {"title": "Rivers & Lake Systems", "text": "Kerala has 44 rivers, all originating in the Western Ghats:\n* **West-flowing (41)**: Short, swift rivers creating waterfalls\n* **East-flowing (3)**: Kabini, Bhavani, Pambar flow to Tamil Nadu\n* **Vembanad Lake**: Kerala's largest, connecting backwaters\n* **Ashtamudi Lake**: A gateway to Kerala's backwater network\n\nThese rivers shaped Kerala's settlement patterns and agricultural systems."},
        {"title": "Modern Geographic Identity", "text": "Kerala's four geographic zones create its distinctive identity:\n1. **Highlands** (Western Ghats) \u2013 Tea, coffee, spice plantations\n2. **Midlands** \u2013 Rubber, paddy, cashew\n3. **Lowlands** \u2013 Coconut, fishing, trade\n4. **Below Sea Level** (Kuttanad) \u2013 Rice farming\n\nThis compression of four ecosystems into 120 km width makes Kerala one of India's most ecologically diverse states."},
    ],
    mcqs=[
        {"question_text": "When did the Indian plate break from Gondwana?", "option_a": "65 million years ago", "option_b": "130 million years ago", "option_c": "200 million years ago", "option_d": "50 million years ago", "correct_option": "B", "explanation": "The Indian plate separated ~130 million years ago."},
        {"question_text": "What is the highest peak in South India?", "option_a": "Doddabetta", "option_b": "Anamudi", "option_c": "Mullayanagiri", "option_d": "Meesapulimala", "correct_option": "B", "explanation": "Anamudi at 2,695m is the highest peak in South India."},
        {"question_text": "Who created Kerala according to mythology?", "option_a": "Vishnu", "option_b": "Brahma", "option_c": "Parasurama", "option_d": "Shiva", "correct_option": "C", "explanation": "Parasurama threw his axe to create Kerala from the sea."},
        {"question_text": "How many rivers does Kerala have?", "option_a": "34", "option_b": "44", "option_c": "54", "option_d": "24", "correct_option": "B", "explanation": "Kerala has 44 rivers."},
        {"question_text": "When were the Western Ghats declared a UNESCO site?", "option_a": "2008", "option_b": "2010", "option_c": "2012", "option_d": "2015", "correct_option": "C", "explanation": "UNESCO World Heritage Site since 2012."},
        {"question_text": "What is the width of Kerala at its widest?", "option_a": "60 km", "option_b": "90 km", "option_c": "120 km", "option_d": "150 km", "correct_option": "C", "explanation": "Kerala is about 120 km at its widest."},
        {"question_text": "How many of Kerala's rivers flow westward?", "option_a": "38", "option_b": "41", "option_c": "44", "option_d": "35", "correct_option": "B", "explanation": "41 of 44 rivers flow westward."},
        {"question_text": "Which geographic zones make up Kerala?", "option_a": "Two", "option_b": "Three", "option_c": "Four", "option_d": "Five", "correct_option": "C", "explanation": "Highlands, Midlands, Lowlands, and Below Sea Level."},
    ]
)

print("\n" + "="*60)
print("PART 1 COMPLETE: All 7 existing empty topics enriched!")
print("="*60)
print("\nContinue to Part 3 by running: python seed_kerala_content_p3.py")
