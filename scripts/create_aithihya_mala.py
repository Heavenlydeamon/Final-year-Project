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

# 1. Get the Topic (Folklore in keralam)
topic = Topic.objects.get(id=2)

# 2. Create the Drag & Drop Activity
activity_items = {
    "draggables": [
        {"id": "kochunni", "label": "Kochunni's Coin", "image": "/media/study_materials/images/onam.png"},
        {"id": "kathanar", "label": "Kathanar's Wand", "image": "/media/study_materials/images/theyyam.png"},
        {"id": "theyyam", "label": "Theyyam Mask", "image": "/media/study_materials/images/theyyam.png"}
    ],
    "containers": [
        {"id": "thief", "label": "Kind Thief", "icon": "👤"},
        {"id": "magic", "label": "Magical Priest", "icon": "🪄"},
        {"id": "ritual", "label": "Divine Ritual", "icon": "🎭"}
    ]
}

activity_answer = {
    "matches": [
        {"draggableId": "kochunni", "containerId": "thief"},
        {"draggableId": "kathanar", "containerId": "magic"},
        {"draggableId": "theyyam", "containerId": "ritual"}
    ]
}

activity = ActivityQuestion.objects.create(
    topic=topic,
    question_type='drag_drop',
    question_text="Aditya is confused! Can you help him match the items to the legends?",
    items=activity_items,
    answer=activity_answer,
    created_by=user
)

# 3. Create the Story
story = Story.objects.create(
    topic=topic,
    title="Aithihya Mala: The Magic Garland",
    tagline="Discover the legendary heroes and magical creatures of Kerala!",
    cover_image="study_materials/images/kathakali.png", # Reusing existing media
    character_name="Aditya",
    character_age=8,
    character_avatar="🧒",
    character_description="A curious boy who loves old stories and mysteries.",
    created_by=user,
    status='published'
)

# 4. Create Story Panels
panels = [
    {
        "order": 1,
        "type": "narration",
        "title": "The Old Attic",
        "text": "Aditya was exploring his grandfather's dusty attic when he found a beautiful book with golden letters: 'Aithihya Mala'.",
        "image": "study_materials/images/palace.png"
    },
    {
        "order": 2,
        "type": "narration",
        "title": "The Glowing Book",
        "text": "As soon as he touched the book, it began to glow! The stories of ancient Kerala were waking up.",
        "image": "study_materials/images/vishu.png"
    },
    {
        "order": 3,
        "type": "narration",
        "title": "Meeting the Heroes",
        "text": "Suddenly, a kind man appeared. It was Kayamkulam Kochunni! He told Aditya, 'Our legends are fading, help us bring them back!'",
        "image": "study_materials/images/kalaripayattu.png"
    },
    {
        "order": 4,
        "type": "activity",
        "title": "The Legend Challenge",
        "text": "To open the next chapter, Aditya needs to match these magical items to their owners. Can you help him?",
        "image": "study_materials/images/onam.png",
        "activity": activity
    },
    {
        "order": 5,
        "type": "narration",
        "title": "The Garland Complete",
        "text": "Well done! The legends are safe. Aditya realized that these stories are the real treasures of Kerala.",
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
