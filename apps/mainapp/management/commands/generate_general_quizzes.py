"""
Management command to bulk generate AI quizzes for general content sections.
This command generates quizzes for all existing general study materials
(Environment, Heritage Sites, Cultural Artforms).
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from mainapp.models import (
    StudyMaterial, Section, Topic,
    AIGeneratedQuiz, AIGeneratedQuestion, AIGeneratedChoice
)
from mainapp.ai_quiz_generator import (
    generate_quiz_from_text,
    QuizGenerationError,
    InputValidationError,
    MIN_INPUT_LENGTH
)


class Command(BaseCommand):
    help = 'Bulk generate AI quizzes for all general content study materials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--section-id',
            type=int,
            help='Generate quizzes for a specific section ID only',
        )
        parser.add_argument(
            '--topic-id',
            type=int,
            help='Generate quizzes for a specific topic ID only',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without actually creating quizzes',
        )
        parser.add_argument(
            '--num-questions',
            type=int,
            default=10,
            help='Number of questions to generate per quiz (default: 10)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate quizzes even if they already exist',
        )

    def handle(self, *args, **options):
        section_id = options.get('section_id')
        topic_id = options.get('topic_id')
        dry_run = options.get('dry_run')
        num_questions = options.get('num_questions')
        force = options.get('force')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No quizzes will be created'))

        # Get study materials to process
        study_materials = self.get_study_materials_to_process(section_id, topic_id)

        if not study_materials:
            self.stdout.write(self.style.WARNING('No study materials found to process'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'\nFound {len(study_materials)} study material(s) to process'
        ))

        # Process each study material
        total_generated = 0
        total_skipped = 0
        total_errors = 0

        for sm in study_materials:
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(f'Processing: {sm.title}')
            self.stdout.write(f'Topic: {sm.topic.name} | Section: {sm.topic.section.name}')
            self.stdout.write(f'Content length: {len(sm.content_text)} characters')

            # Check content length
            if len(sm.content_text) < MIN_INPUT_LENGTH:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP: Content too short ({len(sm.content_text)} < {MIN_INPUT_LENGTH} chars)'
                ))
                total_skipped += 1
                continue

            # Check if quiz already exists
            existing_quiz = AIGeneratedQuiz.objects.filter(
                topic=sm.topic,
                status__in=['approved', 'pending']
            ).first()

            if existing_quiz and not force:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP: Quiz already exists (ID: {existing_quiz.id}, Status: {existing_quiz.status})'
                ))
                total_skipped += 1
                continue

            if existing_quiz and force:
                self.stdout.write(self.style.WARNING(
                    f'  FORCE: Deleting existing quiz (ID: {existing_quiz.id})'
                ))
                existing_quiz.delete()

            # Generate AI quiz
            if dry_run:
                self.stdout.write(self.style.WARNING(f'  DRY RUN: Would generate {num_questions} questions'))
                total_generated += 1
                continue

            result = self.generate_ai_quiz(sm, num_questions)
            if result:
                total_generated += 1
            else:
                total_errors += 1

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('SUMMARY'))
        self.stdout.write(self.style.SUCCESS('='*60))

        if dry_run:
            self.stdout.write(self.style.WARNING(f'Would have generated: {total_generated} quiz(es)'))
            self.stdout.write(self.style.WARNING(f'Would have skipped: {total_skipped}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Quizzes generated: {total_generated}'))
            self.stdout.write(self.style.WARNING(f'Quizzes skipped: {total_skipped}'))
            self.stdout.write(self.style.ERROR(f'Errors: {total_errors}'))

    def get_study_materials_to_process(self, section_id, topic_id):
        """Get study materials to process based on arguments"""
        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                self.stdout.write(f'Targeting specific topic: {topic.name}')
                return list(StudyMaterial.objects.filter(topic=topic))
            except Topic.DoesNotExist:
                raise CommandError(f'Topic with ID {topic_id} not found')

        elif section_id:
            try:
                section = Section.objects.get(id=section_id)
                self.stdout.write(f'Targeting all study materials in section: {section.name}')
                topics = section.topics.all()
                return list(StudyMaterial.objects.filter(topic__in=topics))
            except Section.DoesNotExist:
                raise CommandError(f'Section with ID {section_id} not found')

        else:
            # Default: Get all general sections
            general_sections = Section.objects.filter(is_general=True)
            self.stdout.write(f'Targeting all general sections: {general_sections.count()}')

            if not general_sections.exists():
                raise CommandError('No general sections found')

            topics = Topic.objects.filter(section__in=general_sections)
            return list(StudyMaterial.objects.filter(topic__in=topics).order_by('topic__section', 'topic', 'id'))

    def generate_ai_quiz(self, study_material, num_questions):
        """Generate an AI quiz for a study material"""
        try:
            self.stdout.write(f'  Generating {num_questions} questions...')

            # Generate questions using AI
            generated_questions = generate_quiz_from_text(
                study_material.content_text,
                num_questions=num_questions
            )

            if not generated_questions:
                self.stdout.write(self.style.ERROR('  ERROR: No questions could be generated'))
                return False

            # Create the quiz in database
            with transaction.atomic():
                ai_quiz = AIGeneratedQuiz.objects.create(
                    title=f"AI Quiz - {study_material.title}",
                    description=f"Auto-generated from: {study_material.title}",
                    study_material=study_material,
                    content_type='general',
                    section=study_material.topic.section,
                    topic=study_material.topic,
                    status='approved',  # Auto-approve for general content
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

            self.stdout.write(self.style.SUCCESS(
                f'  SUCCESS: Created quiz with {len(generated_questions)} questions (ID: {ai_quiz.id})'
            ))
            return True

        except InputValidationError as e:
            self.stdout.write(self.style.ERROR(f'  ERROR (Validation): {str(e)}'))
            return False
        except QuizGenerationError as e:
            self.stdout.write(self.style.ERROR(f'  ERROR (AI Generation): {str(e)}'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ERROR: {str(e)}'))
            return False

