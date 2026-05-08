import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from content.models import Topic, Story, StoryPanel
from activities.models import ActivityQuestion
from django.contrib.auth.models import User

# Get a user (admin or any teacher)
user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.first()

# 1. Get the Topic (Kerala Cuisine and Spice Trade)
topic = Topic.objects.get(id=31)

# 2. Create the Image Pick Activity
activity_items = {
    "options": [
        {"id": "pepper", "label": "Black Pepper", "image": "/media/study_materials/images/western_ghats.png"},
        {"id": "cardamom", "label": "Cardamom", "image": "/media/study_materials/images/onam.png"},
        {"id": "ginger", "label": "Ginger", "image": "/media/study_materials/images/vishu.png"},
        {"id": "cinnamon", "label": "Cinnamon", "image": "/media/study_materials/images/palace.png"}
    ]
}

activity_answer = "pepper"

activity = ActivityQuestion.objects.create(
    topic=topic,
    question_type='image_pick',
    question_text="Which of these spices was known as 'Black Gold' and brought traders from all over the world to Kerala?",
    items=activity_items,
    answer=activity_answer,
    created_by=user
)

# 3. Create the Story
story = Story.objects.create(
    topic=topic,
    title="Ancient Kerala: Land of Spices",
    tagline="Follow Meenu and her talking parrot Pappu on a journey to the land of Black Gold!",
    cover_image="study_materials/images/western_ghats.png",
    character_name="Meenu",
    character_age=7,
    character_avatar="👧",
    character_description="A little girl who loves the smell of fresh spices in her mother's kitchen.",
    created_by=user,
    status='published'
)

# 4. Create Story Panels
panels = [
    {
        "order": 1,
        "type": "narration",
        "title": "The Magic Spice Box",
        "text": "In Meenu's kitchen, there was an old wooden box. When she opened it, a wonderful aroma filled the air. 'That's the smell of history!' chirped her parrot, Pappu.",
        "image": "study_materials/images/palace.png"
    },
    {
        "order": 2,
        "type": "narration",
        "title": "The Mountains of Gold",
        "text": "Pappu took Meenu to the high mountains. 'Look!' he said. The hills were covered in green vines dripping with tiny black berries. This was the famous Kerala Pepper!",
        "image": "study_materials/images/western_ghats.png"
    },
    {
        "order": 3,
        "type": "narration",
        "title": "Visitors from Far Away",
        "text": "Down at the port, Meenu saw giant ships with big white sails. People from Arabia and Rome had traveled for months just to buy these tiny spices.",
        "image": "study_materials/images/fort_kochi.png"
    },
    {
        "order": 4,
        "type": "activity",
        "title": "The Trader's Secret",
        "text": "One trader lost his way! Can you help him find the most valuable spice in Kerala, the one they call 'Black Gold'?",
        "image": "study_materials/images/onam.png",
        "activity": activity
    },
    {
        "order": 5,
        "type": "narration",
        "title": "A World of Flavor",
        "text": "Because of these spices, Kerala became famous all over the world. Meenu realized that her kitchen was connected to the whole wide world!",
        "image": "study_materials/images/boat_race.png"
    }
]

for p in panels:
    StoryPanel.objects.create(
        story=story,
        order=p["order"],
        panel_type=p["type"],
        title=p["title"],
        text=p["text"],
        image=p["image"],
        linked_activity=p.get("activity")
    )

print(f"Successfully created story: {story.title} with {len(panels)} panels!")
