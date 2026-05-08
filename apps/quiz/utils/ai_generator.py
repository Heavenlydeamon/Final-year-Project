import logging
import random
import re
import requests
from django.conf import settings
from content.models import Topic
from ..models import Quiz, MCQQuestion

logger = logging.getLogger(__name__)

def generate_with_gemma(prompt):
    """
    Generates text using Gemma:2b via local Ollama instance.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["response"]
        return "Error: Ollama service returned status code " + str(response.status_code)
    except Exception as e:
        logger.error(f"Ollama/Gemma generation failed: {e}")
        return "Error generating response: " + str(e)

class AIQuizGenerator:
    """
    Logic for generating MCQs using Ollama and Python distractors.
    """
    
    @staticmethod
    def generate_quiz(topic_id, text, num_questions=5, user=None):
        topic = Topic.objects.get(id=topic_id)
        
        # 1. Generate Q&A with Gemma
        prompt = f"""
        Generate exactly {num_questions} quiz questions with correct answers based on the text below.
        Format each exactly as:
        Q: [Question]
        A: [Correct Answer]

        Text:
        {text[:4000]}
        """
        raw_output = generate_with_gemma(prompt)
        
        # 2. Parse Q&A
        qa_pairs = []
        q_blocks = re.split(r'Q:', raw_output)
        for block in q_blocks:
            if not block.strip(): continue
            ans_match = re.search(r'(?:A|Answer):\s*(.+?)(?=\n|Q:|$)', block, re.DOTALL | re.IGNORECASE)
            if ans_match:
                q_text = re.split(r'(?:A|Answer):', block, flags=re.IGNORECASE)[0].strip()
                answer = ans_match.group(1).strip()
                if q_text and answer:
                    qa_pairs.append((q_text, answer))
        
        if not qa_pairs:
            return None

        # 3. Create Quiz Object
        quiz = Quiz.objects.create(
            title=f"AI Quiz: {topic.title}",
            topic=topic,
            created_by=user,
            source='ai',
            is_challenge_eligible=True
        )

        # 4. Generate Distractors and Save Questions
        for q_text, answer in qa_pairs[:num_questions]:
            options = AIQuizGenerator._generate_options(answer)
            
            MCQQuestion.objects.create(
                quiz=quiz,
                question_text=q_text,
                option_a=options[0],
                option_b=options[1],
                option_c=options[2],
                option_d=options[3],
                correct_option=chr(65 + options.index(answer)),
                explanation=f"The correct answer is {answer}."
            )
        
        return quiz

    @staticmethod
    def _generate_options(correct_answer):
        """Python-based distractor generation."""
        # Common distractors for Kerala Heritage context
        distractors_db = {
            "Kathakali": ["Mohiniyattam", "Bharatanatyam", "Kuchipudi"],
            "Kerala": ["Tamil Nadu", "Karnataka", "Andhra Pradesh"],
            "Onam": ["Vishu", "Thiruvathira", "Deepavali"],
            "Malayalam": ["Tamil", "Telugu", "Kannada"],
            "Western Ghats": ["Eastern Ghats", "Himalayas", "Aravallis"],
        }

        options = []
        for key, value in distractors_db.items():
            if key.lower() in correct_answer.lower():
                options = value[:]
                break
        
        while len(options) < 3:
            options.append(f"Incorrect option {len(options)+1}")
        
        options = options[:3]
        options.append(correct_answer)
        random.shuffle(options)
        return options
