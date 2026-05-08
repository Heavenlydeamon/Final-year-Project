import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoheritage.settings')
django.setup()

from content.models import Topic as CT
from mainapp.models import Topic as MT, Section, StudyMaterial
from quiz.models import Quiz, MCQQuestion

print("=" * 60)
print("CONTENT TOPICS (content.models.Topic)")
print("=" * 60)
for t in CT.objects.all().order_by('id'):
    secs = len(t.sections) if t.sections else 0
    print(f"  ID={t.id} | {t.title} | cat={t.category} | sections={secs}")

print()
print("=" * 60)
print("MAINAPP TOPICS (mainapp.models.Topic)")
print("=" * 60)
for t in MT.objects.all().order_by('id'):
    mats = StudyMaterial.objects.filter(topic=t).count()
    print(f"  ID={t.id} | {t.name} | section={t.section.name} | study_materials={mats}")

print()
print("=" * 60)
print("QUIZZES (quiz.models.Quiz)")
print("=" * 60)
for q in Quiz.objects.all().order_by('id'):
    qcount = MCQQuestion.objects.filter(quiz=q).count()
    topic_name = q.topic.title if q.topic else 'None'
    print(f"  ID={q.id} | {q.title} | questions={qcount} | topic={topic_name}")

print()
print("=" * 60)
print("TOPICS WITHOUT QUIZZES")
print("=" * 60)
quiz_topic_ids = set(Quiz.objects.values_list('topic_id', flat=True))
for t in CT.objects.all().order_by('id'):
    if t.id not in quiz_topic_ids:
        print(f"  NO QUIZ: ID={t.id} | {t.title}")
