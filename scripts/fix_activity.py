import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from activities.models import ActivityQuestion

# Target media directory
media_dir = os.path.join("d:\\", "Eco Legacy main project file", "ecoheritage", "media", "study_materials", "images")
os.makedirs(media_dir, exist_ok=True)

# Copy the generated images
import glob
kochunni_img = glob.glob("C:\\Users\\LOQ\\.gemini\\antigravity\\brain\\3bfedbce-a54d-44d3-8c8f-6e0c375b0977\\kochunni_coin_*.png")[0]
kathanar_img = glob.glob("C:\\Users\\LOQ\\.gemini\\antigravity\\brain\\3bfedbce-a54d-44d3-8c8f-6e0c375b0977\\kathanar_wand_*.png")[0]
theyyam_img = glob.glob("C:\\Users\\LOQ\\.gemini\\antigravity\\brain\\3bfedbce-a54d-44d3-8c8f-6e0c375b0977\\theyyam_mask_*.png")[0]

shutil.copy(kochunni_img, os.path.join(media_dir, "kochunni_coin.png"))
shutil.copy(kathanar_img, os.path.join(media_dir, "kathanar_wand.png"))
shutil.copy(theyyam_img, os.path.join(media_dir, "theyyam_mask.png"))

# Find the activity
activity = ActivityQuestion.objects.filter(question_text="Aditya is confused! Can you help him match the items to the legends?").first()

if activity:
    items = activity.items
    for draggable in items.get('draggables', []):
        if draggable['id'] == 'kochunni':
            draggable['image'] = '/media/study_materials/images/kochunni_coin.png'
        elif draggable['id'] == 'kathanar':
            draggable['image'] = '/media/study_materials/images/kathanar_wand.png'
        elif draggable['id'] == 'theyyam':
            draggable['image'] = '/media/study_materials/images/theyyam_mask.png'
            
    activity.items = items
    
    # Let's ensure the answer structure is also correct
    # The current answer might be {"matches": [...]}
    activity.save()
    print("Activity updated successfully!")
else:
    print("Activity not found.")
