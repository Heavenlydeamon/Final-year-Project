"""
Management command to generate AI quizzes for Western Ghats sections.
Uses Source-to-Inference pipeline with content filtering.

Features:
- Strips non-factual metadata (Learning Outcomes, Summary)
- Extracts numerical facts (150M years, 1,600km, 2,695m)
- Uses terminology bank for distractors (Gondwana, Shola, Rain Shadow)
- Entity-based questioning (Eravikulam, Silent Valley)
- Cross-context fallbacks when AI fails
- Validates against placeholders
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
from mainapp.utils.content_filter import ContentFilter


class Command(BaseCommand):
    help = 'Generate AI quizzes for Western Ghats study materials using Source-to-Inference pipeline'

    def add_arguments(self, parser):
        parser.add_argument(
            '--section-id',
            type=int,
            help='Generate quizzes for a specific section ID',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without creating quizzes',
        )
        parser.add_argument(
            '--num-questions',
            type=int,
            default=10,
            help='Number of questions per quiz (default: 10)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate quizzes even if they exist',
        )

    def handle(self, *args, **options):
        section_id = options.get('section_id')
        dry_run = options.get('dry_run')
        num_questions = options.get('num_questions')
        force = options.get('force')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No quizzes will be created'))

        study_materials = self.get_study_materials(section_id)

        if not study_materials:
            self.stdout.write(self.style.WARNING('No Western Ghats study materials found'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'\nFound {len(study_materials)} study material(s) to process'
        ))

        total_generated = 0
        total_skipped = 0
        total_errors = 0

        for sm in study_materials:
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(f'Processing: {sm.title}')
            self.stdout.write(f'Topic: {sm.topic.name} | Section: {sm.topic.section.name}')
            self.stdout.write(f'Content length: {len(sm.content_text)} characters')

            # Step 1: Apply content filtering (Source-to-Inference)
            content_filter = ContentFilter(sm.content_text)
            processed = content_filter.process()
            
            self.stdout.write(f'  Numerical facts found: {len(processed.numerical_facts)}')
            self.stdout.write(f'  Terminology entries: {len(processed.terminology)}')
            self.stdout.write(f'  Entities: {len(processed.entities)}')

            # Step 2: Check content length
            if len(sm.content_text) < MIN_INPUT_LENGTH:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP: Content too short ({len(sm.content_text)} < {MIN_INPUT_LENGTH})'
                ))
                total_skipped += 1
                continue

            # Step 3: Check if quiz already exists
            existing_quiz = AIGeneratedQuiz.objects.filter(
                topic=sm.topic,
                status__in=['approved', 'pending']
            ).first()

            if existing_quiz and not force:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP: Quiz already exists (ID: {existing_quiz.id})'
                ))
                total_skipped += 1
                continue

            if existing_quiz and force:
                self.stdout.write(self.style.WARNING(
                    f'  FORCE: Deleting existing quiz (ID: {existing_quiz.id})'
                ))
                existing_quiz.delete()

            # Step 4: Generate quiz
            if dry_run:
                self.stdout.write(self.style.WARNING(f'  DRY RUN: Would generate {num_questions} questions'))
                total_generated += 1
                continue

            result = self.generate_ai_quiz(sm, num_questions, processed)
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

    def get_study_materials(self, section_id):
        """Get Western Ghats study materials based on section ID or default filters"""
        if section_id:
            try:
                section = Section.objects.get(id=section_id)
                self.stdout.write(f'Targeting specific section: {section.name}')
                topics = section.topics.all()
                return list(StudyMaterial.objects.filter(topic__in=topics))
            except Section.DoesNotExist:
                raise CommandError(f'Section with ID {section_id} not found')

        # Default: Get Western Ghats or Environment sections
        wg_sections = Section.objects.filter(name__icontains='Western Ghats')
        
        if not wg_sections.exists():
            wg_sections = Section.objects.filter(name__icontains='Environment')
        
        if not wg_sections.exists():
            wg_sections = Section.objects.filter(is_general=True)
        
        topics = Topic.objects.filter(section__in=wg_sections)
        return list(StudyMaterial.objects.filter(topic__in=topics).order_by('topic__section', 'topic', 'id'))

    def generate_ai_quiz(self, study_material, num_questions, processed_content):
        """Generate an AI quiz with content filtering and validation"""
        try:
            self.stdout.write(f'  Generating {num_questions} questions with Source-to-Inference pipeline...')

            # Use cleaned content from content filter
            text = processed_content.clean_text

            # Generate questions using AI
            generated_questions = generate_quiz_from_text(text, num_questions=num_questions)

            if not generated_questions:
                self.stdout.write(self.style.ERROR('  ERROR: No questions could be generated'))
                return False

            # Validate questions before saving
            valid_questions = []
            for q in generated_questions:
                if self.validate_question(q):
                    valid_questions.append(q)
            
            if not valid_questions:
                self.stdout.write(self.style.ERROR('  ERROR: No valid questions after validation'))
                return False

            # Create the quiz in database
            with transaction.atomic():
                ai_quiz = AIGeneratedQuiz.objects.create(
                    title=f"AI Quiz - {study_material.title}",
                    description=f"Auto-generated from: {study_material.title} using Source-to-Inference pipeline",
                    study_material=study_material,
                    content_type='general',
                    section=study_material.topic.section,
                    topic=study_material.topic,
                    status='approved',
                )

                # Create questions with is_verified=False for review workflow
                for i, q_data in enumerate(valid_questions):
                    question = AIGeneratedQuestion.objects.create(
                        quiz=ai_quiz,
                        question_text=q_data['question_text'],
                        difficulty=q_data.get('difficulty', 'medium'),
                        order=i + 1,
                        is_verified=False,
                        source_fact=q_data.get('source_fact', ''),
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
                f'  SUCCESS: Created quiz with {len(valid_questions)} questions (ID: {ai_quiz.id})'
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

    def validate_question(self, question_data):
        """Validate question to ensure it's not a placeholder"""
        # Check for placeholder words in options
        placeholder_words = ['correct', 'incorrect', 'placeholder', 'not defined', 'option']
        
        options = question_data.get('options', [])
        for option in options:
            option_lower = option.lower()
            if any(word in option_lower for word in placeholder_words):
                # Allow "not correct" type options
                if 'correct' in option_lower and 'incorrect' not in option_lower:
                    continue
                self.stdout.write(f'    WARNING: Skipping question with placeholder: {option[:30]}...')
                return False
        
        # Check question is not empty
        if not question_data.get('question_text') or len(question_data['question_text'].strip()) < 10:
            return False
        
        # Check we have enough options
        if len(options) < 2:
            return False
        
        return True
