from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from content.models import Topic
from learning_sessions.models import LowerClassSession, SessionResponse
from classes.models import Class
from django.db.models import Count

@login_required
def teacher_dashboard(request):
    # Lower Class Data
    lower_topics = Topic.objects.filter(class_level__in=['lower', 'both'], is_published=True)
    recent_sessions = LowerClassSession.objects.filter(teacher=request.user).order_by('-started_at')[:5]
    
    # Higher Class Data
    lower_classes = Class.objects.filter(teacher=request.user, is_lower_class=True)
    higher_classes = Class.objects.filter(teacher=request.user, is_lower_class=False)
    
    # Mastery Trends Aggregation
    topic_stats = []
    # Only for topics the teacher has taught (referenced in sessions)
    taught_topic_ids = LowerClassSession.objects.filter(teacher=request.user).values_list('topic_id', flat=True).distinct()
    taught_topics = Topic.objects.filter(id__in=taught_topic_ids)

    for topic in taught_topics:
        # Get all responses for this topic's activities across all sessions of this teacher
        responses = SessionResponse.objects.filter(
            session__teacher=request.user,
            activity_question__topic=topic
        )
        total = responses.count()
        if total > 0:
            good = responses.filter(response_level='good').count()
            mixed = responses.filter(response_level='mixed').count()
            struggled = responses.filter(response_level='struggled').count()
            
            topic_stats.append({
                'topic': topic,
                'good_pct': round((good / total) * 100),
                'mixed_pct': round((mixed / total) * 100),
                'struggled_pct': round((struggled / total) * 100),
                'total_count': total
            })

    return render(request, 'accounts/teacher_dashboard.html', {
        'lower_topics': lower_topics,
        'recent_sessions': recent_sessions,
        'lower_classes': lower_classes,
        'higher_classes': higher_classes,
        'topic_stats': topic_stats,
    })
