import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, StoryScene

def seed_learning_modes():
    # Target topic
    topic_name = "Highlands (Western Ghats)"
    try:
        topic = Topic.objects.filter(name__icontains="Highlands").first()
        if not topic:
            print("Topic 'Highlands' not found. Creating a temporary one for demo.")
            from mainapp.models import Section
            section = Section.objects.filter(is_general=True).first()
            topic = Topic.objects.create(
                name="Highlands (Western Ghats)",
                description="The biological island of Kerala.",
                section=section,
                is_general=True
            )
        
        print(f"Seeding content for: {topic.name}")

        # 1. Clear existing scenes to avoid duplicates
        StoryScene.objects.filter(topic=topic).delete()

        # 2. Add Story Scenes
        scenes = [
            (1, "Deep in the mists of the Western Ghats, an ancient secret was waiting. The Sahyadri mountains are older than the Himalayas themselves!"),
            (2, "These mountains act as a giant wall, catching the monsoon clouds and giving Kerala its life-giving rain. Without them, our land would be a desert."),
            (3, "High up on the peaks, we find the Nilgiri Tahr. These brave mountain goats can climb near-vertical cliffs with their special rubbery hooves."),
            (4, "Deep in the valleys, the Shola forests stay cool and damp, protecting species like the Purple Frog that has lived here since the time of dinosaurs."),
            (5, "But our highlands are in danger. People are building too much and cutting down forests. We must become the guardians of the Sahyadri!")
        ]

        for num, text in scenes:
            StoryScene.objects.create(topic=topic, scene_number=num, text=text)
            print(f"Added Story Scene {num}")

        print("Successfully seeded Story mode!")

        # 4. Add Districts
        from mainapp.models import District
        District.objects.all().delete()
        
        # Mapping districts to topics
        # Note: We'll use simple rectangular coordinates for this demo
        # Format for 'poly': x1,y1,x2,y2,x3,y3...
        dist_data = [
            ("Kasaragod", "Theyyam", "50,50,150,50,150,150,50,150"),
            ("Wayanad", "Highlands", "100,200,200,200,200,300,100,300"),
            ("Thrissur", "Panchavadyam", "50,400,150,400,150,500,50,500"),
            ("Ernakulam", "Fort Kochi", "150,500,250,500,250,600,150,600"),
            ("Alappuzha", "Lowlands", "100,650,200,650,200,750,100,750"),
            ("Kannur", "Theyyam", "30,150,130,150,130,250,30,250"),
        ]

        for name, topic_search, coords in dist_data:
            target_topic = Topic.objects.filter(name__icontains=topic_search).first()
            if target_topic:
                District.objects.create(name=name, topic=target_topic, coords=coords)
                print(f"Added District {name} linked to {target_topic.name}")

        print("Successfully seeded Districts!")

    except Exception as e:
        print(f"Error seeding: {e}")

if __name__ == "__main__":
    seed_learning_modes()
