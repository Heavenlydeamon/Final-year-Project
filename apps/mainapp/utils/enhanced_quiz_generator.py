"""
Enhanced AI Quiz Generator
=========================
Advanced quiz generation with Western Ghats-specific features.

Features:
- Source-to-Inference pipeline with context filtering
- Structured prompt engineering
- Entity-based questioning for landmarks
- Terminology-based distractors
- Difficulty calibration
- Cross-context fallback logic
- Validation check for placeholders
"""

import logging
import random
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from mainapp.utils.content_filter import (
    ContentFilter, 
    filter_content_for_quiz,
    extract_western_ghats_facts,
    ProcessedContent
)

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class QuizConfig:
    """Configuration for quiz generation"""
    num_questions: int = 10
    difficulty: str = 'mixed'  # easy, medium, analytical, mixed
    focus_on_numerical: bool = True
    use_terminology_bank: bool = True
    entity_focus: List[str] = None
    
    def __post_init__(self):
        if self.entity_focus is None:
            self.entity_focus = []


@dataclass 
class GeneratedQuizQuestion:
    """Enhanced question data structure"""
    question_text: str
    options: List[str]
    correct_answer: str
    difficulty: str
    source_fact: str = ""
    is_verified: bool = False


class PlaceholderValidationError(Exception):
    """Raised when generated content contains placeholders"""
    pass


class EnhancedQuizGenerator:
    """
    Enhanced Quiz Generator with Source-to-Inference pipeline.
    """
    
    # Western Ghats-specific landmarks
    LANDMARKS = [
        'Eravikulam National Park',
        'Silent Valley',
        'Periyar Tiger Reserve',
        'Wayanad Wildlife Sanctuary',
        'Bandipur National Park',
        'Nagarhole National Park',
        'Kudremukh National Park',
    ]
    
    # Terminology for distractor generation
    TERMINOLOGY_BANK = [
        'Gondwana', 'Rain Shadow', 'Shola', 'Montane Forest',
        'Biodiversity Hotspot', 'Endemic Species', 'Ecologically Sensitive Area',
        'Watershed', 'River Basin', 'Western Ghats', 'Sahyadri',
        'Deccan Plateau', 'Escarpment', 'Fault Line', 'Carbon Sink',
        'Eco-tourism', 'Conservation', 'Wildlife Corridor',
    ]
    
    # States for incorrect options
    INDIAN_STATES = [
        'Gujarat', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 
        'Goa', 'Andhra Pradesh', 'Telangana', 'Madhya Pradesh',
        'Rajasthan', 'Odisha', 'West Bengal', 'Assam'
    ]
    
    # Fallback categories for cross-context logic
    FALLBACK_CATEGORIES = {
        'species': ['Iron Mining', 'Deforestation', 'Urbanization', 'Industrialization'],
        'location': ['Ancient Rome', 'Amazon Rainforest', 'Himalayas', 'Sahara Desert'],
        'process': ['Time Travel', 'Teleportation', 'Telekinesis', 'Invisibility'],
        'geography': ['Pacific Ocean', 'Atlantic Ocean', 'Arctic Circle', 'Mount Everest'],
    }
    
    def __init__(self, model=None, tokenizer=None):
        self.model = model
        self.tokenizer = tokenizer
        self.content_filter = None
        self.processed_content = None
    
    def generate_quiz(
        self, 
        content: str, 
        config: QuizConfig = None,
        use_content_filter: bool = True
    ) -> List[GeneratedQuizQuestion]:
        """Generate quiz questions from content."""
        if config is None:
            config = QuizConfig()
        
        # Step 1: Process content with filters
        if use_content_filter:
            self.content_filter = ContentFilter(content)
            self.processed_content = self.content_filter.process()
            generation_text = self.processed_content.clean_text
        else:
            generation_text = content
            self.processed_content = None
        
        # Step 2: Generate questions
        if config.difficulty == 'mixed':
            questions = self._generate_mixed_difficulty(generation_text, config)
        else:
            questions = self._generate_by_difficulty(generation_text, config)
        
        # Step 3: Validate and filter questions
        validated_questions = []
        for q in questions:
            if self._validate_question(q):
                validated_questions.append(q)
        
        # Step 4: Apply cross-context fallback if needed
        if len(validated_questions) < config.num_questions:
            needed = config.num_questions - len(validated_questions)
            fallback_questions = self._generate_fallback_questions(generation_text, needed, config)
            validated_questions.extend(fallback_questions)
        
        return validated_questions[:config.num_questions]
    
    def _generate_mixed_difficulty(self, text: str, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate questions with mixed difficulty levels."""
        questions = []
        
        num_easy = max(1, int(config.num_questions * 0.3))
        num_medium = max(1, int(config.num_questions * 0.4))
        num_analytical = config.num_questions - num_easy - num_medium
        
        easy_config = QuizConfig(num_questions=num_easy, difficulty='easy', focus_on_numerical=config.focus_on_numerical)
        questions.extend(self._generate_by_difficulty(text, easy_config))
        
        medium_config = QuizConfig(num_questions=num_medium, difficulty='medium', focus_on_numerical=config.focus_on_numerical)
        questions.extend(self._generate_by_difficulty(text, medium_config))
        
        analytical_config = QuizConfig(num_questions=num_analytical, difficulty='analytical', focus_on_numerical=config.focus_on_numerical)
        questions.extend(self._generate_by_difficulty(text, analytical_config))
        
        return questions
    
    def _generate_by_difficulty(self, text: str, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate questions for specific difficulty level."""
        if config.difficulty == 'easy':
            return self._generate_easy_questions(text, config)
        elif config.difficulty == 'medium':
            return self._generate_medium_questions(text, config)
        elif config.difficulty == 'analytical':
            return self._generate_analytical_questions(text, config)
        else:
            return self._generate_mixed_difficulty(text, config)
    
    def _generate_easy_questions(self, text: str, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate easy (identification) questions."""
        questions = []
        
        if self.processed_content and config.use_terminology_bank:
            terminology = self.processed_content.terminology
            
            for term_data in terminology[:config.num_questions]:
                term = term_data.get('term', '')
                definition = term_data.get('definition', '')
                
                if not term or not definition:
                    continue
                
                question_text = f"What is '{term}'?"
                correct_answer = definition
                distractors = self._generate_terminology_distractors(term, self.TERMINOLOGY_BANK)
                
                options = [correct_answer] + distractors
                while len(options) < 4:
                    options.append("Not defined in the text")
                options = options[:4]
                random.shuffle(options)
                
                questions.append(GeneratedQuizQuestion(
                    question_text=question_text,
                    options=options,
                    correct_answer=correct_answer,
                    difficulty='easy',
                    source_fact=f"Term: {term}",
                    is_verified=False
                ))
        
        if config.focus_on_numerical and self.processed_content:
            numerical_facts = self.processed_content.numerical_facts
            
            for fact in numerical_facts[:config.num_questions]:
                if fact['type'] in ['distance', 'height', 'age', 'area']:
                    question_text = f"What is the {fact['type']} mentioned in the text?"
                    correct_answer = fact['value']
                    distractors = self._generate_numerical_distractors(fact['value'])
                    
                    options = [correct_answer] + distractors
                    options = options[:4]
                    random.shuffle(options)
                    
                    questions.append(GeneratedQuizQuestion(
                        question_text=question_text,
                        options=options,
                        correct_answer=correct_answer,
                        difficulty='easy',
                        source_fact=fact['value'],
                        is_verified=False
                    ))
        
        return questions[:config.num_questions]
    
    def _generate_medium_questions(self, text: str, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate medium (understanding) questions."""
        questions = []
        
        if self.processed_content:
            entities = self.processed_content.entities
            
            for landmark in entities[:config.num_questions]:
                context = self._find_entity_context(text, landmark)
                
                if context:
                    question_text = f"Which of the following best describes {landmark}?"
                    correct_answer = context[:100]
                    distractors = self._generate_entity_distractors(landmark)
                    
                    options = [correct_answer] + distractors
                    options = options[:4]
                    random.shuffle(options)
                    
                    questions.append(GeneratedQuizQuestion(
                        question_text=question_text,
                        options=options,
                        correct_answer=correct_answer,
                        difficulty='medium',
                        source_fact=f"Landmark: {landmark}",
                        is_verified=False
                    ))
        
        return questions[:config.num_questions]
    
    def _generate_analytical_questions(self, text: str, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate analytical (hard) questions."""
        questions = []
        
        if self.processed_content:
            landmarks = self.processed_content.landmarks
            entities = self.processed_content.entities
            all_subjects = landmarks + entities
            
            for subject in all_subjects[:config.num_questions]:
                context = self._find_entity_context(text, subject)
                
                if context:
                    question_text = f"Analyze the significance of {subject} in the context of the Western Ghats:"
                    correct_answer = context[:100]
                    distractors = self._generate_definition_distractors(subject)
                    
                    options = [correct_answer] + distractors
                    options = options[:4]
                    random.shuffle(options)
                    
                    questions.append(GeneratedQuizQuestion(
                        question_text=question_text,
                        options=options,
                        correct_answer=correct_answer,
                        difficulty='hard',
                        source_fact=f"Analysis: {subject}",
                        is_verified=False
                    ))
        
        return questions[:config.num_questions]
    
    def _generate_terminology_distractors(self, correct_term: str, terminology_bank: List[str]) -> List[str]:
        """Generate distractors from terminology bank."""
        distractors = []
        available_terms = [t for t in terminology_bank if t.lower() != correct_term.lower()]
        random.shuffle(available_terms)
        distractors = available_terms[:3]
        
        while len(distractors) < 3:
            distractors.append("An unrelated geographical term")
        
        return distractors[:3]
    
    def _generate_numerical_distractors(self, correct_value: str) -> List[str]:
        """Generate numerical distractors."""
        distractors = []
        
        import re
        numbers = re.findall(r'\d+(?:,\d+)?(?:\.\d+)?', correct_value)
        
        if numbers:
            try:
                num = float(numbers[0].replace(',', ''))
                variations = [num * 0.5, num * 2, num * 0.75, num * 1.5, num * 10]
                
                for var in variations:
                    if var < 1000:
                        distractor = f"{int(var)}"
                    elif var < 1000000:
                        distractor = f"{int(var/1000)}K"
                    else:
                        distractor = f"{int(var/1000000)}M"
                    
                    if distractor != correct_value:
                        distractors.append(distractor)
            except:
                pass
        
        while len(distractors) < 3:
            distractors.append("Not specified in the text")
        
        return distractors[:3]
    
    def _generate_entity_distractors(self, correct_entity: str) -> List[str]:
        """Generate distractors using entity types."""
        distractors = []
        available_states = [s for s in self.INDIAN_STATES if s.lower() not in correct_entity.lower()]
        random.shuffle(available_states)
        distractors.extend(available_states[:2])
        
        while len(distractors) < 3:
            distractors.append("An unrelated location")
        
        return distractors[:3]
    
    def _generate_definition_distractors(self, correct_term: str) -> List[str]:
        """Generate definition-based distractors."""
        distractors = []
        other_terms = [t for t in self.TERMINOLOGY_BANK if t.lower() != correct_term.lower()]
        random.shuffle(other_terms)
        
        for term in other_terms[:3]:
            distractors.append(f"Definition of {term}")
        
        while len(distractors) < 3:
            distractors.append("An unrelated concept")
        
        return distractors[:3]
    
    def _generate_fallback_questions(self, text: str, needed: int, config: QuizConfig) -> List[GeneratedQuizQuestion]:
        """Generate fallback questions using cross-context logic."""
        questions = []
        
        category = self._detect_fallback_category(text)
        fallback_terms = self.FALLBACK_CATEGORIES.get(category, self.FALLBACK_CATEGORIES['species'])
        
        for i in range(needed):
            question_text = f"What is a related concept to the Western Ghats ecosystem?"
            correct_answer = fallback_terms[i % len(fallback_terms)]
            
            distractors = []
            other_categories = [c for c in self.FALLBACK_CATEGORIES.keys() if c != category]
            for cat in other_categories:
                distractors.extend(self.FALLBACK_CATEGORIES[cat][:1])
            
            options = [correct_answer] + distractors[:3]
            random.shuffle(options)
            
            questions.append(GeneratedQuizQuestion(
                question_text=question_text,
                options=options[:4],
                correct_answer=correct_answer,
                difficulty='medium',
                source_fact="Cross-context fallback",
                is_verified=False
            ))
        
        return questions
    
    def _detect_fallback_category(self, text: str) -> str:
        """Detect which fallback category to use."""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['species', 'animal', 'plant', 'wildlife']):
            return 'species'
        elif any(w in text_lower for w in ['location', 'place', 'park', 'reserve']):
            return 'location'
        elif any(w in text_lower for w in ['process', 'formation', 'develop']):
            return 'process'
        else:
            return 'geography'
    
    def _find_entity_context(self, text: str, entity: str) -> Optional[str]:
        """Find context text about an entity."""
        sentences = text.split('.')
        
        for sentence in sentences:
            if entity.lower() in sentence.lower():
                return sentence.strip()
        
        return None
    
    def _validate_question(self, question: GeneratedQuizQuestion) -> bool:
        """
        Validate question to ensure no placeholders.
        
        Checks for:
        - "correct", "incorrect", "placeholder" in options
        - Empty question or options
        - Very short options
        """
        # Check for placeholder words
        placeholder_words = ['correct', 'incorrect', 'placeholder', 'not defined', 'option']
        
        for option in question.options:
            option_lower = option.lower()
            
            # Check for placeholder indicators
            if any(word in option_lower for word in placeholder_words):
                # Check if it's explicitly marking wrong answers
                if 'correct' in option_lower and 'incorrect' not in option_lower:
                    continue  # Allow "not correct" type options
                logger.warning(f"Found placeholder in option: {option}")
                return False
        
        # Check question is not empty
        if not question.question_text or len(question.question_text.strip()) < 10:
            return False
        
        # Check we have enough options
        if len(question.options) < 2:
            return False
        
        # Check options are not too short
        for option in question.options:
            if len(option.strip()) < 3:
                return False
        
        return True


def generate_western_ghats_quiz(
    content: str,
    num_questions: int = 10,
    difficulty: str = 'mixed'
) -> List[Dict]:
    """
    Convenience function to generate Western Ghats quiz.
    
    Args:
        content: Study material text
        num_questions: Number of questions
        difficulty: easy, medium, analytical, mixed
        
    Returns:
        List of question dictionaries
    """
    config = QuizConfig(
        num_questions=num_questions,
        difficulty=difficulty
    )
    
    generator = EnhancedQuizGenerator()
    questions = generator.generate_quiz(content, config)
    
    return [
        {
            'question_text': q.question_text,
            'options': q.options,
            'correct_answer': q.correct_answer,
            'difficulty': q.difficulty,
            'source_fact': q.source_fact,
            'is_verified': q.is_verified
        }
        for q in questions
    ]
