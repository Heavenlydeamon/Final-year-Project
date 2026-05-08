from django.shortcuts import render, get_object_or_404
from .models import Topic

def student_dashboard(request):
    # Only higher class or both
    topics = Topic.objects.filter(class_level__in=['higher', 'both'], is_published=True)
    return render(request, 'content/student_dashboard.html', {'topics': topics})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    # Get materials and quizzes for this topic
    return render(request, 'content/topic_detail.html', {'topic': topic})
