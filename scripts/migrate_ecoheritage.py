import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from django.contrib.auth.models import User
from mainapp.models import Section as OldSection, Topic as OldTopic, StudyMaterial as OldMaterial, Question as OldQuestion, Choice as OldChoice, MatchQuiz as OldMatchQuiz, MatchPair as OldMatchPair
from content.models import Topic as NewTopic
from classes.models import StudyMaterial as NewMaterial, Class as NewClass
from activities.models import ActivityQuestion as NewActivity
from quiz.models import Quiz as NewQuiz, MCQQuestion as NewMCQ

def migrate_data():
    print("Starting data migration...")

    # 1. Migrate Topics
    print("Migrating Topics...")
    category_map = {
        'Environment': 'environment',
        'Heritage': 'heritage',
        'Cultural': 'artforms', # mapping cultural to artforms as catch-all for now
        'Folklore': 'festivals', # mapping folklore to festivals
    }

    for old_topic in OldTopic.objects.all():
        cat = category_map.get(old_topic.section.name, 'heritage')
        level = 'both' if old_topic.is_general else 'higher'
        
        new_topic, created = NewTopic.objects.get_or_create(
            title=old_topic.name,
            defaults={
                'category': cat,
                'class_level': level,
                'description': old_topic.description,
                'is_published': True,
                # Note: thumbnail might need manual copy or mapping from image_url
            }
        )
        if created:
            print(f"  Created Topic: {new_topic.title}")

    # 2. Migrate Study Materials
    print("Migrating Study Materials...")
    # We need at least one class for Higher Class students to see materials
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    default_class, _ = NewClass.objects.get_or_create(
        name="General Higher Class",
        grade="All",
        teacher=admin_user
    )

    for old_mat in OldMaterial.objects.all():
        try:
            target_topic = NewTopic.objects.get(title=old_mat.topic.name)
            NewMaterial.objects.create(
                class_group=default_class,
                topic=target_topic,
                file=old_mat.video if old_mat.video else (old_mat.audio if old_mat.audio else None),
                content_text=old_mat.content_text
            )
            print(f"  Created Material for: {target_topic.title}")
        except NewTopic.DoesNotExist:
            print(f"  Warning: Target topic {old_mat.topic.name} not found for material.")

    # 3. Migrate Match Quiz to ActivityQuestion
    print("Migrating Match Quizzes...")
    for old_mq in OldMatchQuiz.objects.all():
        try:
            target_topic = NewTopic.objects.get(title=old_mq.topic.name)
            items = []
            answer = {}
            for i, pair in enumerate(old_mq.pairs.all()):
                items.append({"id": i, "label": pair.left_item, "image": pair.left_image.url if pair.left_image else None})
                items.append({"id": f"{i}_r", "label": pair.right_item, "image": pair.right_image.url if pair.right_image else None})
                answer[str(i)] = f"{i}_r"
            
            NewActivity.objects.create(
                topic=target_topic,
                question_type='tap_match',
                question_text=old_mq.title,
                items=items,
                answer=answer,
                explanation=old_mq.description,
                order=0
            )
            print(f"  Created Activity for: {target_topic.title}")
        except NewTopic.DoesNotExist:
            print(f"  Warning: Target topic {old_mq.topic.name} not found for match quiz.")

    # 4. Migrate MCQ Questions
    print("Migrating MCQ Questions...")
    for old_q in OldQuestion.objects.all():
        try:
            topic_name = old_q.topic.name if old_q.topic else old_q.section.name
            target_topic = NewTopic.objects.get(title=topic_name)
            
            # Create a quiz container for these questions if not exists
            quiz, _ = NewQuiz.objects.get_or_create(
                title=f"{target_topic.title} Assessment",
                topic=target_topic,
                created_by=admin_user,
                source='admin'
            )
            
            choices = list(old_q.choice_set.all())
            if len(choices) >= 4:
                correct_idx = [i for i, c in enumerate(choices) if c.is_correct]
                correct_char = chr(65 + correct_idx[0]) if correct_idx else 'A'
                
                NewMCQ.objects.create(
                    quiz=quiz,
                    question_text=old_q.question_text,
                    option_a=choices[0].choice_text,
                    option_b=choices[1].choice_text,
                    option_c=choices[2].choice_text,
                    option_d=choices[3].choice_text,
                    correct_option=correct_char
                )
                print(f"  Created MCQ for Quiz: {quiz.title}")
        except Exception as e:
            print(f"  Error migrating question {old_q.id}: {e}")

    print("Data migration complete!")

if __name__ == "__main__":
    migrate_data()
