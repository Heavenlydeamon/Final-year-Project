import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from content.models import Story, StoryPanel
from activities.models import ActivityQuestion

# Get the Story (ID 2 usually, based on my previous script)
# Let's find it by title
story = Story.objects.get(title="Ancient Kerala: Land of Spices")

# Update Story Cover
story.cover_image = "stories/spices/mountains.png"
story.save()

# Update Panels
panels = story.panels.all().order_by('order')

# Mapping new images to panels
# Panel 1: Kitchen (I'll reuse mountains for now as kitchen failed, or use port)
# Panel 2: Mountains -> mountains.png
# Panel 3: Port -> port.png
# Panel 4: Activity -> pepper.png
# Panel 5: Conclusion -> port.png (reused)

for p in panels:
    if p.order == 1:
        p.image = "stories/spices/mountains.png"
    elif p.order == 2:
        p.image = "stories/spices/mountains.png"
    elif p.order == 3:
        p.image = "stories/spices/port.png"
    elif p.order == 4:
        p.image = "stories/spices/pepper.png"
    elif p.order == 5:
        p.image = "stories/spices/port.png"
    p.save()

# Update Activity Image as well
activity = story.panels.filter(panel_type='activity').first().linked_activity
if activity:
    # Update the pepper option image
    for opt in activity.items['options']:
        if opt['id'] == 'pepper':
            opt['image'] = "/media/stories/spices/pepper.png"
    activity.save()

print(f"Successfully updated story '{story.title}' with high-quality generated images!")
