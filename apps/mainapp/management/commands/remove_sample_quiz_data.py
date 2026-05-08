"""
Management command to remove sample quiz data and optionally replace with AI-generated quizzes.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from mainapp.models import (
    Question, Choice, Topic, StudyMaterial, 
    AIGeneratedQuiz, AIGeneratedQuestion, AIGeneratedChoice,
    Section
)
from mainapp.ai_quiz_generator import (
    generate_quiz_from_text, 
    QuizGenerationError, 
    InputValidationError,
    MIN_INPUT_LENGTH
)


class Command(BaseCommand):
    help = 'Remove sample quiz data (Question and Choice) and optionally replace with AI-generated quizzes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--topic-id',
            type=int,
            help='Remove quiz data for a specific topic ID only',
        )
        parser.add_argument(
            '--section-id',
            type=int,
            help='Remove quiz data for all topics in a specific section ID',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Remove ALL sample quiz data from all topics',
        )
        parser.add_argument(
            '--generate-ai',
            action='store_true',
            help='Automatically generate AI quizzes for topics with sufficient study material',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        topic_id = options.get('topic_id')
        section_id = options.get('section_id')
        all_topics = options.get('all')
        generate_ai = options.get('generate_ai')
        dry_run = options.get('dry_run')

        # Validate arguments
        if not any([topic_id, section_id, all_topics]):
            raise CommandError(
                'Please specify --topic-id, --section-id, or --all\n'
                'Usage: python manage.py remove_sample_quiz_data --all'
            )

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        # Get topics to process
        topics = self.get_topics_to_process(topic_id, section_id, all_topics)
        
        if not topics:
            self.stdout.write(self.style.WARNING('No topics found to process'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {len(topics)} topic(s) to process'))

        # Process each topic
        total_questions_deleted = 0
        total_quizzes_generated = 0

        for topic in topics:
            self.stdout.write(f'\nProcessing topic: {topic.name} (ID: {topic.id})')
            
            # Get questions for this topic
            topic_questions = Question.objects.filter(topic=topic)
            section_questions = Question.objects.filter(section=topic.section, topic__isnull=True)
            
            # Count questions to delete
            question_count = topic_questions.count() + section_questions.count()
            
            if question_count > 0:
                self.stdout.write(f'  - Found {question_count} question(s) to delete')
                
                # Always add to count (for summary in both dry-run and actual run)
                total_questions_deleted += question_count
                
                if not dry_run:
                    # Delete topic-specific questions with their choices
                    for question in topic_questions:
                        Choice.objects.filter(question=question).delete()
                    topic_questions.delete()
                    
                    # Delete section-level fallback questions
                    for question in section_questions:
                        Choice.objects.filter(question=question).delete()
                    section_questions.delete()
                    
                    self.stdout.write(self.style.SUCCESS(f'  - Deleted {question_count} question(s)'))
            else:
                self.stdout.write(f'  - No questions found for this topic')

            # Generate AI quiz if requested
            if generate_ai and not dry_run:
                ai_result = self.generate_ai_quiz_for_topic(topic)
                if ai_result:
                    total_quizzes_generated += 1

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*50))
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'Would have deleted {total_questions_deleted} question(s)'))
            if generate_ai:
                self.stdout.write(self.style.WARNING('Would have generated AI quizzes'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Total questions deleted: {total_questions_deleted}'))
            if generate_ai:
                self.stdout.write(self.style.SUCCESS(f'Total AI quizzes generated: {total_quizzes_generated}'))
            else:
                self.stdout.write(self.style.WARNING(
                    '\nNote: No AI quizzes generated. '
                    'Use --generate-ai to auto-generate quizzes from study materials.'
                ))

    def get_topics_to_process(self, topic_id, section_id, all_topics):
        """Get the topics to process based on arguments"""
        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                self.stdout.write(f'Targeting specific topic: {topic.name}')
                return [topic]
            except Topic.DoesNotExist:
                raise CommandError(f'Topic with ID {topic_id} not found')

        elif section_id:
            try:
                section = Section.objects.get(id=section_id)
                topics = list(section.topics.all())
                self.stdout.write(f'Targeting all topics in section: {section.name}')
                return topics
            except Section.DoesNotExist:
                raise CommandError(f'Section with ID {section_id} not found')

        elif all_topics:
            topics = list(Topic.objects.all())
            self.stdout.write(f'Targeting all {len(topics)} topics')
            return topics

        return []

    def generate_ai_quiz_for_topic(self, topic):
        """
        Generate an AI quiz for a topic if study material is available.
        Returns True if quiz was generated, False otherwise.
        """
        # Get the first study material for this topic
        study_material = StudyMaterial.objects.filter(topic=topic).first()
        
        if not study_material:
            self.stdout.write(f'  - No study material found, skipping AI generation')
            return False

        # Check if study material is long enough
        if len(study_material.content_text) < MIN_INPUT_LENGTH:
            self.stdout.write(
                f'  - Study material too short ({len(study_material.content_text)} chars), '
                f'minimum required: {MIN_INPUT_LENGTH}'
            )
            return False

        # Check if quiz already exists
        existing_quiz = AIGeneratedQuiz.objects.filter(
            topic=topic,
            status__in=['approved', 'pending']
        ).first()

        if existing_quiz:
            self.stdout.write(f'  - Quiz already exists (ID: {existing_quiz.id}, Status: {existing_quiz.status})')
            return False

        # Generate AI quiz
        try:
            self.stdout.write(f'  - Generating AI quiz from: {study_material.title}')
            generated_questions = generate_quiz_from_text(
                study_material.content_text, 
                num_questions=10
            )

            if not generated_questions:
                self.stdout.write(self.style.ERROR('  - No questions could be generated'))
                return False

            # Create the quiz
            with transaction.atomic():
                ai_quiz = AIGeneratedQuiz.objects.create(
                    title=f"AI Quiz - {topic.name}",
                    description=f"Auto-generated from: {study_material.title}",
                    study_material=study_material,
                    content_type='general' if topic.is_general else 'class',
                    section=topic.section,
                    topic=topic,
                    status='approved',  # Auto-approve for admin-generated
                )

                # Create questions
                for i, q_data in enumerate(generated_questions):
                    question = AIGeneratedQuestion.objects.create(
                        quiz=ai_quiz,
                        question_text=q_data['question_text'],
                        difficulty=q_data.get('difficulty', 'medium'),
                        order=i + 1
                    )

                    # Create choices
                    options = q_data.get('options', [])
                    correct_answer = q_data.get('correct_answer', '')

                    for j, option_text in enumerate(options):
                        # ISSUE 10 FIX: Normalize strings for comparison to handle whitespace differences
                        is_correct = (option_text.strip().lower() == correct_answer.strip().lower()) if correct_answer else False
                        AIGeneratedChoice.objects.create(
                            question=question,
                            choice_text=option_text,
                            is_correct=is_correct,
                            order=j + 1
                        )

            self.stdout.write(
                self.style.SUCCESS(f'  - Generated AI quiz with {len(generated_questions)} questions')
            )
            return True

        except (QuizGenerationError, InputValidationError) as e:
            self.stdout.write(self.style.ERROR(f'  - AI generation failed: {str(e)}'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  - Error: {str(e)}'))
            return False

