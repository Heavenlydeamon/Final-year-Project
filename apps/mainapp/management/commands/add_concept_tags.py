from django.core.management.base import BaseCommand
from mainapp.models import ConceptTag


class Command(BaseCommand):
    help = 'Add sample concept tags for AI-based recommendations'

    def handle(self, *args, **kwargs):
        concept_tags = [
            # Environmental Concepts
            {'name': 'Carbon Cycle', 'description': 'The process of carbon cycling through the atmosphere, biosphere, and geosphere'},
            {'name': 'Biodiversity', 'description': 'The variety of life in a particular habitat or ecosystem'},
            {'name': 'Ecosystem Balance', 'description': 'The equilibrium state where organisms interact with each other and their environment'},
            {'name': 'Wildlife Conservation', 'description': 'Protecting wild animals and their habitats'},
            {'name': 'Climate Change', 'description': 'Long-term changes in global temperature and weather patterns'},
            {'name': 'Sustainable Development', 'description': 'Development that meets present needs without compromising future generations'},
            {'name': 'Environmental Impact', 'description': 'Effects of human activities on the environment'},
            
            # Heritage & Cultural Concepts
            {'name': 'Heritage Preservation', 'description': 'Protecting and maintaining historical and cultural heritage sites'},
            {'name': 'Cultural Artforms', 'description': 'Traditional arts, crafts, and performing arts'},
            {'name': 'Traditional Knowledge', 'description': 'Indigenous knowledge passed down through generations'},
            {'name': 'Historical Sites', 'description': 'Locations of historical significance'},
            {'name': 'Archaeological Heritage', 'description': 'Physical remains of past human activity'},
            
            # Western Ghats Specific
            {'name': 'Western Ghats', 'description': 'The mountain range along the western side of India'},
            {'name': 'Endemic Species', 'description': 'Species found only in a specific region'},
            {'name': 'Tropical Forest', 'description': 'Forests in tropical regions with high rainfall'},
            {'name': 'Bio-diversity Hotspot', 'description': 'Regions with high biodiversity and conservation importance'},
            
            # General Learning
            {'name': 'Definitions', 'description': 'Clear explanations of key terms and concepts'},
            {'name': 'Processes', 'description': 'Step-by-step explanations of how things work'},
            {'name': 'Case Studies', 'description': 'Real-world examples and applications'},
            {'name': 'Analysis', 'description': 'In-depth examination and evaluation'},
        ]
        
        created_count = 0
        for tag_data in concept_tags:
            tag, created = ConceptTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'description': tag_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created: {tag.name}')
            else:
                self.stdout.write(f'Already exists: {tag.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully added {created_count} new concept tags. Total: {ConceptTag.objects.count()}'))
