import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import District, Topic
from django.db import transaction

def seed_map_details():
    districts_data = [
        {"name": "Kasaragod", "topic": "Lowlands (Coastal Plains)", "folklore": "Folklore in keralam"},
        {"name": "Kannur", "topic": "Theyyam", "folklore": "Folklore in keralam"},
        {"name": "Wayanad", "topic": "Highlands (Western Ghats)", "folklore": "Kerala Cuisine and Spice Trade"},
        {"name": "Kozhikode", "topic": "Kerala Cultural Heritage", "folklore": "The legend of Mahabali"},
        {"name": "Malappuram", "topic": "Kalaripayattu", "folklore": "Folklore in keralam"},
        {"name": "Palakkad", "topic": "Midlands (The Transition Belt)", "folklore": "Panchavadyam"},
        {"name": "Thrissur", "topic": "Panchavadyam", "folklore": "Kerala Cultural Heritage"},
        {"name": "Ernakulam", "topic": "Fort Kochi", "folklore": "Kerala Cuisine and Spice Trade"},
        {"name": "Idukki", "topic": "Highlands (Western Ghats)", "folklore": "The Geographic History of Kerala: From Gondwana to the Arabian Sea"},
        {"name": "Kottayam", "topic": "Midlands (The Transition Belt)", "folklore": "Folklore in keralam"},
        {"name": "Alappuzha", "topic": "Below Sea Level (Kuttanad)", "folklore": "The legend of Mahabali"},
        {"name": "Pathanamthitta", "topic": "Midlands (The Transition Belt)", "folklore": "Folklore in keralam"},
        {"name": "Kollam", "topic": "Midlands (The Transition Belt)", "folklore": "Folklore in keralam"},
        {"name": "Thiruvananthapuram", "topic": "Lowlands (Coastal Plains)", "folklore": "Kerala Cultural Heritage"},
    ]

    with transaction.atomic():
        for d_info in districts_data:
            topic = Topic.objects.filter(name=d_info["topic"]).first()
            folklore = Topic.objects.filter(name=d_info["folklore"]).first()
            
            if not topic:
                # Fallback if specific topic not found
                topic = Topic.objects.first()
            
            district, created = District.objects.get_or_create(
                name=d_info["name"],
                defaults={
                    "topic": topic,
                    "folklore_topic": folklore,
                    "coords": "0,0,100,100" # Placeholder for now
                }
            )
            
            if not created:
                district.topic = topic
                district.folklore_topic = folklore
                district.save()
            
            print(f"{'Created' if created else 'Updated'} district: {d_info['name']}")

if __name__ == "__main__":
    seed_map_details()
