from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from mainapp.models import Topic, TopicProgress, MatchQuiz, UserProfile, Enrollment
from mainapp.views.base import award_xp, check_module_completion

XP_REWARD_MATCH_PASS = 20

@login_required
def match_quiz_view(request, topic_id):
    """Activity-based drag and drop match quiz for lower class students"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Needs a student profile to save progress
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'student':
            messages.error(request, 'Only students can take activities.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')

    # Get the MatchQuiz for this topic
    match_quiz = topic.match_quizzes.first()
    
    # If no match quiz exists, fallback to standard quiz
    if not match_quiz:
        return redirect('topic_quiz', topic_id=topic_id)

    pairs = list(match_quiz.pairs.all())
    
    if request.method == 'POST':
        # Assuming Javascript handles verification and only submits if correct
        score = int(request.POST.get('score', 0))
        total = int(request.POST.get('total', len(pairs)))
        
        # Calculate percentage
        percentage = (score / total * 100) if total > 0 else 0
        
        xp_results = []
        if percentage >= 70:
            # Update TopicProgress
            progress, created = TopicProgress.objects.get_or_create(
                user=request.user,
                topic=topic,
                defaults={'status': 'completed', 'is_studied': True}
            )
            if not created and progress.status != 'completed':
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
            
            # Award XP using existing mechanism
            pass_result = award_xp(request.user, XP_REWARD_MATCH_PASS, f'Activity Mastered: {topic.name}', profile)
            if pass_result['xp_awarded'] > 0:
                xp_results.append({
                    'xp': pass_result['xp_awarded'],
                    'reason': f'Passed Knowledge Match: {topic.name}',
                    'leveled_up': pass_result.get('leveled_up', False)
                })
            
            # Check Module Completion
            module_result = check_module_completion(request.user, topic.section)
            if module_result['xp_awarded'] > 0:
                xp_results.append({
                    'xp': module_result['xp_awarded'],
                    'reason': f'Mastered Module: {topic.section.name}',
                    'leveled_up': module_result.get('leveled_up', False)
                })
        
        # Using the existing quiz_result view by faking the session payload
        request.session['last_quiz_result'] = {
            'score': score,
            'total': total,
            'percentage': percentage,
            'topic_name': topic.name,
            'attempt_id': "activity",
            'xp_results': xp_results
        }
        
        return redirect('quiz_result')

    # Randomize the matching order for the view
    import random
    left_items = [
        {'id': pair.id, 'text': pair.left_item, 'image': pair.left_image} 
        for pair in pairs
    ]
    right_items = [
        {'id': pair.id, 'text': pair.right_item, 'image': pair.right_image} 
        for pair in pairs
    ]
    random.shuffle(right_items)

    return render(request, 'quizzes/match_quiz.html', {
        'topic': topic,
        'quiz': match_quiz,
        'left_items': left_items,
        'right_items': right_items
    })
