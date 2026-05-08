from django.utils import timezone
from mainapp.models import TopicProgress, QuizAttempt, DailyChallengeSubmission, DailyTopicChallenge

def calculate_composite_marks(user, topic):
    """
    Calculate composite marks for a student for a specific topic.
    Formula (Adjustable):
    - Theory Studied: 10 pts
    - Activity Completed: 10 pts
    - AI Quiz Best Score (Scaled to 50 pts): (score/total) * 50
    - Daily Challenge Correct (Scaled to 30 pts): 30 pts if any correct submission for this topic
    Total Potential Auto Points: 100
    """
    auto_points = 0
    
    # 1. Progress points (20% weight)
    progress, created = TopicProgress.objects.get_or_create(user=user, topic=topic)
    
    if progress.is_studied:
        auto_points += 10
    if progress.activity_completed:
        auto_points += 10
        
    # 2. Quiz points (50% weight)
    # Get the best quiz attempt for this topic
    best_quiz = QuizAttempt.objects.filter(user=user, topic=topic).order_by('-score').first()
    if best_quiz and best_quiz.total_questions > 0:
        # Scale score to 50
        quiz_points = (best_quiz.score / best_quiz.total_questions) * 50
        auto_points += quiz_points
        
    # 3. Daily Challenge points (30% weight)
    # Check if student has completed any daily challenge for this topic correctly
    # We check if there's any correctly submitted challenge linked to this topic
    has_correct_challenge = DailyChallengeSubmission.objects.filter(
        user=user, 
        challenge__topic=topic, 
        is_correct=True
    ).exists()
    
    if has_correct_challenge:
        auto_points += 30
        
    # Final total = Auto + Manual
    total = auto_points + (progress.manual_marks or 0)
    
    # Update progress model
    progress.composite_marks = round(total, 2)
    
    # Logic for Topic Completion:
    # 1. Theory Studied
    # 2. Activity Completed
    # 3. Quiz passed (at least 70%)
    passing_quiz = best_quiz and (best_quiz.score / best_quiz.total_questions >= 0.7) if best_quiz and best_quiz.total_questions > 0 else False
    
    if progress.is_studied and progress.activity_completed and passing_quiz:
        if progress.status != 'completed':
            progress.status = 'completed'
            if not progress.completed_at:
                progress.completed_at = timezone.now()
    elif progress.is_studied or progress.activity_completed or (best_quiz):
        progress.status = 'in_progress'
            
    progress.save()
    
    return progress.composite_marks
