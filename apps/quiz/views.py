from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils.ai_generator import AIQuizGenerator
from content.models import Topic
from .models import Quiz, MCQQuestion, QuizAttempt
from django.http import JsonResponse


def resolve_content_topic_id(raw_topic_id):
    """
    The study page URL uses mainapp.Topic IDs, but Quiz FK points to
    content.Topic. This helper returns the correct content.Topic ID
    by first trying a direct match, then bridging via topic name.
    """
    # Direct match (works if already a content.Topic id)
    if Topic.objects.filter(id=raw_topic_id).exists():
        return raw_topic_id

    # Bridge: find the mainapp.Topic name, then look up content.Topic by title
    try:
        from mainapp.models import Topic as MainTopic
        mt = MainTopic.objects.get(id=raw_topic_id)
        ct = Topic.objects.get(title=mt.name)
        return ct.id
    except Exception:
        return raw_topic_id  # fall back; query will return 0 results gracefully

@login_required
def generate_quiz_view(request):
    topics = Topic.objects.filter(is_published=True)
    
    if request.method == "POST":
        topic_id = request.POST.get('topic')
        text_content = request.POST.get('content')
        num_q = int(request.POST.get('num_questions', 5))
        
        quiz = AIQuizGenerator.generate_quiz(
            topic_id=topic_id,
            text=text_content,
            num_questions=num_q,
            user=request.user
        )
        
        if quiz:
            return redirect('accounts_teacher_dashboard')
            
    return render(request, 'quiz/generate_quiz.html', {'topics': topics})

@login_required
def take_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    if request.method == "POST":
        score = 0
        user_answers = {}
        for q in questions:
            selected = request.POST.get(f'q_{q.id}')
            user_answers[str(q.id)] = selected
            if selected == q.correct_option:
                score += 1
        
        final_score = (score / questions.count()) * 100 if questions.count() > 0 else 0
        from .models import QuizAttempt
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=final_score,
            answers=user_answers
        )
        
        points_earned = 0
        if hasattr(request.user, 'userprofile'):
            points_earned = request.user.userprofile.award_quiz_points(final_score)
            
        request.session[f'quiz_{quiz.id}_points'] = points_earned
        return redirect('quiz:quiz_results', quiz_id=quiz.id)
        
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz, 
        'questions': questions,
        'topic': quiz.topic
    })

@login_required
def quiz_results_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    from .models import QuizAttempt
    latest_attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).latest('attempted_at')
    points_earned = request.session.pop(f'quiz_{quiz.id}_points', 0)
    
    return render(request, 'quiz/results.html', {
        'quiz': quiz,
        'attempt': latest_attempt,
        'points_earned': points_earned,
        'new_total_points': request.user.userprofile.points if hasattr(request.user, 'userprofile') else 0,
        'topic': quiz.topic
    })

@login_required
def section_check_api(request):
    topic_id = request.GET.get('topic')
    section_id = request.GET.get('section')
    if not topic_id or not section_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Resolve mainapp.Topic id → content.Topic id
    content_topic_id = resolve_content_topic_id(int(topic_id))

    questions = MCQQuestion.objects.filter(quiz__topic_id=content_topic_id, section_tag=section_id)
    question_count = questions.count()
    has_questions = question_count > 0

    already_attempted = False
    percentage = 0

    # Try to find an attempt specific to this section
    attempt = QuizAttempt.objects.filter(
        student=request.user,
        quiz__topic_id=content_topic_id,
        attempt_metadata__section_tag=section_id,
        attempt_metadata__mini_quiz=True
    ).order_by('-attempted_at').first()

    if attempt:
        already_attempted = True
        percentage = attempt.score

    return JsonResponse({
        'has_questions': has_questions,
        'question_count': question_count,
        'already_attempted': already_attempted,
        'percentage': percentage
    })

@login_required
def mini_quiz_view(request, topic_id, section_id):
    # Resolve mainapp.Topic id → content.Topic id
    content_topic_id = resolve_content_topic_id(topic_id)

    # Use mainapp.Topic for display context (has .name used in template)
    try:
        from mainapp.models import Topic as MainTopic
        display_topic = MainTopic.objects.get(id=topic_id)
        # Ensure it has both for template compatibility
        if not hasattr(display_topic, 'title'):
            display_topic.title = display_topic.name
    except Exception:
        display_topic = get_object_or_404(Topic, id=content_topic_id)
        if not hasattr(display_topic, 'name'):
            display_topic.name = display_topic.title

    questions = MCQQuestion.objects.filter(quiz__topic_id=content_topic_id, section_tag=section_id)
    quiz = questions.first().quiz if questions.exists() else None

    if request.method == "POST":
        score = 0
        user_answers = {}
        for q in questions:
            selected = request.POST.get(f'q_{q.id}')
            user_answers[str(q.id)] = selected
            if selected == q.correct_option:
                score += 1

        final_score = (score / questions.count()) * 100 if questions.count() > 0 else 0

        points_earned = 0
        if quiz:
            QuizAttempt.objects.create(
                student=request.user,
                quiz=quiz,
                score=final_score,
                answers=user_answers,
                attempt_metadata={"section_tag": section_id, "mini_quiz": True}
            )
            
            if hasattr(request.user, 'userprofile'):
                points_earned = request.user.userprofile.award_quiz_points(final_score)

        # Show results page for the mini-quiz
        return render(request, 'quiz/results.html', {
            'score': final_score,
            'questions': questions,
            'topic': display_topic,
            'section_id': section_id,
            'is_mini_quiz': True,
            'points_earned': points_earned,
            'new_total_points': request.user.userprofile.points if hasattr(request.user, 'userprofile') else 0
        })

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'is_mini_quiz': True,
        'section_id': section_id,
        'topic': display_topic
    })

@login_required
def admin_sections_api(request):
    quiz_id = request.GET.get('quiz_id')
    if not quiz_id:
        return JsonResponse({'sections': []})
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        sections = quiz.topic.sections
        if not isinstance(sections, list):
            sections = []
        return JsonResponse({'sections': sections})
    except Quiz.DoesNotExist:
        return JsonResponse({'sections': []})
