from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from mainapp.models import Topic, Question, DailyTopicChallenge, DailyChallengeSubmission, UserProfile, Choice
from mainapp.utils.gamification import get_daily_challenge_for_topic, get_user_challenge_status

@login_required
def daily_challenge_view(request, topic_id):
    """
    View to display the daily challenge for a specific topic.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    challenge = get_daily_challenge_for_topic(topic)
    
    if not challenge:
        return render(request, 'daily_challenge_error.html', {
            'topic': topic,
            'error': "No questions available for this topic's daily challenge yet."
        })
    
    submission = get_user_challenge_status(request.user, challenge)
    is_expired = challenge.is_expired()
    
    context = {
        'topic': topic,
        'challenge': challenge,
        'question': challenge.question,
        'submission': submission,
        'is_expired': is_expired,
        'time_remaining': challenge.time_remaining_seconds(),
        'choices': challenge.question.choice_set.all()
    }
    
    return render(request, 'daily_challenge.html', context)

@login_required
def submit_daily_challenge(request, challenge_id):
    """
    API endpoint to submit the answer for a daily challenge.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    challenge = get_object_or_404(DailyTopicChallenge, id=challenge_id)
    
    # Check expiry
    if challenge.is_expired():
        return JsonResponse({'status': 'error', 'message': 'This challenge has expired!'}, status=400)
    
    # Check if already submitted
    if DailyChallengeSubmission.objects.filter(user=request.user, challenge=challenge).exists():
        return JsonResponse({'status': 'error', 'message': 'You have already attempted this challenge!'}, status=400)
    
    selected_choice_id = request.POST.get('choice_id')
    if not selected_choice_id:
        return JsonResponse({'status': 'error', 'message': 'No choice selected'}, status=400)
    
    try:
        choice = Choice.objects.get(id=selected_choice_id, question=challenge.question)
    except Choice.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid choice selected'}, status=400)
    
    is_correct = choice.is_correct
    
    # Create submission
    DailyChallengeSubmission.objects.create(
        user=request.user,
        challenge=challenge,
        is_correct=is_correct
    )
    
    points_earned = 0
    xp_earned = 0
    if is_correct:
        points_earned = challenge.points_bonus
        xp_earned = 20 # Bonus XP for daily challenge
        
        profile = request.user.userprofile
        profile.points += points_earned
        profile.xp += xp_earned
        profile.total_xp_earned += xp_earned
        
        # Challenge-specific tracking
        profile.challenge_points += points_earned
        from mainapp.utils.gamification import update_challenge_streak
        update_challenge_streak(profile)
        
        profile.save()
    
    correct_choice = challenge.question.choice_set.filter(is_correct=True).first()
    
    if is_correct:
        from mainapp.utils.valuation import calculate_composite_marks
        calculate_composite_marks(request.user, challenge.topic)
    
    return JsonResponse({
        'status': 'success',
        'is_correct': is_correct,
        'correct_choice_id': correct_choice.id if correct_choice else None,
        'points_earned': points_earned,
        'xp_earned': xp_earned,
        'challenge_streak': request.user.userprofile.challenge_streak,
        'message': f'Correct! +{points_earned} bonus points awarded.' if is_correct else 'Incorrect. Better luck tomorrow!'
    })
