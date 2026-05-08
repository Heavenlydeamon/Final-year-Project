"""
Kerala Content Expansion - Part 3b: Remaining 7 New Topics
Run: python seed_kerala_content_p3b.py
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
    section = get_or_create_section(section_name)
    ct, created = ContentTopic.objects.get_or_create(
        title=title,
        defaults={'category': category, 'class_level': 'higher', 'description': description,
                  'is_published': True, 'created_by': admin_user, 'thumbnail': 'topics/default.jpg'}
    )
    if not created and not ct.sections: ct.description = description
    ct.sections = sections_json
    ct.save()
    mt, _ = MainTopic.objects.get_or_create(name=title, section=section, defaults={'description': description, 'is_general': True})
    if StudyMaterial.objects.filter(topic=mt).count() <= 1:
        StudyMaterial.objects.filter(topic=mt).delete()
        for i, sm in enumerate(study_materials):
            StudyMaterial.objects.create(topic=mt, title=sm['title'], content_text=sm['text'], order=i+1)
    if not Quiz.objects.filter(topic=ct).exists():
        quiz = Quiz.objects.create(title=f"{title} Assessment", topic=ct, created_by=admin_user, source='admin', is_challenge_eligible=True)
        for q in mcqs: MCQQuestion.objects.create(quiz=quiz, **q)
        print(f"  + Quiz created ({len(mcqs)} MCQs)")
    else: print(f"  ~ Quiz already exists")
    print(f"{'Created' if created else 'Updated'}: {title}")

print("="*60)
print("PART 3b: Creating remaining 7 new topics")
print("="*60)

# 4. Ayurveda
seed_topic("Ayurveda in Kerala", "heritage", "Heritage Sites",
    "Kerala is the global capital of Ayurveda, the ancient Indian system of medicine that has been practiced here for over 3,000 years.",
    [{"id":"origins","label":"Origins & Philosophy"},{"id":"practices","label":"Key Practices"},{"id":"herbs","label":"Medicinal Herbs"},{"id":"panchakarma","label":"Panchakarma"},{"id":"tourism","label":"Ayurveda Tourism"},{"id":"modern","label":"Modern Integration"}],
    [{"title":"Origins & Philosophy","text":"Ayurveda ('Science of Life') originated from the Atharva Veda (1500 BCE). Kerala became its stronghold because:\n* The Ashtavaidya families (8 physician lineages) preserved ancient texts\n* Kerala's tropical climate supports 1,500+ medicinal plant species\n* The monsoon season (Karkidakam) is considered ideal for treatment\n* Vagbhata's Ashtanga Hridayam is the primary text used in Kerala"},
     {"title":"Key Practices","text":"**Three Doshas:** All bodies are governed by Vata, Pitta, and Kapha.\n\n**Key Treatments:**\n* Dhara – Oil poured on the forehead (for stress)\n* Pizhichil – Warm oil bath (for arthritis)\n* Njavara Kizhi – Rice poultice massage\n* Sirovasti – Oil retained on scalp in a leather cap\n* Elakizhi – Herbal leaf bundle massage"},
     {"title":"Medicinal Herbs","text":"Kerala's forests yield critical Ayurvedic ingredients:\n* **Ashwagandha** – Stress relief\n* **Turmeric (Manjal)** – Anti-inflammatory\n* **Brahmi** – Brain tonic\n* **Neem (Veppu)** – Blood purifier\n* **Amla (Nellikka)** – Immunity booster\n* **Kacholam** – Digestive aid\n\nOver 900 formulations use native Kerala plants."},
     {"title":"Panchakarma","text":"Panchakarma ('five actions') is Ayurveda's detox system:\n1. **Vamana** – Therapeutic vomiting\n2. **Virechana** – Purgation\n3. **Nasya** – Nasal medication\n4. **Basti** – Medicated enema\n5. **Raktamokshana** – Blood purification\n\nKerala's version emphasizes oil therapies (Snehana) unique to the region."},
     {"title":"Ayurveda Tourism","text":"Kerala attracts millions for Ayurvedic wellness:\n* Kottakkal Arya Vaidya Sala (est. 1902) is world-renowned\n* Major hubs: Thrissur, Palakkad, Kannur, Wayanad\n* Government-certified treatment centers number 2,500+\n* Kerala Tourism markets 'Monsoon packages' for Panchakarma\n* Revenue exceeds ₹5,000 crore annually"},
     {"title":"Modern Integration","text":"Ayurveda is officially integrated into Kerala's healthcare:\n* Government Ayurveda hospitals in every district\n* Ayurveda degrees (BAMS) from 15+ colleges\n* Research at AVS Kottakkal and CSIR-NBRI\n* WHO recognizes Kerala's Ayurvedic practices\n* AYUSH Ministry promotes standardization globally"}],
    [{"question_text":"What does Ayurveda mean?","option_a":"Science of Herbs","option_b":"Science of Life","option_c":"Science of Health","option_d":"Science of Nature","correct_option":"B","explanation":"Ayurveda means Science of Life."},
     {"question_text":"How many Doshas govern the body?","option_a":"2","option_b":"3","option_c":"4","option_d":"5","correct_option":"B","explanation":"Vata, Pitta, and Kapha."},
     {"question_text":"What is Panchakarma?","option_a":"A 5-step detox","option_b":"A diet plan","option_c":"A yoga routine","option_d":"A herbal mix","correct_option":"A","explanation":"Panchakarma means 'five actions' for detox."},
     {"question_text":"Which month is ideal for Ayurvedic treatment?","option_a":"Chingam","option_b":"Karkidakam","option_c":"Medam","option_d":"Thulam","correct_option":"B","explanation":"Karkidakam (monsoon) is ideal."},
     {"question_text":"What is Dhara?","option_a":"Massage","option_b":"Oil poured on forehead","option_c":"Herbal bath","option_d":"Yoga pose","correct_option":"B","explanation":"Dhara involves oil poured on the forehead."},
     {"question_text":"What herb is known as a brain tonic?","option_a":"Turmeric","option_b":"Neem","option_c":"Brahmi","option_d":"Amla","correct_option":"C","explanation":"Brahmi is used as a brain tonic."},
     {"question_text":"When was Kottakkal Arya Vaidya Sala established?","option_a":"1882","option_b":"1902","option_c":"1922","option_d":"1942","correct_option":"B","explanation":"Established in 1902."},
     {"question_text":"What text is primarily used in Kerala Ayurveda?","option_a":"Charaka Samhita","option_b":"Sushruta Samhita","option_c":"Ashtanga Hridayam","option_d":"Rigveda","correct_option":"C","explanation":"Vagbhata's Ashtanga Hridayam."}]
)

# 5. Vallam Kali
seed_topic("Vallam Kali (Snake Boat Race)", "heritage", "Cultural Artforms",
    "The spectacular snake boat races of Kerala, where 100-foot long Chundan Vallams slice through backwaters powered by synchronized rowing.",
    [{"id":"history","label":"Historical Origins"},{"id":"boats","label":"The Snake Boats"},{"id":"races","label":"Famous Races"},{"id":"culture","label":"Cultural Significance"},{"id":"training","label":"Training & Teamwork"},{"id":"modern","label":"Modern Revival"}],
    [{"title":"Historical Origins","text":"Vallam Kali dates back to the 13th century when kings of Chempakassery used war boats (Chundan Vallam) for naval battles. After warfare ceased, the tradition transformed into competitive racing.\n\nThe Champakulam Moolam Boat Race (est. 1595) is the oldest organized race."},
     {"title":"The Snake Boats","text":"Chundan Vallam ('snake boat') specs:\n* Length: 100-138 feet\n* Width: Just 5 feet at the widest\n* Weight: Over 2 tons\n* Rowers: 100-125 per boat\n* Built from Anjili wood (Artocarpus hirsutus)\n* Construction takes 6 months\n* No nails – planks stitched with coir rope\n\nThe raised stern resembles a cobra's hood, hence 'snake boat'."},
     {"title":"Famous Races","text":"**Nehru Trophy Boat Race:** Started in 1952 after PM Jawaharlal Nehru watched a race and was deeply moved. Held on Punnamada Lake, Alappuzha, on the 2nd Saturday of August.\n\n**Others:**\n* Aranmula Uthrattathi – Connected to Sree Parthasarathy Temple\n* Payippad Jalotsavam – 3-day festival\n* Presidents Trophy – Held in Kollam"},
     {"title":"Cultural Significance","text":"Boat races embody Kerala's community values:\n* **Teamwork:** 100+ rowers must synchronize perfectly\n* **Village Pride:** Each boat represents a village\n* **Vanchipattu:** Rhythmic rowing songs coordinate the crew\n* **Equality:** Rowers come from all castes and religions\n\nThe entire village contributes to building and maintaining the boat."},
     {"title":"Training & Teamwork","text":"Training begins months before race season:\n* Rowers practice dawn-to-dusk for 45 days\n* Special diet of kanji and fish\n* A 'helmsman' (amarakkaran) steers from the stern\n* Sync is achieved through Vanchipattu songs\n* Each beat of the song dictates the rowing rhythm\n\nOne out-of-sync oar can cost the entire race."},
     {"title":"Modern Revival","text":"Recent developments:\n* Champions Boat League (CBL) – Kerala's IPL-style league since 2019\n* International tourists flock to Nehru Trophy\n* Women's boat race introduced\n* Carbon fiber technology being explored (debated)\n* Government funding for traditional boat maintenance\n* TV broadcasting has expanded the audience globally"}],
    [{"question_text":"How long is a Chundan Vallam?","option_a":"50-70 feet","option_b":"100-138 feet","option_c":"150-200 feet","option_d":"30-50 feet","correct_option":"B","explanation":"Snake boats are 100-138 feet long."},
     {"question_text":"When was the Nehru Trophy started?","option_a":"1942","option_b":"1952","option_c":"1962","option_d":"1972","correct_option":"B","explanation":"Started in 1952."},
     {"question_text":"What are Vanchipattu?","option_a":"Battle cries","option_b":"Rowing songs","option_c":"Victory dances","option_d":"Prayer chants","correct_option":"B","explanation":"Vanchipattu are rhythmic rowing songs."},
     {"question_text":"Which is the oldest boat race?","option_a":"Nehru Trophy","option_b":"Aranmula","option_c":"Champakulam Moolam","option_d":"Presidents Trophy","correct_option":"C","explanation":"Champakulam Moolam dates to 1595."},
     {"question_text":"How many rowers per snake boat?","option_a":"50-60","option_b":"100-125","option_c":"60-80","option_d":"200+","correct_option":"B","explanation":"100-125 rowers per boat."},
     {"question_text":"What wood are snake boats made from?","option_a":"Teak","option_b":"Anjili","option_c":"Mahogany","option_d":"Bamboo","correct_option":"B","explanation":"Anjili wood (Artocarpus hirsutus)."},
     {"question_text":"What is the CBL?","option_a":"Cricket league","option_b":"Champions Boat League","option_c":"Cultural Board","option_d":"Coir Business","correct_option":"B","explanation":"Champions Boat League, Kerala's IPL-style boat race."},
     {"question_text":"Why is the boat called a snake boat?","option_a":"Snake carvings","option_b":"Stern resembles cobra hood","option_c":"Speed like a snake","option_d":"Used to catch snakes","correct_option":"B","explanation":"The raised stern resembles a cobra's hood."}]
)

# 6. Kerala Cuisine & Spice Trade
seed_topic("Kerala Cuisine and Spice Trade", "heritage", "Heritage Sites",
    "Kerala's unique culinary traditions shaped by millennia of spice trade with Rome, China, Arabia, and Europe.",
    [{"id":"spice-history","label":"The Spice Route"},{"id":"sadya","label":"The Kerala Sadya"},{"id":"non-veg","label":"Non-Vegetarian Traditions"},{"id":"snacks","label":"Tea-time Snacks"},{"id":"beverages","label":"Traditional Beverages"},{"id":"fusion","label":"Cultural Fusion Cuisine"}],
    [{"title":"The Spice Route","text":"Kerala was the world's spice capital for over 2,000 years.\n\n**Historical Trade:**\n* Roman Empire traded gold for Kerala pepper\n* Arab merchants established spice networks by 7th century CE\n* Vasco da Gama reached Calicut in 1498 seeking spices\n* 'Black Gold' (pepper) and 'Queen of Spices' (cardamom) were Kerala's exports\n\nMuziris was the primary port, trading with 30+ civilizations."},
     {"title":"The Kerala Sadya","text":"A traditional vegetarian feast served on banana leaf with 26+ items:\n* **Center:** Rice, Sambar, Rasam\n* **Top row:** Pickle, Pappadam, Banana chips\n* **Curries:** Avial, Olan, Kalan, Erissery, Koottukari\n* **Payasam:** Pradhaman (ada, pal, parippu varieties)\n\nEverything is eaten by hand. The leaf must be folded toward you after eating (folding away means dissatisfaction)."},
     {"title":"Non-Vegetarian Traditions","text":"Kerala has rich non-veg traditions across communities:\n* **Meen Pollichathu** – Fish in banana leaf (Syrian Christian)\n* **Malabar Biryani** – Kaima rice with meat (Muslim)\n* **Kozhi Curry** – Kerala chicken curry with coconut\n* **Karimeen Pollichathu** – Pearl spot fish grilled (Hindu)\n* **Duck Roast (Tharavu)** – Kottayam Christian specialty\n* **Prawn Masala** – Coastal Kerala specialty"},
     {"title":"Tea-time Snacks","text":"**Banana varieties:** Kerala has 20+ banana types used in cooking.\n\n**Popular Snacks:**\n* Pazham Pori – Banana fritters\n* Unniyappam – Sweet rice balls\n* Sukhiyan – Sweet dal fritters\n* Neyyappam – Ghee-fried rice cakes\n* Achappam – Rose cookies (Syrian Christian)\n* Kozhukatta – Sweet dumplings"},
     {"title":"Traditional Beverages","text":"* **Toddy (Kallu)** – Fermented coconut palm sap\n* **Sambharam** – Spiced buttermilk\n* **Sulaimani** – Malabar black tea with lemon\n* **Noon Chai** – Salted tea (Mappila influence)\n* **Panakam** – Jaggery-ginger water\n* **Tender coconut water** – Kerala's natural isotonic drink"},
     {"title":"Cultural Fusion Cuisine","text":"Each community contributed unique flavors:\n* **Syrian Christians:** Appam and stew, Duck roast, Wine-influenced meat preparations\n* **Mappilas:** Pathiri (rice bread), Kozhipathal, Unnakkaya\n* **Hindu traditions:** Sadya, Temple Prasadam like Aravana\n* **Jewish Cochin:** Pastel (meat-filled pastry), influenced by Sephardic traditions\n* **Anglo-Indian:** Cutlets, Ball curry from colonial era"}],
    [{"question_text":"Who reached Calicut seeking spices?","option_a":"Columbus","option_b":"Magellan","option_c":"Vasco da Gama","option_d":"Drake","correct_option":"C","explanation":"Vasco da Gama reached Calicut in 1498."},
     {"question_text":"What is Meen Pollichathu?","option_a":"Rice dish","option_b":"Fish in banana leaf","option_c":"Prawn curry","option_d":"Chicken roast","correct_option":"B","explanation":"Fish grilled inside banana leaf."},
     {"question_text":"How many banana types does Kerala have?","option_a":"5+","option_b":"10+","option_c":"20+","option_d":"50+","correct_option":"C","explanation":"Kerala has 20+ varieties of bananas."},
     {"question_text":"What is Sulaimani?","option_a":"A curry","option_b":"Black tea with lemon","option_c":"Coconut drink","option_d":"Rice porridge","correct_option":"B","explanation":"Malabar black tea with lemon."},
     {"question_text":"What is Appam?","option_a":"A rice pancake","option_b":"A banana fritter","option_c":"A meat dish","option_d":"A pickle","correct_option":"A","explanation":"Appam is a fermented rice pancake."},
     {"question_text":"What does folding the banana leaf toward you mean?","option_a":"Dissatisfaction","option_b":"Satisfaction","option_c":"Asking for more","option_d":"Nothing","correct_option":"B","explanation":"Folding toward you means satisfaction."},
     {"question_text":"What is toddy?","option_a":"Coffee","option_b":"Fermented coconut palm sap","option_c":"Fruit juice","option_d":"Herbal tea","correct_option":"B","explanation":"Toddy is fermented coconut palm sap."},
     {"question_text":"What was Kerala's ancient trading port?","option_a":"Calicut","option_b":"Muziris","option_c":"Quilon","option_d":"Cochin","correct_option":"B","explanation":"Muziris traded with 30+ civilizations."}]
)

# 7. Syrian Christians of Kerala
seed_topic("Syrian Christians of Kerala", "heritage", "Heritage Sites",
    "The 2,000-year-old Christian community of Kerala, tracing their origins to the Apostle St. Thomas, making it one of the oldest Christian communities in the world.",
    [{"id":"st-thomas","label":"St. Thomas Tradition"},{"id":"churches","label":"Ancient Churches"},{"id":"copper-plates","label":"The Copper Plates"},{"id":"denominations","label":"Denominations"},{"id":"culture","label":"Cultural Traditions"},{"id":"contributions","label":"Contributions to Kerala"}],
    [{"title":"St. Thomas Tradition","text":"According to tradition, the Apostle St. Thomas (Doubting Thomas) arrived in Muziris (Kodungallur) in 52 CE and established seven churches:\n1. Kodungallur\n2. Palayoor\n3. Kottakkavu (Paravur)\n4. Kokkamangalam\n5. Niranam\n6. Nilackal (Chayal)\n7. Kollam\n\nHe was martyred at Mylapore (Chennai) in 72 CE."},
     {"title":"Ancient Churches","text":"Kerala has some of the oldest churches outside the Roman Empire:\n* **Kodungallur Cheraman Church** – Possibly the first church in India\n* **Kottakkavu Church (Paravur)** – Among the seven St. Thomas churches\n* **St. Francis Church, Fort Kochi** – Where Vasco da Gama was originally buried (1503)\n* **Marth Mariam Church, Kuravilangad** – One of the oldest parishes\n\nArchitecturally, early Kerala churches blend Hindu temple and Christian designs."},
     {"title":"The Copper Plates","text":"The Tharisapalli Copper Plates (849 CE) are crucial historical evidence:\n* Granted by King Ayyanadikal Thiruvadikal to the Christian merchant Thomas of Kanai\n* Gave 72 privileges including tax exemptions and land rights\n* Written in Tamil, Pahlavi, Arabic, and Hebrew\n* Prove that Christians had a respected social position in medieval Kerala\n\nThese are preserved at the Kottayam Syrian Orthodox Seminary."},
     {"title":"Denominations","text":"Kerala's Syrian Christians branched into several denominations:\n* **Syro-Malabar Catholic Church** (Largest, ~4 million members)\n* **Malankara Orthodox Syrian Church**\n* **Jacobite Syrian Christian Church**\n* **Marthoma Syrian Church** (Reformed)\n* **Syro-Malankara Catholic Church**\n* **Church of South India (CSI)**\n\nDespite divisions, cultural unity remains strong."},
     {"title":"Cultural Traditions","text":"**Margam Kali:** Traditional dance depicting St. Thomas's journey\n**Oppana (Christian version):** Wedding celebration\n**Pesaha Appam:** Unleavened bread eaten on Maundy Thursday\n**Syrian Christian Wedding:** Mantrakodi (wedding saree) and Minnu (thali)\n**Festivals:** Easter, Christmas (with unique Kerala traditions), Feast of St. Thomas\n\nChristian homes feature Nasrani Menorah symbols."},
     {"title":"Contributions to Kerala","text":"Syrian Christians profoundly shaped Kerala:\n* **Education:** Founded schools and colleges (CMS, Mar Ivanios)\n* **Rubber Cultivation:** Pioneered rubber planting in Kottayam\n* **Press:** Started early Malayalam printing and newspapers\n* **Cuisine:** Introduced duck roast, appam-stew, wine cake traditions\n* **Architecture:** Unique 'Nalukettu-Church' hybrid style\n* **Social Reform:** Supported literacy and women's education movements"}],
    [{"question_text":"When did St. Thomas arrive in Kerala?","option_a":"32 CE","option_b":"52 CE","option_c":"72 CE","option_d":"100 CE","correct_option":"B","explanation":"Tradition says St. Thomas arrived in 52 CE."},
     {"question_text":"How many churches did St. Thomas establish?","option_a":"5","option_b":"7","option_c":"9","option_d":"12","correct_option":"B","explanation":"He established seven churches."},
     {"question_text":"What are the Tharisapalli Copper Plates?","option_a":"Ancient coins","option_b":"Royal decrees granting privileges to Christians","option_c":"Temple records","option_d":"Trade agreements","correct_option":"B","explanation":"Copper plates granting 72 privileges to Christians."},
     {"question_text":"Which is the largest Syrian Christian denomination?","option_a":"Orthodox","option_b":"Marthoma","option_c":"Syro-Malabar Catholic","option_d":"Jacobite","correct_option":"C","explanation":"Syro-Malabar Catholic has ~4 million members."},
     {"question_text":"What is Margam Kali?","option_a":"A martial art","option_b":"A dance depicting St. Thomas's journey","option_c":"A boat race","option_d":"A church hymn","correct_option":"B","explanation":"Traditional dance about St. Thomas."},
     {"question_text":"What is Pesaha Appam?","option_a":"Christmas cake","option_b":"Unleavened bread for Maundy Thursday","option_c":"Easter egg","option_d":"Wedding bread","correct_option":"B","explanation":"Eaten on Maundy Thursday."},
     {"question_text":"Where was St. Thomas martyred?","option_a":"Kodungallur","option_b":"Kochi","option_c":"Mylapore (Chennai)","option_d":"Goa","correct_option":"C","explanation":"St. Thomas was martyred at Mylapore in 72 CE."},
     {"question_text":"What is a Minnu?","option_a":"A cross","option_b":"A wedding thali/pendant","option_c":"A church bell","option_d":"A prayer book","correct_option":"B","explanation":"Minnu is the Syrian Christian wedding pendant."}]
)

# 8. Mappila Heritage
seed_topic("Mappila Heritage of Malabar", "heritage", "Heritage Sites",
    "The rich cultural legacy of Kerala's Mappila Muslim community, descended from Arab traders who brought Islam to the Malabar coast.",
    [{"id":"origins","label":"Arab Trade Origins"},{"id":"mosque","label":"Cheraman Juma Masjid"},{"id":"songs","label":"Mappila Songs"},{"id":"cuisine","label":"Mappila Cuisine"},{"id":"rebellion","label":"Malabar Rebellion"},{"id":"modern","label":"Modern Mappila Culture"}],
    [{"title":"Arab Trade Origins","text":"Islam arrived in Kerala through Arab traders during the Prophet's lifetime (7th century CE), making Kerala home to India's first mosque.\n\n**Key Facts:**\n* Arab traders married local women, creating the Mappila community\n* 'Mappila' means 'great child' or 'bridegroom' in Malayalam\n* Trade in pepper, cardamom, and timber sustained the community\n* Calicut (Kozhikode) was the main Mappila trading hub\n* The Zamorin kings of Calicut had strong Arab alliances"},
     {"title":"Cheraman Juma Masjid","text":"Built in 629 CE in Kodungallur, Cheraman Juma Masjid is believed to be India's first mosque.\n\n**Legend:** King Cheraman Perumal of Kerala converted to Islam after meeting the Prophet Muhammad. He traveled to Arabia and sent followers back with instructions to build the mosque.\n\n**Architecture:** The mosque originally had a traditional Kerala temple style – sloped roof, wooden architecture – showing how Islam adapted to local culture."},
     {"title":"Mappila Songs","text":"Mappila Pattu is a unique musical tradition blending Arabic melodies with Malayalam lyrics.\n\n**Types:**\n* **Oppana Pattu** – Wedding songs with clapping rhythm\n* **Kolkali Pattu** – Stick dance songs\n* **Ishal** – Love songs\n* **Padappattu** – War ballads (especially about the Malabar Rebellion)\n\nMoyinkutty Vaidyar (1852-1892) is the most famous Mappila poet, known for 'Badr Padappattu'."},
     {"title":"Mappila Cuisine","text":"Mappila food is distinct from other Kerala cuisines:\n* **Malabar Biryani** – Uses kaima (short-grain) rice, layered\n* **Pathiri** – Thin rice bread, eaten with curry\n* **Unnakkaya** – Sweet banana-filled snack\n* **Kozhipathal** – Chicken with thin rice sheets\n* **Mutta Mala** – Egg yolk strings (festive sweet)\n* **Sulaimani** – Lemon-black tea served after meals\n\nRamadan iftar spreads are legendary feasts."},
     {"title":"Malabar Rebellion","text":"The Mappila Rebellion of 1921 was a significant anti-colonial uprising:\n* Mappilas revolted against British colonial rule and landlord oppression\n* Led by Variyankunnathu Kunjahammed Haji\n* The Wagon Tragedy: 70 prisoners died in an airless railway wagon\n* The rebellion is seen as both a freedom struggle and an agrarian revolt\n* It highlighted the exploitation of Mappila tenant farmers by jenmis (landlords)"},
     {"title":"Modern Mappila Culture","text":"Today, Mappilas are integral to Kerala's identity:\n* **Gulf Migration:** Large Mappila diaspora in the Middle East has transformed Malabar's economy\n* **Education:** Muslim Educational Society (MES) runs 150+ institutions\n* **Art:** Mappila songs are mainstream Malayalam music\n* **Literature:** Vaikom Muhammad Basheer is one of Malayalam's greatest writers\n* **Festivals:** Eid, Milad-un-Nabi celebrated with Kerala-specific traditions\n* **Duff Muttu** and **Kolkali** are popular folk art performances"}],
    [{"question_text":"When was Cheraman Juma Masjid built?","option_a":"529 CE","option_b":"629 CE","option_c":"729 CE","option_d":"829 CE","correct_option":"B","explanation":"Built in 629 CE in Kodungallur."},
     {"question_text":"What does 'Mappila' mean?","option_a":"Trader","option_b":"Sailor","option_c":"Great child/bridegroom","option_d":"Fisher","correct_option":"C","explanation":"Means 'great child' or 'bridegroom'."},
     {"question_text":"What is Malabar Biryani's unique rice?","option_a":"Basmati","option_b":"Kaima","option_c":"Pokkali","option_d":"Jasmine","correct_option":"B","explanation":"Uses kaima (short-grain) rice."},
     {"question_text":"Who is the most famous Mappila poet?","option_a":"Basheer","option_b":"Moyinkutty Vaidyar","option_c":"Vallathol","option_d":"Asan","correct_option":"B","explanation":"Known for 'Badr Padappattu'."},
     {"question_text":"When was the Malabar Rebellion?","option_a":"1857","option_b":"1921","option_c":"1942","option_d":"1947","correct_option":"B","explanation":"The Mappila Rebellion occurred in 1921."},
     {"question_text":"What is Pathiri?","option_a":"A curry","option_b":"Thin rice bread","option_c":"Banana snack","option_d":"Sweet dessert","correct_option":"B","explanation":"Pathiri is thin rice bread."},
     {"question_text":"What is Oppana?","option_a":"A wedding dance/song celebration","option_b":"A war dance","option_c":"A prayer ritual","option_d":"A cooking style","correct_option":"A","explanation":"Wedding celebration with clapping rhythm."},
     {"question_text":"Who led the Malabar Rebellion?","option_a":"Pazhassi Raja","option_b":"Variyankunnathu Kunjahammed Haji","option_c":"Ayyankali","option_d":"Veluthampi Dalawa","correct_option":"B","explanation":"Led by Variyankunnathu Kunjahammed Haji."}]
)

# 9. Thrissur Pooram
seed_topic("Thrissur Pooram", "festivals", "Cultural Artforms",
    "The most spectacular temple festival in Kerala, featuring 30 caparisoned elephants, massive percussion ensembles, and a fireworks finale.",
    [{"id":"history","label":"History & Origins"},{"id":"pageant","label":"The Elephant Pageant"},{"id":"percussion","label":"Panchavadyam & Percussion"},{"id":"fireworks","label":"The Vedikkettu"},{"id":"rivalry","label":"Paramekkavu vs Thiruvambadi"},{"id":"significance","label":"Cultural Significance"}],
    [{"title":"History & Origins","text":"Thrissur Pooram was started by Sakthan Thampuran (Maharaja of Cochin) around 1798 CE. Previously, temples celebrated individually. Sakthan unified 10 temples into one grand festival at Vadakkunnathan Temple.\n\nIt falls in the Malayalam month of Medam (April-May) on the Pooram asterism."},
     {"title":"The Elephant Pageant","text":"The Kudamattam (umbrella ceremony) is Pooram's iconic highlight:\n* 15 elephants each from Paramekkavu and Thiruvambadi temples (30 total)\n* Each elephant carries decorated golden nettipattam (headdress)\n* Colorful silk parasols are exchanged in rapid succession\n* The crowd erupts at each umbrella change\n\nThrissur's tusker elephants are among the most famous in India."},
     {"title":"Panchavadyam & Percussion","text":"The sound of Pooram is overwhelming:\n* **Panchavadyam** – Ensemble of 5 instruments: Timila, Maddalam, Ilathalam, Idakka, Kombu\n* **Panchari Melam** – Rhythmic drumming escalating through 5 tempos\n* Over 250 percussionists perform simultaneously\n* The tempo builds from slow (1st kalam) to explosive (5th kalam)\n\nThis percussion is unique to Kerala temple festivals."},
     {"title":"The Vedikkettu","text":"Pooram climaxes with Kerala's greatest fireworks display:\n* Both temple groups compete with rival fireworks\n* Starts at 3 AM and lasts until dawn\n* Lakhs of people gather in Thekkinkadu Maidan\n* The display is competitive – each side tries to outperform the other\n* Worth crores of rupees in pyrotechnics\n\nThe Vedikkettu is considered one of the most spectacular fireworks in Asia."},
     {"title":"Paramekkavu vs Thiruvambadi","text":"The festival's energy comes from the friendly rivalry:\n* **Paramekkavu Bhagavathy Temple** (west side)\n* **Thiruvambadi Sri Krishna Temple** (east side)\n* Each group tries to outperform with better elephants, louder percussion, bigger fireworks\n* Supporters are as passionate as sports fans\n* The rivalry has continued for over 200 years"},
     {"title":"Cultural Significance","text":"Thrissur Pooram embodies Kerala's values:\n* **Secular:** All faiths attend – Christians and Muslims join celebrations\n* **Community:** Entire city participates regardless of caste\n* **Art Preservation:** Keeps percussion traditions alive\n* **Economic:** Generates massive tourism revenue\n* **Identity:** Often called 'The Festival of All Festivals'\n* Attendance exceeds 1 million visitors"}],
    [{"question_text":"Who started Thrissur Pooram?","option_a":"Zamorin","option_b":"Sakthan Thampuran","option_c":"Pazhassi Raja","option_d":"Marthanda Varma","correct_option":"B","explanation":"Started by Sakthan Thampuran around 1798."},
     {"question_text":"How many elephants participate?","option_a":"15","option_b":"20","option_c":"30","option_d":"50","correct_option":"C","explanation":"30 elephants (15 from each temple)."},
     {"question_text":"What is Kudamattam?","option_a":"Elephant decoration","option_b":"Umbrella exchange ceremony","option_c":"Fireworks display","option_d":"Drum performance","correct_option":"B","explanation":"Rapid exchange of colorful parasols."},
     {"question_text":"What is Vedikkettu?","option_a":"Percussion finale","option_b":"Elephant parade","option_c":"Competitive fireworks display","option_d":"Religious prayer","correct_option":"C","explanation":"The spectacular competitive fireworks."},
     {"question_text":"How many instruments in Panchavadyam?","option_a":"3","option_b":"5","option_c":"7","option_d":"10","correct_option":"B","explanation":"Pancha means five instruments."},
     {"question_text":"Which two temples compete?","option_a":"Guruvayur and Sabarimala","option_b":"Paramekkavu and Thiruvambadi","option_c":"Vadakkunnathan and Guruvayur","option_d":"Ettumanoor and Vaikom","correct_option":"B","explanation":"Paramekkavu vs Thiruvambadi."},
     {"question_text":"At what time does Vedikkettu start?","option_a":"6 PM","option_b":"Midnight","option_c":"3 AM","option_d":"6 AM","correct_option":"C","explanation":"Starts at 3 AM and lasts until dawn."},
     {"question_text":"How many tempos in Panchari Melam?","option_a":"3","option_b":"5","option_c":"7","option_d":"9","correct_option":"B","explanation":"Builds through 5 tempos (kalams)."}]
)

# 10. Nalukettu Architecture
seed_topic("Nalukettu - Traditional Kerala Architecture", "heritage", "Heritage Sites",
    "The traditional Kerala house with an open courtyard, designed with ancient Vastu principles for natural cooling, ventilation, and monsoon resilience.",
    [{"id":"design","label":"Design Principles"},{"id":"courtyard","label":"The Nadumuttam"},{"id":"materials","label":"Building Materials"},{"id":"social","label":"Social Organization"},{"id":"famous","label":"Famous Nalukettus"},{"id":"preservation","label":"Preservation Today"}],
    [{"title":"Design Principles","text":"Nalukettu literally means 'four blocks' – four wings built around a central courtyard.\n\n**Architectural Rules:**\n* Aligned North-South based on Thachu Shastra (carpentry science)\n* Sloped tiled roofs at steep angles for heavy monsoon rain\n* Wide verandas (Charupadi) for socializing\n* Height decreases from center outward\n* Built on a raised plinth (Utharam) to prevent flooding"},
     {"title":"The Nadumuttam","text":"The Nadumuttam (central courtyard) is the soul of the house:\n* Open to the sky for rain, light, and ventilation\n* Contains a Tulsi Thara (sacred basil platform)\n* Rainwater collected in an underground tank\n* Creates a natural chimney effect – hot air rises, cool air enters\n* Functions as the family's social and ritual hub\n* Larger homes have Ettukettu (8 blocks) or Pathinaarukettu (16 blocks)"},
     {"title":"Building Materials","text":"All materials are locally sourced:\n* **Teak (Thekku)** – Main structural wood\n* **Laterite stone** – Walls (naturally cooling)\n* **Clay tiles** – Roofing (handmade)\n* **Coconut palm** – Rafters and thatch\n* **Cow dung** – Mixed with clay for floor polishing\n* **Jack fruit wood (Plavu)** – Door frames and carvings\n\nNo cement or steel was used in traditional construction."},
     {"title":"Social Organization","text":"The Nalukettu's layout reflected social hierarchy:\n* **Thekkini (South block)** – Reception and formal area\n* **Vadakkini (North block)** – Kitchen and dining\n* **Kizhakkini (East block)** – Prayer room (Pooja Muri)\n* **Padinjattini (West block)** – Bedrooms and storage\n* **Ara** – Granary for rice storage\n* **Kulam** – Attached pond for bathing\n\nJoint families of 50+ members lived in large Nalukettus."},
     {"title":"Famous Nalukettus","text":"Notable surviving examples:\n* **Padmanabhapuram Palace** – Largest wooden palace in Asia\n* **Mattancherry Palace** – Dutch-Kerala hybrid\n* **Poonthanam Illam** – Poet's ancestral home\n* **Olappamanna Mana** – 400-year-old Brahmin Nalukettu in Palakkad\n* **Kuthiramalika Palace** – 122 wooden horse carvings\n* **Varikkasseri Mana** – Heritage hotel restoration success"},
     {"title":"Preservation Today","text":"Traditional Nalukettus face threats:\n* Urbanization is destroying heritage homes\n* Younger generations prefer modern apartments\n* Skilled Thachu (carpentry) craftsmen are disappearing\n\n**Conservation Efforts:**\n* Kerala Heritage Home scheme promotes restoration\n* Several Nalukettus converted to heritage hotels\n* INTACH (Indian National Trust) documents endangered homes\n* Architecture students study Thachu Shastra traditions"}],
    [{"question_text":"What does Nalukettu mean?","option_a":"Four rooms","option_b":"Four blocks","option_c":"Four floors","option_d":"Four doors","correct_option":"B","explanation":"Nalu = four, kettu = blocks."},
     {"question_text":"What is Nadumuttam?","option_a":"Kitchen","option_b":"Central open courtyard","option_c":"Prayer room","option_d":"Bedroom","correct_option":"B","explanation":"The open courtyard at the center."},
     {"question_text":"What is an Ettukettu?","option_a":"4-block house","option_b":"8-block house","option_c":"16-block house","option_d":"2-block house","correct_option":"B","explanation":"Ettu = eight, a larger house variant."},
     {"question_text":"What stone is used for walls?","option_a":"Granite","option_b":"Marble","option_c":"Laterite","option_d":"Sandstone","correct_option":"C","explanation":"Laterite stone naturally cools interiors."},
     {"question_text":"Which is the largest wooden palace in Asia?","option_a":"Mattancherry","option_b":"Padmanabhapuram","option_c":"Kuthiramalika","option_d":"Hill Palace","correct_option":"B","explanation":"Padmanabhapuram Palace in Kanyakumari."},
     {"question_text":"What is the Thekkini?","option_a":"Kitchen","option_b":"South block for reception","option_c":"Prayer room","option_d":"Bedroom","correct_option":"B","explanation":"Thekkini is the south-facing reception area."},
     {"question_text":"What science governs Nalukettu construction?","option_a":"Vastu Shastra","option_b":"Thachu Shastra","option_c":"Feng Shui","option_d":"Yoga Shastra","correct_option":"B","explanation":"Thachu Shastra is the carpentry science."},
     {"question_text":"What plant is in the Nadumuttam?","option_a":"Neem","option_b":"Tulsi (sacred basil)","option_c":"Bamboo","option_d":"Coconut","correct_option":"B","explanation":"Tulsi Thara is placed in the courtyard."}]
)

print("\n" + "="*60)
print("ALL 10 NEW TOPICS CREATED SUCCESSFULLY!")
print("="*60)
