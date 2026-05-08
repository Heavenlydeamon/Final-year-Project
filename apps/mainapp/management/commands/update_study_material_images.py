from django.core.management.base import BaseCommand
from mainapp.models import StudyMaterial
from urllib.parse import quote

class Command(BaseCommand):
    help = 'Update image URLs for all study materials using reliable Unsplash links'

    # Valid Unsplash photo IDs for nature/environment/heritage themes
    UNSPLASH_PHOTO_IDS = [
        '1501854140884-074cf2b21d25',  # Nature landscape
        '1507003211169-0a1dd7228f2d',  # Forest
        '1470071459604-3b5ec3a7fe05',  # Mountain nature
        '1441974231531-c6227db76b6e',  # Forest sunlight
        '1518173947018-37e981d7d5c4',  # Heritage building
        '1564496907526-aa18160d8b9c',  # Cultural heritage
        '1464822759023-fed622ff2c3b',  # Mountain
        '1426604960688-7e74dc2ba4ed',  # Nature
        '1472214103451-9374bd1c798e',  # Landscape
        '1433086977785-6c92a5c29a55',  # Forest
        '1507525428034-b723cf961d3e',  # Beach
        '1475924156734-499f1d8a04c6',  # Temple/heritage
        '1518709262918-5ab5ed9e9e25',  # Western ghats
        '1447752875204-b2f979455950',  # Nature
        '1470091715977-b8db4d2c9c04',  # Forest
    ]

    def handle(self, *args, **options):
        # select_related helps fetch topic and section data in one database hit
        study_materials = list(StudyMaterial.objects.select_related('topic__section').all())
        
        if not study_materials:
            self.stdout.write(self.style.WARNING('No study materials found.'))
            return

        updated_count = 0

        for material in study_materials:
            # 1. Logic for choosing the best keyword
            keyword = 'nature'
            if material.topic:
                if material.topic.name:
                    keyword = material.topic.name
                elif material.topic.section and material.topic.section.name:
                    keyword = material.topic.section.name

            # 2. Make the keyword URL-safe
            safe_keyword = quote(keyword)

            # 3. Select a valid Unsplash photo ID based on material ID
            photo_id = self.UNSPLASH_PHOTO_IDS[material.id % len(self.UNSPLASH_PHOTO_IDS)]

            # 4. Use the stable Unsplash Image URL with valid photo ID
            # Format: https://images.unsplash.com/photo-1?auto=format&fit=crop&w=800&q=80&{keyword}&sig={material.id}
            url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80&keyword={safe_keyword}&sig={material.id}"
            
            material.image_url = url
            updated_count += 1
            self.stdout.write(f'Updated: {material.title[:30]}... with "{keyword}"')

        # 5. Save all changes at once for speed
        StudyMaterial.objects.bulk_update(study_materials, ['image_url'])

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} study materials!')
        )
