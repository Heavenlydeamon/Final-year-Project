"""
Kerala Content Expansion - Part 3: 10 New Topics
Run: python seed_kerala_content_p3.py
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
print("PART 3: Creating 10 new Kerala topics")
print("="*60)

# 1. Backwaters of Kerala
seed_topic("Backwaters of Kerala", "environment", "Environment",
    "The intricate network of lagoons, lakes, and canals that define Kerala's identity as 'God's Own Country'.",
    [{"id":"network","label":"The Backwater Network"},{"id":"houseboats","label":"Kettuvallam Houseboats"},{"id":"ecology","label":"Backwater Ecology"},{"id":"communities","label":"Backwater Communities"},{"id":"tourism","label":"Tourism Impact"},{"id":"conservation","label":"Conservation Challenges"}],
    [{"title":"The Backwater Network","text":"Kerala's backwaters are a chain of 34 lagoons and 44 rivers linked by 1,500 km of canals. The system runs parallel to the Arabian Sea coast.\n\n**Major Backwater Lakes:**\n* Vembanad Lake (2,033 sq km) – Kerala's largest\n* Ashtamudi Lake – 'Gateway to Backwaters'\n* Sasthamkotta Lake – Kerala's largest freshwater lake\n* Paravur Lake in Kollam"},
     {"title":"Kettuvallam Houseboats","text":"Kettuvallam (literally 'tied boats') are traditional cargo boats converted into luxury houseboats.\n\n**Construction:**\n* Built entirely from anjili wood and bamboo\n* Bound using coir ropes – no nails used\n* Waterproofed with cashew nut shell oil\n* Originally used to transport rice and spices from Kuttanad to Kochi port"},
     {"title":"Backwater Ecology","text":"The backwaters host a unique brackish water ecosystem:\n* **Mangrove forests** along waterways\n* 150+ species of resident and migratory birds\n* Freshwater fish like karimeen (pearl spot) and konju (prawns)\n* The Kumarakom Bird Sanctuary is a Ramsar site\n\nThe salinity varies seasonally – monsoon brings freshwater, summer increases salt."},
     {"title":"Backwater Communities","text":"Traditional fishing and farming communities have lived along backwaters for centuries:\n* **Fishing (Matsya Thozhil)** using country boats and Chinese nets\n* **Coir making** from coconut husks soaked in backwaters\n* **Duck farming** – Thousands of ducks are herded across backwaters daily\n* **Toddy tapping** from coconut palms along the banks"},
     {"title":"Tourism Impact","text":"Backwater tourism is Kerala's biggest revenue generator:\n* Alappuzha ('Venice of the East') gets 1M+ tourists annually\n* Houseboat industry employs 10,000+ families\n* Kumarakom, Kollam, and Kochi are key houseboat hubs\n\nHowever, unregulated tourism has caused pollution and habitat destruction."},
     {"title":"Conservation Challenges","text":"The backwaters face critical threats:\n* **Pollution** from houseboat waste and domestic sewage\n* **Invasive species** like African Catfish and Water Hyacinth\n* **Land reclamation** reducing water area by 30% in 50 years\n* **Thanneermukkom Bund** disrupted natural water flow\n\nKerala Tourism's 'Responsible Tourism' initiative aims to address these."}],
    [{"question_text":"How many km of canals link Kerala's backwaters?","option_a":"500","option_b":"1000","option_c":"1500","option_d":"2000","correct_option":"C","explanation":"1,500 km of canals."},
     {"question_text":"What does Kettuvallam mean?","option_a":"Fishing boat","option_b":"Tied boat","option_c":"Speed boat","option_d":"Royal boat","correct_option":"B","explanation":"Literally 'tied boat'."},
     {"question_text":"What is karimeen?","option_a":"A bird","option_b":"Pearl spot fish","option_c":"A prawn","option_d":"A crab","correct_option":"B","explanation":"Karimeen is the pearl spot fish."},
     {"question_text":"Which city is called Venice of the East?","option_a":"Kochi","option_b":"Kollam","option_c":"Alappuzha","option_d":"Thrissur","correct_option":"C","explanation":"Alappuzha is called Venice of the East."},
     {"question_text":"What material waterproofs a Kettuvallam?","option_a":"Tar","option_b":"Cashew nut shell oil","option_c":"Coconut oil","option_d":"Resin","correct_option":"B","explanation":"Cashew nut shell oil waterproofs the boat."},
     {"question_text":"What is Sasthamkotta Lake known as?","option_a":"Largest backwater lake","option_b":"Largest freshwater lake in Kerala","option_c":"Deepest lake","option_d":"Oldest lake","correct_option":"B","explanation":"It's Kerala's largest freshwater lake."},
     {"question_text":"What invasive plant threatens backwaters?","option_a":"Lotus","option_b":"Water Hyacinth","option_c":"Bamboo","option_d":"Mangrove","correct_option":"B","explanation":"Water Hyacinth is an invasive species."},
     {"question_text":"What is the Kumarakom Bird Sanctuary designated as?","option_a":"National Park","option_b":"Ramsar site","option_c":"UNESCO site","option_d":"Tiger Reserve","correct_option":"B","explanation":"It is a Ramsar wetland site."}]
)

# 2. Onam Festival
seed_topic("Onam Festival", "festivals", "Cultural Artforms",
    "Kerala's grandest festival celebrating the annual homecoming of King Mahabali, marked by feasts, boat races, and cultural performances.",
    [{"id":"history","label":"History & Origins"},{"id":"rituals","label":"Rituals & Celebrations"},{"id":"sadya","label":"The Grand Onasadya"},{"id":"vallamkali","label":"Vallam Kali"},{"id":"arts","label":"Onam Arts & Games"},{"id":"unity","label":"Festival of Unity"}],
    [{"title":"History & Origins","text":"Onam falls in the Malayalam month of Chingam (Aug-Sep) and marks King Mahabali's annual visit. It is a 10-day festival, with Thiruvonam being the most important day.\n\n**The 10 Days:**\nAtham → Chithira → Chodhi → Vishakam → Anizham → Thriketa → Moolam → Pooradam → Uthradom → Thiruvonam"},
     {"title":"Rituals & Celebrations","text":"**Pookalam:** Elaborate flower carpets at every doorstep, growing larger each day.\n**Onathappan:** A clay pyramid representing Mahabali, placed at the center of the Pookalam.\n**Thumbi Thullal:** Traditional women's dance during Onam.\n**Kaikottikali/Thiruvathira:** Group dances performed in circles around a lamp."},
     {"title":"The Grand Onasadya","text":"The Onasadya is a 26-course vegetarian feast served on a banana leaf.\n\n**Key Dishes:**\n* Avial – Mixed vegetables in coconut\n* Olan – Pumpkin in coconut milk\n* Sambar – Lentil curry\n* Payasam – Dessert (Ada Pradhaman, Pal Payasam)\n* Parippu Curry – Lentil with ghee\n\nEating order follows strict tradition: rice in center, curries clockwise."},
     {"title":"Vallam Kali","text":"Snake boat races are Onam's most spectacular event. The Nehru Trophy Boat Race on Punnamada Lake features 100-foot Chundan Vallams (snake boats) with 100+ rowers each.\n\n**Famous Races:**\n* Nehru Trophy (Alappuzha)\n* Aranmula Uthrattathi (Pathanamthitta)\n* Champakulam Moolam (Oldest race, 400+ years)"},
     {"title":"Onam Arts & Games","text":"**Pulikali:** Men painted as tigers dance through Thrissur streets.\n**Kazhchakkula:** Giant banana bunches offered at temples.\n**Onakalikal:** Traditional games including:\n* Uriyadi (pot-breaking blindfolded)\n* Tug of war\n* Attakalam (wrestling)\n* Ambeyyal (archery)"},
     {"title":"Festival of Unity","text":"Onam transcends religion in Kerala. Hindus, Christians, and Muslims celebrate together, making it truly secular.\n\n* Schools and offices close for 4-5 days\n* Kerala government declares Onam a state festival\n* Gulf Malayalis organize massive Onam celebrations abroad\n* The festival contributes over ₹10,000 crore to Kerala's economy annually"}],
    [{"question_text":"How many days does Onam last?","option_a":"5","option_b":"7","option_c":"10","option_d":"15","correct_option":"C","explanation":"Onam is a 10-day festival."},
     {"question_text":"What is the most important day of Onam?","option_a":"Atham","option_b":"Moolam","option_c":"Thiruvonam","option_d":"Vishakam","correct_option":"C","explanation":"Thiruvonam is the main day."},
     {"question_text":"How many courses are in an Onasadya?","option_a":"16","option_b":"20","option_c":"26","option_d":"30","correct_option":"C","explanation":"Traditional Onasadya has 26 courses."},
     {"question_text":"What is Pulikali?","option_a":"Boat race","option_b":"Tiger dance","option_c":"Flower carpet","option_d":"Wrestling","correct_option":"B","explanation":"Men painted as tigers dance through streets."},
     {"question_text":"Which is the oldest boat race?","option_a":"Nehru Trophy","option_b":"Aranmula","option_c":"Champakulam Moolam","option_d":"President's Trophy","correct_option":"C","explanation":"Champakulam Moolam is over 400 years old."},
     {"question_text":"What is placed at the center of a Pookalam?","option_a":"A lamp","option_b":"Onathappan","option_c":"A flower","option_d":"A flag","correct_option":"B","explanation":"Onathappan is a clay pyramid representing Mahabali."},
     {"question_text":"In which Malayalam month does Onam fall?","option_a":"Medam","option_b":"Chingam","option_c":"Karkidakam","option_d":"Thulam","correct_option":"B","explanation":"Onam falls in Chingam (Aug-Sep)."},
     {"question_text":"What is Ada Pradhaman?","option_a":"A curry","option_b":"A rice dish","option_c":"A dessert/payasam","option_d":"A pickle","correct_option":"C","explanation":"Ada Pradhaman is a traditional Onam dessert."}]
)

# 3. Vishu
seed_topic("Vishu - Kerala New Year", "festivals", "Cultural Artforms",
    "Vishu marks the Malayalam New Year and the spring equinox, celebrated with the sacred Vishukkani, fireworks, and new clothes.",
    [{"id":"significance","label":"Astronomical Significance"},{"id":"vishukkani","label":"The Sacred Vishukkani"},{"id":"rituals","label":"Rituals & Traditions"},{"id":"cuisine","label":"Vishu Cuisine"},{"id":"regional","label":"Regional Variations"},{"id":"modern","label":"Modern Celebrations"}],
    [{"title":"Astronomical Significance","text":"Vishu falls on the 1st of Medam (April 14-15), marking the sun's transit into Mesha Rashi (Aries). It coincides with the spring equinox.\n\n**Shared Across India:**\n* Baisakhi (Punjab)\n* Puthandu (Tamil Nadu)\n* Ugadi (Karnataka/Andhra)\n* Bihu (Assam)\n\nAll celebrate the agricultural new year."},
     {"title":"The Sacred Vishukkani","text":"Vishukkani ('the first sight') is the most important ritual. A brass vessel (Uruli) is arranged the night before with:\n* **Kani Konna flowers** (golden shower – Vishu's signature flower)\n* **Rice** in a measuring vessel\n* **Coconut** (halved)\n* **Betel leaves and areca nuts**\n* **Gold ornaments and coins**\n* **Mirror** to reflect abundance\n* **Holy text** (usually Ramayana)\n* **Lit brass lamp** (Nilavilakku)\n\nThe first thing you see on Vishu morning must be the Vishukkani."},
     {"title":"Rituals & Traditions","text":"**Vishukaineetam:** Elders give money (coins/notes) to children and younger family members as blessings for the new year.\n\n**Vishuppada:** Fireworks and crackers at dawn – the 'Vishu sound'.\n\n**Temple visits:** Devotees visit Guruvayur, Sabarimala, and local temples.\n\n**New clothes (Puthukodi):** Everyone wears new clothes on Vishu."},
     {"title":"Vishu Cuisine","text":"The Vishu Sadya balances all six tastes (sweet, sour, salty, bitter, pungent, astringent):\n\n* **Veppampoorasam** – Bitter neem flowers mixed with jaggery (symbolizing life's mix of bitter and sweet)\n* **Vishu Kanji** – Rice porridge with coconut milk\n* **Thoran** – Stir-fried vegetables with coconut\n* **Mampazhapachadi** – Raw mango curry (sweet and sour)\n* **Vishu special payasam**"},
     {"title":"Regional Variations","text":"* **Thrissur:** Grand temple celebrations at Vadakkunnathan\n* **Palakkad:** Agricultural rituals with the first ploughing\n* **Malabar:** Kani Konna decorations on homes\n* **Syrian Christians** also celebrate Vishu, reflecting Kerala's syncretic culture\n* **Kerala diaspora** celebrates with community gatherings worldwide"},
     {"title":"Modern Celebrations","text":"Today Vishu combines tradition with modernity:\n* TV channels broadcast special Vishu programs\n* Social media Vishukkani sharing has become a trend\n* Shopping festivals and sales mark the season\n* Schools organize Vishu celebrations with Pookalam and Sadya\n* The Kerala government issues Vishu bonus to employees"}],
    [{"question_text":"When does Vishu fall?","option_a":"January 1","option_b":"March 21","option_c":"April 14-15","option_d":"August 15","correct_option":"C","explanation":"Vishu falls on the 1st of Medam (April 14-15)."},
     {"question_text":"What is Vishukkani?","option_a":"A dance","option_b":"The sacred first sight on Vishu morning","option_c":"A feast","option_d":"Fireworks","correct_option":"B","explanation":"Vishukkani is the first auspicious sight."},
     {"question_text":"What flower is associated with Vishu?","option_a":"Lotus","option_b":"Jasmine","option_c":"Kani Konna (golden shower)","option_d":"Rose","correct_option":"C","explanation":"Kani Konna is Vishu's signature flower."},
     {"question_text":"What is Vishukaineetam?","option_a":"Temple visit","option_b":"Money given by elders","option_c":"New clothes","option_d":"Fireworks","correct_option":"B","explanation":"Elders give money as blessings."},
     {"question_text":"What does Veppampoorasam symbolize?","option_a":"Sweetness of life","option_b":"Life's mix of bitter and sweet","option_c":"Prosperity","option_d":"Victory","correct_option":"B","explanation":"Neem with jaggery symbolizes life's contrast."},
     {"question_text":"What astronomical event does Vishu mark?","option_a":"Winter solstice","option_b":"Spring equinox","option_c":"Lunar eclipse","option_d":"Summer solstice","correct_option":"B","explanation":"Vishu coincides with the spring equinox."},
     {"question_text":"What is Vishuppada?","option_a":"A prayer","option_b":"A feast","option_c":"Fireworks at dawn","option_d":"A dance","correct_option":"C","explanation":"Vishuppada refers to dawn fireworks."},
     {"question_text":"What is Puthukodi?","option_a":"Old clothes","option_b":"New clothes for Vishu","option_c":"A fruit","option_d":"A ritual","correct_option":"B","explanation":"Everyone wears new clothes on Vishu."}]
)

print("\n3 of 10 new topics created. Continuing...")
