from django.core.management.base import BaseCommand
from django.db.models import Q
from mainapp.models import StudyMaterial, Topic, Section


class Command(BaseCommand):
    help = 'Remove images from all general study materials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to remove images from general study materials...'))
        
        # Get all study materials where the topic's section is general (is_general=True)
        # This means we need to filter through Topic -> Section relationship
        general_study_materials = StudyMaterial.objects.filter(
            topic__section__is_general=True
        ).select_related('topic__section')
        
        count = general_study_materials.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('No general study materials found.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {count} general study materials to process.'))
        
        removed_url_count = 0
        removed_image_count = 0
        
        for material in general_study_materials:
            section_name = material.topic.section.name if material.topic.section else 'Unknown'
            topic_name = material.topic.name if material.topic else 'Unknown'
            
            # Clear image_url if it has a value
            if material.image_url:
                self.stdout.write(f'Removing image_url from: {material.title} (Section: {section_name}, Topic: {topic_name})')
                material.image_url = ''
                removed_url_count += 1
            
            # Clear image file field if it has a value
            if material.image:
                self.stdout.write(f'Removing image file from: {material.title} (Section: {section_name}, Topic: {topic_name})')
                material.image = None
                removed_image_count += 1
            
            # Save the material
            material.save()
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Total general study materials processed: {count}'))
        self.stdout.write(self.style.SUCCESS(f'Removed image_url from: {removed_url_count} materials'))
        self.stdout.write(self.style.SUCCESS(f'Removed image file from: {removed_image_count} materials'))
