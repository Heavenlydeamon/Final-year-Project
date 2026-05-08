import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from gamification.models import ChallengeSession
from quiz.models import QuizAttempt, Quiz, MCQQuestion

@login_required
def find_challenge_opponent(request):
    try:
        my_points = request.user.userprofile.points
    except:
        my_points = 0
        
    # find potential human students
    candidates = User.objects.filter(
        userprofile__role='student',
        userprofile__student_class__is_lower_class=False,
        userprofile__points__gte=max(0, my_points-20),
        userprofile__points__lte=my_points+20
    ).exclude(id=request.user.id).distinct()
    
    opponent = None
    # For a "Ghost Race" experience, we favor the bot unless both users are in a lobby
    # So we keep opponent as None to trigger the Ghost fallback below
    is_ghost = True 
    
    # Base filter for "General Content" quizzes suitable for challenges
    # Must be admin-created, not assigned to a class, and have at least 8 questions
    challenge_quizzes = Quiz.objects.filter(
        source='admin', 
        assigned_class=None, 
        is_challenge_eligible=True
    ).annotate(q_count=models.Count('questions')).filter(q_count__gte=8)

    # Pool all admin quizzes that are challenge-eligible and have at least 8 questions
    eligible_quizzes = Quiz.objects.filter(
        source='admin', 
        is_challenge_eligible=True
    ).annotate(q_count=models.Count('questions')).filter(q_count__gte=8)
    
    quiz = eligible_quizzes.order_by('?').first()

    if not quiz:
        # Final emergency fallback: any admin quiz (hopefully never happens now)
        quiz = Quiz.objects.filter(source='admin').order_by('?').first()

    # Determine if it's a Ghost Match
    is_ghost = (opponent is None)
    # Student-like names (peers)
    ghost_names = [
        "Arjun S.", "Meera Nair", "Rahul K.", "Anjali P.", 
        "Siddharth V.", "Lakshmi R.", "Irfan Khan", "Mary Joseph",
        "Adarsh G.", "Sneha M.", "Kiran Das", "Ammu S."
    ]
    ghost_name = random.choice(ghost_names) if is_ghost else ""
    
    # Calculate ghost accuracy: roughly matches player but with +/- 10% variance
    player_avg = QuizAttempt.objects.filter(student=request.user).aggregate(models.Avg('score'))['score__avg'] or 70
    ghost_acc = max(0.4, min(0.95, (player_avg + random.randint(-10, 10)) / 100.0))

    # create challenge session
    session = ChallengeSession.objects.create(
        player_one=request.user,
        player_two=opponent,
        quiz=quiz,
        status='active',
        is_ghost=is_ghost,
        ghost_name=ghost_name,
        ghost_accuracy=ghost_acc
    )
    
    return JsonResponse({
        'found': True, 
        'session_id': session.id, 
        'opponent': opponent.username if opponent else ghost_name,
        'is_ghost': is_ghost,
        'quiz_topic': 'Global Heritage Challenge'
    })

@login_required
def challenge_arena(request, session_id):
    session = get_object_or_404(ChallengeSession, id=session_id)
    if request.user != session.player_one and request.user != session.player_two:
        return redirect('challenge_mode')
        
    # Get exactly 10 random questions from the admin pool
    # Renamed to arena_questions to avoid shadowing/conflicts
    arena_questions = list(MCQQuestion.objects.filter(quiz__source='admin').order_by('?')[:10])
    arena_question_count = len(arena_questions)
    
    print(f"[DEBUG] Session {session_id} serving {arena_question_count} questions.")
    
    return render(request, 'gamification/challenge_arena.html', {
        'session': session,
        'quiz': session.quiz,
        'arena_questions': arena_questions,
        'arena_question_count': arena_question_count,
        'ghost_accuracy': session.ghost_accuracy,
        'opponent_name': session.player_two.username if session.player_two else session.ghost_name
    })

@login_required
def complete_challenge_session(request, session_id):
    session = get_object_or_404(ChallengeSession, id=session_id)
    
    if request.method == 'POST':
        winner_id = request.POST.get('winner_id')
        
        if winner_id == str(session.player_one.id):
            winner = session.player_one
            loser = session.player_two
        else:
            winner = session.player_two
            loser = session.player_one
            
        session.winner = winner if not session.is_ghost or winner == session.player_one else None
        session.status = 'completed'
        session.save()
        
        points_gained = 0
        if winner == request.user:
            points_gained = 5
        elif loser == request.user:
            points_gained = 1
        else:
            # Handle draw or other cases if needed
            points_gained = 3
            
        if hasattr(request.user, 'userprofile'):
            request.user.userprofile.points += points_gained
            request.user.userprofile.save(update_fields=['points'])
            
        return JsonResponse({
            'status': 'completed', 
            'winner': winner.username if winner else session.ghost_name,
            'points_gained': points_gained
        })
    return JsonResponse({'error': 'POST required'}, status=400)
