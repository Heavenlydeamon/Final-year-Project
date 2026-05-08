from django.core.management.base import BaseCommand
from mainapp.models import Topic, Section

class Command(BaseCommand):
    help = 'Update Western Ghats topic image'

    def handle(self, *args, **options):
        env_section = Section.objects.filter(name='Environment').first()
        if not env_section:
            self.stdout.write(self.style.ERROR('Environment section not found'))
            return
        
        topic = Topic.objects.filter(name='Western Ghats', section=env_section).first()
        if topic:
            topic.image_url = '/static/images/wes.jpeg'
            topic.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Western Ghats image to: {topic.image_url}'))
        else:
            self.stdout.write(self.style.ERROR('Western Ghats topic not found'))
