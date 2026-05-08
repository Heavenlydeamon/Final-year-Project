from django.core.management.base import BaseCommand
from quiz.models import MCQQuestion, Quiz
from content.models import Topic as ContentTopic


class Command(BaseCommand):
    help = 'Debug section quiz trigger for a topic URL'

    def add_arguments(self, parser):
        parser.add_argument('topic_id', type=int, help='Topic ID from the browser URL')
        parser.add_argument('--section', default='intro', help='Section ID to test')

    def handle(self, *args, **options):
        topic_id = options['topic_id']
        section_id = options['section']

        self.stdout.write(f'\n=== DEBUG: topic_id={topic_id}, section={section_id} ===\n')

        # 1. Check content.Topic
        self.stdout.write('-- content.Topic --')
        try:
            ct = ContentTopic.objects.get(id=topic_id)
            self.stdout.write(f'  Found: {ct.title} | category={ct.category}')
            self.stdout.write(f'  sections={ct.sections}')
        except ContentTopic.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'  NOT FOUND in content.Topic!'))

        # 2. Check mainapp.Topic
        self.stdout.write('-- mainapp.Topic --')
        try:
            from mainapp.models import Topic as MainTopic
            mt = MainTopic.objects.get(id=topic_id)
            self.stdout.write(f'  Found: {mt.name}')
        except Exception as e:
            self.stdout.write(f'  Error: {e}')

        # 3. Check Quiz linked to content topic
        self.stdout.write('-- Quiz.objects.filter(topic_id=topic_id) --')
        quizzes = Quiz.objects.filter(topic_id=topic_id)
        self.stdout.write(f'  Found {quizzes.count()} quiz(zes)')
        for q in quizzes:
            self.stdout.write(f'  Quiz: {q.title}')

        # 4. Check MCQQuestion with section_tag
        self.stdout.write(f'-- MCQQuestion.filter(quiz__topic_id={topic_id}, section_tag="{section_id}") --')
        qs = MCQQuestion.objects.filter(quiz__topic_id=topic_id, section_tag=section_id)
        self.stdout.write(f'  Found {qs.count()} question(s)')
        for q in qs:
            self.stdout.write(f'  [{q.section_tag}] {q.question_text[:60]}')

        # 5. Show ALL tagged questions for this topic
        self.stdout.write(f'-- ALL tagged questions for topic_id={topic_id} --')
        all_qs = MCQQuestion.objects.filter(quiz__topic_id=topic_id)
        self.stdout.write(f'  Total: {all_qs.count()}')
        for q in all_qs:
            self.stdout.write(f'  [{q.section_tag or "(none)"}] {q.question_text[:55]}')

        # 6. Show all quizzes and their topic IDs
        self.stdout.write('\n-- ALL Quizzes with topic IDs --')
        for quiz in Quiz.objects.select_related('topic').all():
            cnt = quiz.questions.exclude(section_tag='').count()
            self.stdout.write(
                f'  Quiz ID={quiz.id} topic_id={quiz.topic_id} '
                f'"{quiz.topic.title[:35]}" | tagged={cnt}/{quiz.questions.count()}'
            )
