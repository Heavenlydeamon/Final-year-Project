from django.core.management.base import BaseCommand
from mainapp.models import Section, Topic, StudyMaterial, Question, Choice, Institution

class Command(BaseCommand):
    help = 'Add sample data for sections, topics, study materials, questions, and choices'

    def handle(self, *args, **options):
        # ========================================
        # KERALA INSTITUTIONS
        # ========================================
        
        # Universities
        universities = [
            ('University of Kerala', 'State university located in Thiruvananthapuram, established in 1937'),
            ('Mahatma Gandhi University', 'State university located in Kottayam, established in 1983'),
            ('University of Calicut', 'State university located in Malappuram, established in 1968'),
            ('Cochin University of Science and Technology (CUSAT)', 'Public university in Kochi focused on science and technology'),
            ('Kannur University', 'State university located in Kannur, established in 1996'),
            ('Sree Sankaracharya University of Sanskrit', 'University in Kalady focused on Sanskrit studies'),
            ('Thunchath Ezhuthachan Malayalam University', 'University in Tirur dedicated to Malayalam language and literature'),
            ('Kerala Agricultural University', 'Agricultural university in Thrissur'),
            ('Kerala University of Health Sciences', 'Health sciences university in Thrissur'),
            ('Kerala University of Fisheries and Ocean Studies', 'Fisheries university in Kochi'),
            ('National University of Advanced Legal Studies (NUALS)', 'Law university in Kochi'),
            ('Indian Institute of Space Science and Technology (IIST)', 'Premier space science institute in Thiruvananthapuram'),
        ]
        
        # Engineering Colleges
        engineering_colleges = [
            ('National Institute of Technology Calicut (NITC)', 'Premier engineering institute in Kozhikode'),
            ('College of Engineering Trivandrum (CET)', 'Government engineering college in Thiruvananthapuram'),
            ('Government Engineering College Thrissur', 'Government engineering college in Thrissur'),
            ('Government Engineering College Kozhikode', 'Government engineering college in Kozhikode'),
            ('Government Engineering College Sreekrishnapuram', 'Government engineering college in Palakkad'),
            ('Government Engineering College Wayanad', 'Government engineering college in Wayanad'),
            ('Government Engineering College Idukki', 'Government engineering college in Idukki'),
            ('Government Engineering College Kannur', 'Government engineering college in Kannur'),
            ('Government Engineering College Kottayam', 'Government engineering college in Kottayam'),
            ('Rajiv Gandhi Institute of Technology (RIT)', 'Government engineering college in Kottayam'),
            ('Model Engineering College (MEC)', 'Government engineering college in Kochi'),
            ('T.K.M. College of Engineering', 'Private engineering college in Kollam'),
            ('Mar Athanasius College of Engineering', 'Private engineering college in Kothamangalam'),
            ('Saintgits College of Engineering', 'Private engineering college in Kottayam'),
            ('Muthoot Institute of Technology and Science', 'Private engineering college in Ernakulam'),
            ('Federal Institute of Science and Technology (FISAT)', 'Private engineering college in Ernakulam'),
            ('Adi Shankara Institute of Engineering and Technology', 'Private engineering college in Kalady'),
            ('Viswajyothi College of Engineering and Technology', 'Private engineering college in Ernakulam'),
            ('Jyothi Engineering College', 'Private engineering college in Thrissur'),
            ('Sree Chitra Thirunal College of Engineering', 'Government engineering college in Thiruvananthapuram'),
        ]
        
        # Medical Colleges
        medical_colleges = [
            ('Government Medical College Thiruvananthapuram', 'Premier government medical college in Kerala'),
            ('Government Medical College Kozhikode', 'Government medical college in Kozhikode'),
            ('Government Medical College Thrissur', 'Government medical college in Thrissur'),
            ('Government Medical College Kottayam', 'Government medical college in Kottayam'),
            ('Government Medical College Alappuzha', 'Government medical college in Alappuzha'),
            ('Government Medical College Ernakulam', 'Government medical college in Ernakulam'),
            ('Government Medical College Kollam', 'Government medical college in Kollam'),
            ('Government Medical College Palakkad', 'Government medical college in Palakkad'),
            ('Government Medical College Idukki', 'Government medical college in Idukki'),
            ('Government Medical College Kannur', 'Government medical college in Kannur'),
            ('Government Medical College Kasaragod', 'Government medical college in Kasaragod'),
            ('Government Medical College Malappuram', 'Government medical college in Malappuram'),
            ('Government Medical College Pathanamthitta', 'Government medical college in Pathanamthitta'),
            ('Government Medical College Wayanad', 'Government medical college in Wayanad'),
            ('Amrita Institute of Medical Sciences', 'Private medical college in Kochi'),
            ('Jubilee Mission Medical College', 'Private medical college in Thrissur'),
            ('Pushpagiri Institute of Medical Sciences', 'Private medical college in Thiruvalla'),
            ('Believers Church Medical College', 'Private medical college in Thiruvalla'),
            ('Sree Narayana Institute of Medical Sciences', 'Private medical college in Ernakulam'),
            ('Dr. Somervell Memorial CSI Medical College', 'Private medical college in Karakonam'),
        ]
        
        # Arts & Science Colleges
        arts_science_colleges = [
            ('Government College for Women Thiruvananthapuram', 'Premier women college in Thiruvananthapuram'),
            ('Government Arts College Thiruvananthapuram', 'Government arts college in Thiruvananthapuram'),
            ('University College Thiruvananthapuram', 'One of the oldest colleges in Kerala'),
            ('Maharajas College Ernakulam', 'Government college in Kochi'),
            ('Sacred Heart College Thevara', 'Autonomous college in Kochi'),
            ('St. Alberts College Ernakulam', 'College in Kochi'),
            ('St. Teresas College Ernakulam', 'Women college in Kochi'),
            ('Bharata Mata College Thrikkakara', 'College in Ernakulam'),
            ('Christ College Irinjalakuda', 'Autonomous college in Thrissur'),
            ('St. Thomas College Thrissur', 'College in Thrissur'),
            ('Sree Kerala Varma College Thrissur', 'Government college in Thrissur'),
            ('Government Victoria College Palakkad', 'Government college in Palakkad'),
            ('St. Josephs College Devagiri', 'Autonomous college in Kozhikode'),
            ('Farook College Kozhikode', 'Government college in Kozhikode'),
            ('Government College Kasaragod', 'Government college in Kasaragod'),
            ('Nirmalagiri College Koothuparamba', 'College in Kannur'),
            ('Payyanur College Payyanur', 'College in Kannur'),
            ('Government College Malappuram', 'Government college in Malappuram'),
            ('M.E.S. College Marampally', 'College in Ernakulam'),
            ('St. Xaviers College Thumba', 'College in Thiruvananthapuram'),
            ('All Saints College Thiruvananthapuram', 'Women college in Thiruvananthapuram'),
            ('Kuriakose Gregorios College Pampady', 'College in Kottayam'),
            ('St. Michaels College Cherthala', 'College in Alappuzha'),
            ('N.S.S. College Pandalam', 'College in Pathanamthitta'),
            ('Catholicate College Pathanamthitta', 'College in Pathanamthitta'),
            ('Alphonsa College Pala', 'Women college in Kottayam'),
            ('St. Thomas College Pala', 'College in Kottayam'),
            ('Assumption College Changanassery', 'Autonomous women college in Kottayam'),
            ('St. Berchmans College Changanassery', 'College in Kottayam'),
            ('K.G. College Pampady', 'College in Kottayam'),
            ('M.G. College Trivandrum', 'College in Thiruvananthapuram'),
        ]
        
        # Major Schools
        schools = [
            ('Kendriya Vidyalaya Pattom', 'Central school in Thiruvananthapuram'),
            ('Kendriya Vidyalaya Ernakulam', 'Central school in Kochi'),
            ('Kendriya Vidyalaya Calicut', 'Central school in Kozhikode'),
            ('Kendriya Vidyalaya Thrissur', 'Central school in Thrissur'),
            ('Kendriya Vidyalaya Kottayam', 'Central school in Kottayam'),
            ('Kendriya Vidyalaya Palakkad', 'Central school in Palakkad'),
            ('Kendriya Vidyalaya Kannur', 'Central school in Kannur'),
            ('Kendriya Vidyalaya Kasaragod', 'Central school in Kasaragod'),
            ('Kendriya Vidyalaya Alappuzha', 'Central school in Alappuzha'),
            ('Kendriya Vidyalaya Kollam', 'Central school in Kollam'),
            ('Kendriya Vidyalaya Malappuram', 'Central school in Malappuram'),
            ('Kendriya Vidyalaya Pathanamthitta', 'Central school in Pathanamthitta'),
            ('Kendriya Vidyalaya Wayanad', 'Central school in Wayanad'),
            ('Kendriya Vidyalaya Idukki', 'Central school in Idukki'),
            ('Saraswathi Vidyalaya Thiruvananthapuram', 'Private school in Thiruvananthapuram'),
            ('Christ Nagar School Thiruvananthapuram', 'Private school in Thiruvananthapuram'),
            ('Loyola School Thiruvananthapuram', 'Private school in Thiruvananthapuram'),
            ('Sree Chithira Thirunal School Thiruvananthapuram', 'Government school in Thiruvananthapuram'),
            ('Chinmaya Vidyalaya Kochi', 'Private school in Kochi'),
            ('Rajagiri Public School Kochi', 'Private school in Kochi'),
            ('Bhavans Vidya Mandir Kochi', 'Private school in Kochi'),
            ('Assisi Vidyaniketan Public School Kochi', 'Private school in Kochi'),
            ('The Choice School Kochi', 'Private school in Kochi'),
            ('Sacred Heart CMI Public School Kochi', 'Private school in Kochi'),
            ('St. Josephs Higher Secondary School Kozhikode', 'Private school in Kozhikode'),
            ('Malabar Christian College Higher Secondary School Kozhikode', 'School in Kozhikode'),
            ('Devagiri CMI Public School Kozhikode', 'Private school in Kozhikode'),
            ('Basel Evangelical Mission Higher Secondary School Kozhikode', 'School in Kozhikode'),
            ('St. Thomas Convent School Thrissur', 'Private school in Thrissur'),
            ('Vimala College Higher Secondary School Thrissur', 'School in Thrissur'),
            ('Sree Kerala Varma Higher Secondary School Thrissur', 'School in Thrissur'),
            ('St. Josephs Boys Higher Secondary School Kozhikode', 'School in Kozhikode'),
            ('St. Josephs Girls Higher Secondary School Kozhikode', 'School in Kozhikode'),
            ('St. Marys Convent Girls Higher Secondary School Thrissur', 'School in Thrissur'),
            ('St. Antonyss Higher Secondary School Kottayam', 'School in Kottayam'),
            ('St. Thomas Higher Secondary School Kottayam', 'School in Kottayam'),
            ('Alphonsa Higher Secondary School Kottayam', 'School in Kottayam'),
            ('St. Marys Higher Secondary School Kottayam', 'School in Kottayam'),
            ('St. Josephs Higher Secondary School Alappuzha', 'School in Alappuzha'),
            ('Leo XIII Higher Secondary School Alappuzha', 'School in Alappuzha'),
            ('St. Michaels Higher Secondary School Alappuzha', 'School in Alappuzha'),
            ('St. Gregorios Higher Secondary School Kollam', 'School in Kollam'),
            ('St. Aloysius Higher Secondary School Kollam', 'School in Kollam'),
            ('Infant Jesus Higher Secondary School Kollam', 'School in Kollam'),
            ('St. Josephs Higher Secondary School Palakkad', 'School in Palakkad'),
            ('Victoria College Higher Secondary School Palakkad', 'School in Palakkad'),
            ('Government Higher Secondary School Palakkad', 'School in Palakkad'),
            ('St. Marys Higher Secondary School Kannur', 'School in Kannur'),
            ('St. Josephs Higher Secondary School Kannur', 'School in Kannur'),
            ('Government Higher Secondary School Kannur', 'School in Kannur'),
            ('St. Marys Higher Secondary School Kasaragod', 'School in Kasaragod'),
            ('St. Aloysius Higher Secondary School Kasaragod', 'School in Kasaragod'),
            ('Government Higher Secondary School Kasaragod', 'School in Kasaragod'),
            ('St. Marys Higher Secondary School Malappuram', 'School in Malappuram'),
            ('St. Josephs Higher Secondary School Malappuram', 'School in Malappuram'),
            ('Government Higher Secondary School Malappuram', 'School in Malappuram'),
            ('St. Marys Higher Secondary School Wayanad', 'School in Wayanad'),
            ('St. Josephs Higher Secondary School Wayanad', 'School in Wayanad'),
            ('Government Higher Secondary School Wayanad', 'School in Wayanad'),
            ('St. Marys Higher Secondary School Idukki', 'School in Idukki'),
            ('St. Josephs Higher Secondary School Idukki', 'School in Idukki'),
            ('Government Higher Secondary School Idukki', 'School in Idukki'),
            ('St. Marys Higher Secondary School Pathanamthitta', 'School in Pathanamthitta'),
            ('St. Josephs Higher Secondary School Pathanamthitta', 'School in Pathanamthitta'),
            ('Government Higher Secondary School Pathanamthitta', 'School in Pathanamthitta'),
        ]
        
        # Polytechnics and ITIs
        polytechnics = [
            ('Government Polytechnic College Kalamassery', 'Government polytechnic in Ernakulam'),
            ('Government Polytechnic College Kozhikode', 'Government polytechnic in Kozhikode'),
            ('Government Polytechnic College Thiruvananthapuram', 'Government polytechnic in Thiruvananthapuram'),
            ('Government Polytechnic College Thrissur', 'Government polytechnic in Thrissur'),
            ('Government Polytechnic College Kottayam', 'Government polytechnic in Kottayam'),
            ('Government Polytechnic College Palakkad', 'Government polytechnic in Palakkad'),
            ('Government Polytechnic College Malappuram', 'Government polytechnic in Malappuram'),
            ('Government Polytechnic College Kannur', 'Government polytechnic in Kannur'),
            ('Government Polytechnic College Kasaragod', 'Government polytechnic in Kasaragod'),
            ('Government Polytechnic College Wayanad', 'Government polytechnic in Wayanad'),
            ('Government Polytechnic College Idukki', 'Government polytechnic in Idukki'),
            ('Government Polytechnic College Pathanamthitta', 'Government polytechnic in Pathanamthitta'),
            ('Government Polytechnic College Alappuzha', 'Government polytechnic in Alappuzha'),
            ('Government Polytechnic College Kollam', 'Government polytechnic in Kollam'),
            ('Sree Narayana Polytechnic College Kottayam', 'Private polytechnic in Kottayam'),
            ('Model Polytechnic College Vadakara', 'Government polytechnic in Kozhikode'),
            ('Model Polytechnic College Kunnamkulam', 'Government polytechnic in Thrissur'),
            ('Model Polytechnic College Painavu', 'Government polytechnic in Idukki'),
            ('Government ITI Kalamassery', 'Government ITI in Ernakulam'),
            ('Government ITI Kozhikode', 'Government ITI in Kozhikode'),
            ('Government ITI Thiruvananthapuram', 'Government ITI in Thiruvananthapuram'),
            ('Government ITI Thrissur', 'Government ITI in Thrissur'),
            ('Government ITI Kottayam', 'Government ITI in Kottayam'),
            ('Government ITI Palakkad', 'Government ITI in Palakkad'),
            ('Government ITI Malappuram', 'Government ITI in Malappuram'),
            ('Government ITI Kannur', 'Government ITI in Kannur'),
            ('Government ITI Kasaragod', 'Government ITI in Kasaragod'),
            ('Government ITI Wayanad', 'Government ITI in Wayanad'),
            ('Government ITI Idukki', 'Government ITI in Idukki'),
            ('Government ITI Pathanamthitta', 'Government ITI in Pathanamthitta'),
            ('Government ITI Alappuzha', 'Government ITI in Alappuzha'),
            ('Government ITI Kollam', 'Government ITI in Kollam'),
        ]
        
        # Other Institutions
        other_institutions = [
            ('Indian Institute of Management Kozhikode (IIMK)', 'Premier management institute in Kozhikode'),
            ('Kerala Institute of Local Administration (KILA)', 'Training institute for local government in Thrissur'),
            ('State Institute of Languages Kerala', 'Language institute in Thiruvananthapuram'),
            ('Kerala State Science and Technology Museum', 'Science museum in Thiruvananthapuram'),
            ('Regional Cancer Centre Thiruvananthapuram', 'Cancer research and treatment center'),
            ('Sree Chitra Tirunal Institute for Medical Sciences', 'Medical research institute in Thiruvananthapuram'),
            ('Centre for Development of Imaging Technology (C-DIT)', 'Technology center in Thiruvananthapuram'),
            ('Keltron Knowledge Center', 'Electronics training center'),
            ('Kerala State IT Mission', 'IT training and development center'),
            ('Kerala Academy for Skills Excellence (KASE)', 'Skill development academy'),
            ('Institute of Management in Government (IMG)', 'Management training institute'),
            ('Kerala Institute of Tourism and Travel Studies (KITTS)', 'Tourism training institute'),
            ('Kerala State Biodiversity Board', 'Biodiversity research and education center'),
            ('M.S. Swaminathan Research Foundation', 'Agricultural research foundation'),
            ('Centre for Water Resources Development and Management', 'Water resources research center'),
            ('National Institute of Speech and Hearing (NISH)', 'Speech and hearing institute in Thiruvananthapuram'),
            ('Indian Institute of Information Technology and Management Kerala (IIITM-K)', 'IT and management institute in Thiruvananthapuram'),
            ('Kerala Forest Research Institute (KFRI)', 'Forest research institute in Thrissur'),
            ('Jawaharlal Nehru Tropical Botanic Garden and Research Institute', 'Botanic research institute in Thiruvananthapuram'),
            ('Centre for Marine Living Resources and Ecology (CMLRE)', 'Marine research center in Kochi'),
        ]
        
        # Combine all institutions
        all_institutions = (
            universities + 
            engineering_colleges + 
            medical_colleges + 
            arts_science_colleges + 
            schools + 
            polytechnics + 
            other_institutions
        )
        
        # Create institutions
        institution_count = 0
        for name, description in all_institutions:
            _, created = Institution.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                institution_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'{institution_count} Kerala institutions added successfully'))
        
        # Create sections

        env_section, _ = Section.objects.get_or_create(
            name='Environment',
            defaults={
                'description': 'Learn about the environment, climate change, and conservation.',
                'image_url': 'https://example.com/environment.jpg',
                'video_url': 'https://example.com/environment.mp4'
            }
        )
        heritage_section, _ = Section.objects.get_or_create(
            name='Heritage Sites',
            defaults={
                'description': 'Explore historical heritage sites and their significance.',
                'image_url': 'https://example.com/heritage.jpg',
                'video_url': 'https://example.com/heritage.mp4'
            }
        )
        cultural_section, _ = Section.objects.get_or_create(
            name='Cultural Artforms',
            defaults={
                'description': 'Discover cultural artforms and traditions.',
                'image_url': 'https://example.com/cultural.jpg',
                'video_url': 'https://example.com/cultural.mp4'
            }
        )

        # ========================================
        # WESTERN GHATS - MODULE 1: Physical Geography
        # ========================================
        western_ghats, _ = Topic.objects.get_or_create(
            name='Western Ghats',
            section=env_section,
            defaults={
                'description': 'Explore the biodiversity hotspot of the Western Ghats mountain range.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Kodagu_landscape.jpg/1200px-Kodagu_landscape.jpg',
                'order': 1
            }
        )
        
        # Western Ghats Module 1: Physical Geography
        StudyMaterial.objects.get_or_create(
            topic=western_ghats,
            title='Module 1: The Great Escarpment of India',
            defaults={
                'content_text': '''The Great Escarpment of India

The Western Ghats, also known as the **Sahyadri**, is a mountain range that covers an area of 160,000 km² in a stretch of 1,600 km parallel to the western coast of the Indian peninsula.

Formation

Unlike the Himalayas, the Western Ghats are not "true" mountains. They are the **faulted edge of the Deccan Plateau**, formed during the break-up of the supercontinent **Gondwana** approximately 150 million years ago. This makes them one of the oldest mountain ranges in the world.

 Geographic Extent

The Western Ghats stretches from the **Tapi River in Gujarat** to **Kanyakumari in Tamil Nadu**, running through the states of:
- Gujarat
- Maharashtra
- Goa
- Karnataka
- Kerala
- Tamil Nadu

 Highest Peak

**Anamudi** (2,695 m) in Kerala is the highest peak in India south of the Himalayas. It is often called the **"Everest of South India"** and is located in the Anamalai hills of Kerala.

 Climate Regulator

The Western Ghats act as a **key barrier to the moisture-laden southwest monsoon winds**. This geographical feature causes:
- Heavy rainfall on the western slopes
- Creates the lush rainforests Kerala is known for
- Results in a rain shadow effect on the eastern side

The mountains intercept the monsoon clouds, resulting in annual rainfall ranging from 2,000 mm to 7,000 mm on the windward side, making this region one of the wettest places on Earth.''',
                'image_url': 'ghats.jpg',
                'order': 1
            }
        )
        
        # Western Ghats Module 2: Flora and Fauna
        StudyMaterial.objects.get_or_create(
            topic=western_ghats,
            title='Module 2: A Global Biodiversity Hotspot',
            defaults={
                'content_text': '''A Global Biodiversity Hotspot

The Western Ghats is recognized as one of the **eight hottest biodiversity hotspots** in the world. It is home to over **7,000 species of flowering plants** and hundreds of animal species, many of which are found nowhere else on Earth.

## Endemic Species

The region has an incredibly high rate of **endemism** - species found only here and nowhere else:
- Over 1,500 species of endemic flowering plants
- Over 150 species of endemic reptiles
- Over 100 species of endemic amphibians

 Flagship Species

 Nilgiri Tahr
An endangered mountain goat found in the high-altitude grasslands of **Eravikulam National Park**. The Nilgiri Tahr is the state animal of Tamil Nadu and Kerala.

 Lion-tailed Macaque
One of the **rarest primates in the world**, recognizable by its silver-white mane. These primates live exclusively in the rainforests of the Western Ghats.

 Malabar Giant Squirrel
A colorful canopy-dwelling rodent found in the forests of the Western Ghats. It is one of the largest squirrel species in the world.

 Neelakurinji
A unique shrub found in the Shola forests that blooms only once every **12 years**, turning the hillsides purple. The last major bloom was in 2018.

## Wildlife Corridors

The Western Ghats serves as an important wildlife corridor connecting various national parks and wildlife sanctuaries, allowing for the movement of elephants, tigers, and other large mammals.''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Queen_s_Danaine_Butterfly.jpg/800px-Queen_s_Danaine_Butterfly.jpg',
                'order': 2
            }
        )
        
        # Western Ghats Module 3: Hydrology
        StudyMaterial.objects.get_or_create(
            topic=western_ghats,
            title='Module 3: The Water Tower of South India',
            defaults={
                'content_text': '''The Water Tower of South India

The Western Ghats are essentially the **"Water Tower"** for peninsular India. They feed a complex network of river systems that sustain millions of people and thousands of hectares of farmland.

 Major River Origins

 Rivers in Kerala
- **Periyar**: The longest river in Kerala, originating from the Western Ghats
- **Bharatapuzha**: Also known as River of Heaven, major river in Kerala
- **Pamba River**: Flows through the heart of Kerala, originating from the Ghats

 Interstate Rivers
- **Godavari**: Originates from the Western Ghats in Maharashtra, flows across central India
- **Krishna**: Another major river originating from the Ghats, flowing through Maharashtra, Karnataka, and Andhra Pradesh
- **Kaveri**: Known as the Ganga of the South, originates from Karnataka and flows through Tamil Nadu

 Ecosystem Services

Beyond water supply, the forests of the Western Ghats provide:

 Carbon Sequestration
The forests act as **massive carbon sinks**, helping mitigate the effects of global warming in the Indian subcontinent. The dense vegetation absorbs significant amounts of carbon dioxide.

 Soil Conservation
The steep slopes and dense vegetation prevent soil erosion and landslides.

 Groundwater Recharge
The forests help recharge groundwater aquifers that feed springs and wells in the surrounding plains.

 Biodiversity Habitat
The rivers originating from the Ghats support diverse aquatic ecosystems and fish species.

 Importance for South India

Over **500 million people** depend on the rivers originating from the Western Ghats for their water needs, making this region crucial for the ecological and economic well-being of South India.''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Periyar_River.jpg/1200px-Periyar_River.jpg',
                'order': 3
            }
        )
        
        # Western Ghats Module 4: Threats and Conservation
        StudyMaterial.objects.get_or_create(
            topic=western_ghats,
            title='Module 4: Threats and Conservation',
            defaults={
                'content_text': '''Preserving the Sahyadri

Despite their **UNESCO World Heritage status** (inscribed in 2012), the Western Ghats face severe environmental pressures that threaten its unique ecosystems.

 Key Threats

 1. Deforestation
- Conversion of forest land into **tea, coffee, and rubber plantations**
- Illegal logging for timber and firewood
- Expansion of agricultural activities in forest areas

 2. Mining
- **Iron and manganese ore mining** has caused massive soil erosion in some regions
- Mining activities in Goa, Karnataka, and Maharashtra have devastated large forest areas
- Illegal sand mining along river beds

 3. Climate Change
- Erratic rainfall patterns leading to landslides and floods
- As seen in the **2018 Kerala floods** that caused massive destruction
- Changing temperature patterns affecting endemic species
- Shifting of vegetation zones up the mountains

 4. Infrastructure Development
- Highway expansion through forest areas
- Dam construction disrupting natural water flow
- Urbanization in hill stations

 Conservation Reports

 Gadgil Report (2011)
Led by ecologist Madhav Gadgil, this report recommended:
- Classification of the entire Western Ghats as an Ecologically Sensitive Area (ESA)
- Strict regulations on development activities
- Community-based forest management

 Kasturirangan Report (2013)
Led by environmentalist Sri K. Kasturirangan, this report was more moderate:
- Suggested covering about 37% of the Western Ghats as ESA
- Focused on balancing development with conservation
- Called for sustainable development practices

 Conservation Efforts

- **Project Elephant** and **Project Tiger** continue to protect wildlife
- Several national parks and wildlife sanctuaries
- Community-based conservation initiatives
- Research and monitoring programs

The survival of the Western Ghats depends on balancing human development needs with environmental conservation.''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
                'order': 4
            }
        )

        # ========================================
        # CLIMATE CHANGE - EXPANDED TOPICS
        # ========================================
        climate_change, _ = Topic.objects.get_or_create(
            name='Climate Change',
            section=env_section,
            defaults={
                'description': 'Learn about the causes and effects of climate change on our planet.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Carbon_dioxide_levels.svg/1200px-Carbon_dioxide_levels.svg.png',
                'order': 2
            }
        )
        
        # Climate Change Module 1: Understanding Climate Change
        StudyMaterial.objects.get_or_create(
            topic=climate_change,
            title='Module 1: Understanding Climate Change',
            defaults={
                'content_text': '''Understanding Climate Change

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

## The Greenhouse Effect

The greenhouse effect is a natural process that warms the Earth's surface. When sunlight reaches Earth, some is reflected back to space, and some is absorbed and re-radiated as heat. Greenhouse gases in the atmosphere trap some of this heat, keeping the Earth warm enough to support life.

However, human activities have increased greenhouse gas concentrations, intensifying the natural greenhouse effect and causing global warming.

## Evidence of Climate Change

1. **Rising temperatures** - Each decade since 1980 has been warmer than the preceding one
2. **Melting ice caps** - Arctic sea ice is declining
3. **Sea level rise** - Oceans are expanding as they warm
4. **Changing precipitation** - Some areas getting wetter, others drier
5. **Ocean acidification** - CO2 dissolving in oceans making them more acidic''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Carbon_dioxide_levels.svg/1200px-Carbon_dioxide_levels.svg.png',
                'order': 1
            }
        )
        
        # Climate Change Module 2: Impact and Mitigation
        StudyMaterial.objects.get_or_create(
            topic=climate_change,
            title='Module 2: Impact and Mitigation',
            defaults={
                'content_text': '''Impact and Mitigation

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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Climate_change_impact.jpg/1200px-Climate_change_impact.jpg',
                'order': 2
            }
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
        
        # Wildlife Protection Module 1: Wildlife Conservation in India
        StudyMaterial.objects.get_or_create(
            topic=wildlife_protection,
            title='Module 1: Wildlife Conservation in India',
            defaults={
                'content_text': '''Wildlife Conservation in India

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
- **Marine Turtle''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tiger_in_Ranthambore.jpg/1200px-Tiger_in_Ranthambore.jpg',
                'order': 1
            }
        )
        
        # Wildlife Protection Module 2: Endangered Species
        StudyMaterial.objects.get_or_create(
            topic=wildlife_protection,
            title='Module 2: Endangered Species',
            defaults={
                'content_text': '''Endangered Species

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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Asiatic_Lion.jpg/1200px-Asiatic_Lion.jpg',
                'order': 2
            }
        )

        # Create questions for Western Ghats topic
        if not Question.objects.filter(topic=western_ghats).exists():
            q1 = Question.objects.create(section=env_section, topic=western_ghats, question_text='What is the Western Ghats also known as?', difficulty='easy')
            Choice.objects.create(question=q1, choice_text='Sahyadri', is_correct=True)
            Choice.objects.create(question=q1, choice_text='Vindhyas', is_correct=False)
            Choice.objects.create(question=q1, choice_text='Aravallis', is_correct=False)
            Choice.objects.create(question=q1, choice_text='Himalayas', is_correct=False)

            q2 = Question.objects.create(section=env_section, topic=western_ghats, question_text='How long is the Western Ghats mountain range?', difficulty='medium')
            Choice.objects.create(question=q2, choice_text='About 1,600 km', is_correct=True)
            Choice.objects.create(question=q2, choice_text='About 500 km', is_correct=False)
            Choice.objects.create(question=q2, choice_text='About 3,000 km', is_correct=False)
            Choice.objects.create(question=q2, choice_text='About 800 km', is_correct=False)

            q3 = Question.objects.create(section=env_section, topic=western_ghats, question_text='What is the highest peak in the Western Ghats?', difficulty='medium')
            Choice.objects.create(question=q3, choice_text='Anamudi', is_correct=True)
            Choice.objects.create(question=q3, choice_text='Kudremukh', is_correct=False)
            Choice.objects.create(question=q3, choice_text='Doddabetta', is_correct=False)
            Choice.objects.create(question=q3, choice_text='Mullayanagiri', is_correct=False)

            q4 = Question.objects.create(section=env_section, topic=western_ghats, question_text='Why is the Western Ghats a biodiversity hotspot?', difficulty='medium')
            Choice.objects.create(question=q4, choice_text='It has many endemic species', is_correct=True)
            Choice.objects.create(question=q4, choice_text='It has very few species', is_correct=False)
            Choice.objects.create(question=q4, choice_text='It is a desert region', is_correct=False)
            Choice.objects.create(question=q4, choice_text='It has no forests', is_correct=False)

            q5 = Question.objects.create(section=env_section, topic=western_ghats, question_text='Which animal is known as the "Everest of South India"?', difficulty='easy')
            Choice.objects.create(question=q5, choice_text='Anamudi peak', is_correct=True)
            Choice.objects.create(question=q5, choice_text='Mullayanagiri', is_correct=False)
            Choice.objects.create(question=q5, choice_text='Kudremukh', is_correct=False)
            Choice.objects.create(question=q5, choice_text='Brahmagiri', is_correct=False)

        # Create questions for Climate Change topic
        if not Question.objects.filter(topic=climate_change).exists():
            q6 = Question.objects.create(section=env_section, topic=climate_change, question_text='What is the main cause of current climate change?', difficulty='easy')
            Choice.objects.create(question=q6, choice_text='Human activities', is_correct=True)
            Choice.objects.create(question=q6, choice_text='Natural cycles', is_correct=False)
            Choice.objects.create(question=q6, choice_text='Volcanic eruptions', is_correct=False)
            Choice.objects.create(question=q6, choice_text='Ocean currents', is_correct=False)

            q7 = Question.objects.create(section=env_section, topic=climate_change, question_text='What is the current CO2 level in the atmosphere?', difficulty='medium')
            Choice.objects.create(question=q7, choice_text='Over 420 ppm', is_correct=True)
            Choice.objects.create(question=q7, choice_text='About 200 ppm', is_correct=False)
            Choice.objects.create(question=q7, choice_text='About 100 ppm', is_correct=False)
            Choice.objects.create(question=q7, choice_text='About 600 ppm', is_correct=False)

            q8 = Question.objects.create(section=env_section, topic=climate_change, question_text='How much has the global average temperature increased since the late 19th century?', difficulty='medium')
            Choice.objects.create(question=q8, choice_text='About 1.1°C', is_correct=True)
            Choice.objects.create(question=q8, choice_text='About 5°C', is_correct=False)
            Choice.objects.create(question=q8, choice_text='About 0.1°C', is_correct=False)
            Choice.objects.create(question=q8, choice_text='About 10°C', is_correct=False)

        # Create questions for Wildlife Protection topic
        if not Question.objects.filter(topic=wildlife_protection).exists():
            q9 = Question.objects.create(section=env_section, topic=wildlife_protection, question_text='When was Project Tiger launched in India?', difficulty='easy')
            Choice.objects.create(question=q9, choice_text='1973', is_correct=True)
            Choice.objects.create(question=q9, choice_text='1980', is_correct=False)
            Choice.objects.create(question=q9, choice_text='1965', is_correct=False)
            Choice.objects.create(question=q9, choice_text='1990', is_correct=False)

            q10 = Question.objects.create(section=env_section, topic=wildlife_protection, question_text='How many tiger reserves are there in India?', difficulty='medium')
            Choice.objects.create(question=q10, choice_text='Over 50', is_correct=True)
            Choice.objects.create(question=q10, choice_text='About 10', is_correct=False)
            Choice.objects.create(question=q10, choice_text='About 100', is_correct=False)
            Choice.objects.create(question=q10, choice_text='About 5', is_correct=False)

            q11 = Question.objects.create(section=env_section, topic=wildlife_protection, question_text='What is India\'s national animal?', difficulty='easy')
            Choice.objects.create(question=q11, choice_text='Bengal Tiger', is_correct=True)
            Choice.objects.create(question=q11, choice_text='Asiatic Lion', is_correct=False)
            Choice.objects.create(question=q11, choice_text='Indian Elephant', is_correct=False)
            Choice.objects.create(question=q11, choice_text='One-horned Rhinoceros', is_correct=False)

        # Environment questions (without specific topic - fallback)
        if not Question.objects.filter(section=env_section, topic__isnull=True).exists():
            q12 = Question.objects.create(section=env_section, question_text='What is climate change?', difficulty='easy')
            Choice.objects.create(question=q12, choice_text='A change in weather', is_correct=False)
            Choice.objects.create(question=q12, choice_text='Long-term changes in temperature and weather patterns', is_correct=True)
            Choice.objects.create(question=q12, choice_text='A type of storm', is_correct=False)

            q13 = Question.objects.create(section=env_section, question_text='What is biodiversity?', difficulty='medium')
            Choice.objects.create(question=q13, choice_text='The variety of life on Earth', is_correct=True)
            Choice.objects.create(question=q13, choice_text='A type of energy', is_correct=False)
            Choice.objects.create(question=q13, choice_text='A chemical compound', is_correct=False)

        # ========================================
        # KERALA HERITAGE SITES - TOPICS
        # ========================================
        fort_kochi, _ = Topic.objects.get_or_create(
            name='Fort Kochi',
            section=heritage_section,
            defaults={
                'description': 'Explore the historic Fort Kochi area with its colonial architecture and cultural blend.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/St._Francis_Church_Kochi.jpg/1200px-St._Francis_Church_Kochi.jpg',
                'order': 1
            }
        )
        
        # Fort Kochi Module 1
        StudyMaterial.objects.get_or_create(
            topic=fort_kochi,
            title='Module 1: Introduction to Fort Kochi',
            defaults={
                'content_text': '''Introduction to Fort Kochi

Fort Kochi is a historic port city in Kerala known for its rich colonial heritage and cultural diversity.

 Location and History

Located in the **Ernakulam district**, Fort Kochi has been a center of trade for centuries. The area gets its name from the Fort of Kochi, which was built by the **Portuguese in 1503**.

 Historical Timeline
- **1503**: Portuguese build the first European fort in India
- **1663**: Dutch capture Kochi and develop the area
- **1795**: British take control of Kochi
- **1947**: Independence of India

 Key Landmarks

 St. Francis Church
Built in **1503**, St. Francis Church is one of the oldest European churches in India:
- Originally built by the Portuguese
- Rebuilt by the Dutch in 1779
- Famous poet Samoothiri Ravi Varma was buried here
- Known for its simple yet elegant architecture

 Santa Cruz Basilica
A beautiful Gothic-style church featuring:
- Intricate stained glass windows
- Impressive architecture
- Rich interior decorations

 Chinese Fishing Nets
Known locally as **"Cheenavalai"**, these iconic fishing nets:
- Were introduced by Chinese traders during the 14th century
- Are a unique sight along the coastline
- Still used by local fishermen today
- Create a stunning visual against sunset

### Indo-Portuguese Museum
Showcases the fusion of cultures:
- Historical artifacts
- Religious sculptures
- Cultural memorabilia''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/St._Francis_Church_Kochi.jpg/1200px-St._Francis_Church_Kochi.jpg',
                'order': 1
            }
        )
        
        # Fort Kochi Module 2
        StudyMaterial.objects.get_or_create(
            topic=fort_kochi,
            title='Module 2: Cultural Fusion in Fort Kochi',
            defaults={
                'content_text': '''Cultural Fusion in Fort Kochi

Fort Kochi is a unique blend of various cultures that have settled here over centuries.

 Portuguese Influence

The Portuguese were the first Europeans to establish trade relations with Kerala:
- Built the first fort in 1503
- Introduced Christianity to the region
- Created the first European settlement in India
- Left behind churches and colonial bungalows

 Dutch Influence

The Dutch who captured Kochi in **1663** developed the area significantly:
- Built the famous **Dutch Palace** (Mattancherry Palace)
- Established spice trade
- Created the famous Jew Street
- Introduced architectural styles

 British Influence

The British established their presence later:
- Added colonial architectural elements
- Developed the harbor
- Established administrative systems

 Jewish Influence

The Jewish community settled here, creating:
- **Jew Street** (Jew Town)
- **Paradesi Synagogue** - the oldest active synagogue in the Commonwealth
- Jewish cemetery
- Spice and antique markets

 Chinese Influence

Chinese traders left a unique legacy:
- **Chinese Fishing Nets** - Cheenavalai
- Trade in silk and spices
- Cultural exchange in maritime activities

 Modern Fort Kochi

Today, Fort Kochi is known for:
- **Kochi-Muziris Biennale** - International art exhibition
- Colonial architecture blending with modern facilities
- Spice markets
- Antique shops
- Cafés and art galleries

 Things to Do

1. Watch the sunset at Chinese Fishing Nets
2. Visit St. Francis Church
3. Explore the Jewish Quarter
4. Enjoy local cuisine
5. Visit the Kochi Maritime Museum
6. Take a boat ride through the backwaters''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Chinese_fishing_nets_Kochi.jpg/1200px-Chinese_fishing_nets_Kochi.jpg',
                'order': 2
            }
        )

        padmanabhapuram, _ = Topic.objects.get_or_create(
            name='Padmanabhapuram Palace',
            section=heritage_section,
            defaults={
                'description': 'Discover the ancient wooden palace of the Travancore kings.',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Padmanabhapuram_Palace.jpg/1200px-Padmanabhapuram_Palace.jpg',
                'order': 2
            }
        )
        
        # Padmanabhapuram Palace Module 1
        StudyMaterial.objects.get_or_create(
            topic=padmanabhapuram,
            title='Module 1: History of Padmanabhapuram Palace',
            defaults={
                'content_text': '''History of Padmanabhapuram Palace

Padmanabhapuram Palace is one of the oldest wooden palaces in the world, located in Kanyakumari district but historically part of the **Travancore kingdom**.

 Historical Background

 Establishment
- Built in the **16th century** (around 1550 AD)
- Served as the residence of the **Travancore rulers**
- Was the capital of the Venad kingdom before Thiruvananthapuram
- Remained the royal residence until 1795

 Notable Rulers
- **Marthanda Varma** (1729-1758) - Founded modern Travancore
- **Karthika Thirunal** - Known for reforms
- **Rama Varma** - Expanded the kingdom

 Location

Although located in **Kanyakumari district, Tamil Nadu**, the palace historically belonged to the Travancore kingdom:
- Now maintained by the **Archaeological Survey of India**
- One of the most visited heritage sites in South India
- About 50 km from Thiruvananthapuram

 Architectural Significance

The palace represents the zenith of **traditional Kerala architecture**:
- Entirely made of wood (teak, rosewood, and coconut wood)
- No nails used in construction - only wooden pins
- Beautiful murals depicting mythological stories
- Unique ventilation system using copper plates

 Notable Features

 murals
The palace has exquisite murals:
- Scenes from Ramayana and Mahabharata
- Portraits of kings and queens
- Nature and floral designs
- Some murals over 400 years old

 The Clock Tower
- Known as "Kallanai"
- Still functional after centuries
- Shows blend of Indian and European styles''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Padmanabhapuram_Palace.jpg/1200px-Padmanabhapuram_Palace.jpg',
                'order': 1
            }
        )
        
        # Padmanabhapuram Palace Module 2
        StudyMaterial.objects.get_or_create(
            topic=padmanabhapuram,
            title='Module 2: Architecture and Features',
            defaults={
                'content_text': '''Architecture and Features

Padmanabhapuram Palace is a masterpiece of traditional Kerala architecture.

 Construction Techniques

 Woodwork
- Made primarily of **Teak wood** (Theku)
- **Rosewood** (Paliwood) for intricate carvings
- **Coconut wood** for certain sections
- No iron nails - only wooden pegs

 Unique Features
- Earthquake-resistant design
- Natural cooling systems
- Ventilation through copper plates
- Rainwater harvesting system

 Palace Sections

 Mantrasala (King's Council Chamber)
- Where the king held meetings
- Beautiful wooden carvings
- Historical murals

 Nalukettu (Four-Hall Structure)
- Traditional Kerala architectural style
- Central courtyard
- Surrounding rooms

 Theppakavu (Boat House)
- Used for royal ceremonies
- Located near the palace pond

 Mathilakam (Fortified Walls)
- Inner fortress
- Watch towers
- Secret passages

 Sthalapura (Royal Bedchamber)
- Ornate wooden beds
- Ivory decorations
- Historical artifacts

 The Famous "Thiruvathira" Dance Hall

This hall is renowned for its acoustic perfection:
- Circular design
- Perfect sound projection
- Where classical dance performances were held
- Features of the hall enhance musical sounds

 Cultural Significance

 murals
The palace contains murals that are:
- Over 400 years old
- Depicting mythological stories
- Using natural pigments
- Preserved by ASI

 Impact on Architecture
- Influenced later Travancore architecture
- Documented architectural techniques
- Preserved traditional craftsmanship

 Preservation

The Archaeological Survey of India maintains the palace:
- Regular restoration work
- Preserving original features
- Open to public visitors
- Important tourist destination''',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Padmanabhapuram_Palace.jpg/1200px-Padmanabhapuram_Palace.jpg',
                'order': 2
            }
        )

        # ========================================
        # KERALA HERITAGE SITES - ADDITIONAL SITES
        # ========================================
        
        # ========================================
        # KERALA CULTURAL ARTFORMS - ADDITIONAL CONTENT
        # ========================================

        self.stdout.write(self.style.SUCCESS('Sample data added successfully'))
