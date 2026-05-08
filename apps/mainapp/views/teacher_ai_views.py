import json
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from mainapp.ai_engine import AIEngine
from mainapp.models import UserProfile

logger = logging.getLogger(__name__)

@login_required
@require_POST
def teacher_suggest_topics_api(request):
    """
    AI-powered topic suggestions for teachers based on subject name.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role not in ['teacher', 'admin']:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
            
        subject_name = request.POST.get('subject_name')
        if not subject_name:
            return JsonResponse({'success': False, 'error': 'Subject name is required'}, status=400)
            
        prompt = f"""
        Generate a list of exactly 5 educational topics for the subject "{subject_name}" suitable for school students in Kerala. 
        Each topic should be related to Kerala's heritage, culture, or environment if possible.
        Return ONLY a comma-separated list of the 5 topic titles. No numbers, no bolding, no prefixes.
        """
        
        # Use Gemma via Ollama (fast/local)
        raw_response = AIEngine.generate_chatbot_response(
            "Topic Suggestion", 
            f"Subject: {subject_name}", 
            prompt
        )
        
        # Simple parsing for comma separated list
        topics = [t.strip() for t in raw_response.split(',') if t.strip()]
        
        # Fallback if AI output is messy
        if not topics or len(topics) < 2:
            # Try splitting by newlines
            topics = [t.strip() for t in raw_response.split('\n') if t.strip() and len(t) > 3]
            
        # Clean up any potential AI "noise" (like "1. ", "Hero: ")
        clean_topics = []
        for t in topics[:5]:
            clean_t = t.lstrip('123456789. -').strip('"')
            if clean_t:
                clean_topics.append(clean_t)

        return JsonResponse({
            'success': True,
            'topics': clean_topics
        })
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)
    except Exception as e:
        logger.error(f"Suggest topics API failed: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def teacher_generate_lesson_api(request):
    """
    AI-powered lesson content generation for teachers.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role not in ['teacher', 'admin']:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
            
        title = request.POST.get('title')
        if not title:
            return JsonResponse({'success': False, 'error': 'Title is required'}, status=400)
            
        prompt = f"""
        Write a comprehensive educational lesson about "{title}" for school students.
        Focus on Kerala's context if applicable.
        Include an introduction, three key facts, and a summary.
        The content should be approximately 300 words.
        Use clear, simple English.
        """
        
        # Generate lesson content
        generated_content = AIEngine.generate_chatbot_response(
            "Lesson Generation",
            f"Topic: {title}",
            prompt
        )
        
        if not generated_content or "Error" in generated_content:
            return JsonResponse({'success': False, 'error': 'AI Model failed to generate content or is offline.'}, status=500)

        return JsonResponse({
            'success': True,
            'generated_content': generated_content
        })
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)
    except Exception as e:
        logger.error(f"Generate lesson API failed: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
