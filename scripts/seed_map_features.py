import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from mainapp.models import Topic, CollectibleItem, MatchQuiz, MatchPair, District

def run():
    print("Seeding Gamification and Match Quizzes...")
    
    # Get topics
    theyyam = Topic.objects.filter(name='Theyyam').first()
    kathakali = Topic.objects.filter(name='Kathakali').first()
    fort_kochi = Topic.objects.filter(name='Fort Kochi').first()
    backwaters = Topic.objects.filter(name='Below Sea Level (Kuttanad)').first()
    highlands = Topic.objects.filter(name='Highlands (Western Ghats)').first()

    if theyyam:
        q, _ = MatchQuiz.objects.get_or_create(topic=theyyam, title="Match the Artform Attributes")
        MatchPair.objects.get_or_create(quiz=q, left_item="Theyyam", right_item="North Malabar", order=1)
        MatchPair.objects.get_or_create(quiz=q, left_item="Face Painting", right_item="Intricate Designs", order=2)
        MatchPair.objects.get_or_create(quiz=q, left_item="Ritual Dance", right_item="Worship", order=3)
    
    # Badges (Collectibles) aligned to topics
    if kathakali:
        c, _ = CollectibleItem.objects.get_or_create(name="Kathakali Mask", defaults={'category': 'folklore', 'description': 'A symbolic mask.', 'rarity': 'epic'})
        c.associated_topic = kathakali
        c.save()

    if fort_kochi:
        c, _ = CollectibleItem.objects.get_or_create(name="Chinese Fishing Nets", defaults={'category': 'artifact', 'description': 'Iconic fishing nets in Kochi.', 'rarity': 'common'})
        c.associated_topic = fort_kochi
        c.save()

    if backwaters:
        c, _ = CollectibleItem.objects.get_or_create(name="Houseboat", defaults={'category': 'artifact', 'description': 'Traditional Kettuvallam.', 'rarity': 'rare'})
        c.associated_topic = backwaters
        c.save()
        
    if highlands:
        c, _ = CollectibleItem.objects.get_or_create(name="Nilgiri Tahr", defaults={'category': 'fauna', 'description': 'Endemic mountain goat.', 'rarity': 'legendary'})
        c.associated_topic = highlands
        c.save()

    print("Seeding Complete.")

if __name__ == '__main__':
    run()
