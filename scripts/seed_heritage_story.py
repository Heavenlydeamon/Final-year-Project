import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from django.contrib.auth.models import User
from content.models import Topic, Story, StoryPanel
from activities.models import ActivityQuestion

def seed_story():
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    # 1. Create Topic
    topic, _ = Topic.objects.get_or_create(
        title="Legends of Kerala",
        defaults={
            'category': 'heritage',
            'class_level': 'lower',
            'description': "Enchanting tales from the Land of Coconut Trees that teach us wise lessons.",
            'thumbnail': 'topics/legends_thumb.png',
            'is_published': True,
            'created_by': admin
        }
    )

    # 2. Create Story
    story, _ = Story.objects.get_or_create(
        topic=topic,
        title="The Happy Stone Roller of Rayiranellur",
        defaults={
            'tagline': "Discover why the wise Naranathu Branthan rolled a giant stone every day!",
            'cover_image': 'stories/covers/naranath_cover.png',
            'character_name': "Naranath",
            'character_age': 70,
            'character_avatar': "👴",
            'character_description': "A wise and happy man who lived on a beautiful hill.",
            'story_type': 'admin_original',
            'status': 'published',
            'created_by': admin,
            'approved_by': admin
        }
    )

    # 3. Create Story Panels
    panels_data = [
        {
            'order': 1,
            'panel_type': 'narration',
            'title': "The Giant Stone",
            'text': "Long ago, in a place called Rayiranellur, lived a man named Naranathu Branthan. Every morning, he would roll a huge, heavy stone up a tall green hill.",
            'image': 'stories/panels/naranath_1.png'
        },
        {
            'order': 2,
            'panel_type': 'narration',
            'title': "The Joyful Laugh",
            'text': "When he finally reached the top, he would give the stone a little push. He watched it roll all the way down, laughing loudly with joy! 'Ha ha ha!' he would cheer.",
            'image': 'stories/panels/naranath_2.png'
        },
        {
            'order': 3,
            'panel_type': 'fact',
            'title': "Did You Know?",
            'text': "Naranathu Branthan was one of the twelve children in the famous legend 'Parayi Petta Panthirukulam'. He was very wise but pretended to be a bit silly!",
            'image': 'stories/panels/naranath_3.png'
        },
        {
            'order': 4,
            'panel_type': 'activity',
            'title': "Help Naranath!",
            'text': "Can you remember the order of Naranath's day? Let's put the events in the right order!",
            'image': 'stories/panels/naranath_1.png'
        }
    ]

    for p in panels_data:
        panel, created = StoryPanel.objects.get_or_create(
            story=story,
            order=p['order'],
            defaults={
                'panel_type': p['panel_type'],
                'title': p['title'],
                'text': p['text'],
                'image': p['image']
            }
        )
        
        # If it's an activity panel, link it
        if p['panel_type'] == 'activity':
            activity, _ = ActivityQuestion.objects.get_or_create(
                topic=topic,
                question_type='sequence',
                defaults={
                    'question_text': "Put Naranath's story in order!",
                    'items': {
                        "items": [
                            {"id": "step1", "label": "Naranath finds a big stone", "image": "/media/stories/panels/naranath_1.png"},
                            {"id": "step2", "label": "He rolls it up the hill", "image": "/media/stories/panels/naranath_1.png"},
                            {"id": "step3", "label": "The stone rolls down", "image": "/media/stories/panels/naranath_2.png"},
                            {"id": "step4", "label": "Naranath laughs with joy", "image": "/media/stories/panels/naranath_2.png"}
                        ]
                    },
                    'answer': ["step1", "step2", "step3", "step4"],
                    'explanation': "Naranath enjoyed the hard work and the fun part too!",
                    'order': 1,
                    'created_by': admin
                }
            )
            panel.linked_activity = activity
            panel.save()

    print(f"Successfully seeded story: {story.title}")

if __name__ == "__main__":
    seed_story()
