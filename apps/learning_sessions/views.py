from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from content.models import Topic, Story, StoryPanel
from activities.models import ActivityQuestion
from .models import LowerClassSession, SessionResponse
from mainapp.models import Class
from classes.models import ManualStudent, ManualStudentEvaluation
import csv

from .utils import calculate_session_stars

@login_required
def start_session(request, topic_id, story_id=None, class_id=None):
    # If story_id is not provided, pick the first published story for this topic
    if story_id is None:
        story = Story.objects.filter(topic_id=topic_id, status='published').first()
        if not story:
            # Fallback to any story if no published one
            story = Story.objects.filter(topic_id=topic_id).first()
            
        if not story:
            messages.error(request, "No stories available for this topic yet.")
            return redirect('teacher_dashboard')
        story_id = story.id
    else:
        story = get_object_or_404(Story, id=story_id)

    # Validate class if provided
    class_obj = None
    if class_id:
        class_obj = get_object_or_404(Class, id=class_id)

    # Create session
    session = LowerClassSession.objects.create(
        teacher=request.user,
        topic_id=topic_id,
        story_id=story_id,
        class_group=class_obj
    )
    
    # Build content sequence from story panels
    sequence = []
    for panel in story.panels.all().order_by('order'):
        sequence.append({"type": "panel", "id": panel.id})
        if panel.linked_activity:
            sequence.append({
                "type": "activity", 
                "id": panel.linked_activity.id
            })
    
    session.content_sequence = sequence
    session.save()
    
    return redirect('learning_sessions:projection_view', session_id=session.id)

@login_required
def projection_view(request, session_id):
    session = get_object_or_404(
        LowerClassSession, 
        id=session_id, 
        teacher=request.user
    )
    
    # Get current content item
    current_index = session.current_panel_index
    if current_index >= len(session.content_sequence):
        return redirect('learning_sessions:end_session', session_id=session.id)
        
    content_item = session.content_sequence[current_index]
    
    if content_item['type'] == 'panel':
        panel = StoryPanel.objects.get(id=content_item['id'])
        context = {'session': session, 'panel': panel, 'type': 'panel'}
    else:
        activity = ActivityQuestion.objects.get(id=content_item['id'])
        context = {'session': session, 'activity': activity, 'type': 'activity'}
    
    return render(request, 'learning_sessions/projection.html', context)

@require_POST
@login_required
def next_item(request, session_id):
    session = get_object_or_404(LowerClassSession, id=session_id)
    session.current_panel_index += 1
    
    if session.current_panel_index >= len(session.content_sequence):
        return redirect('learning_sessions:end_session', session_id=session.id)
    
    session.save()
    return redirect('learning_sessions:projection_view', session_id=session.id)

@csrf_exempt
@require_POST
@login_required
def record_response(request, session_id):
    data = json.loads(request.body)
    SessionResponse.objects.create(
        session_id=session_id,
        activity_question_id=data['activity_question_id'],
        response_level=data['response_level']
    )
    return JsonResponse({'success': True})

@login_required
def end_session(request, session_id):
    session = get_object_or_404(LowerClassSession, id=session_id)
    session.ended_at = timezone.now()
    
    # Calculate stars
    star_data = calculate_session_stars(session)
    session.stars_earned = star_data['stars']
    session.save()
    
    # Get response breakdown
    responses = SessionResponse.objects.filter(session=session)
    total_responses = responses.count() or 1
    
    good_count = responses.filter(response_level='good').count()
    mixed_count = responses.filter(response_level='mixed').count()
    struggled_count = responses.filter(response_level='struggled').count()
    
    response_breakdown = {
        'good': good_count,
        'mixed': mixed_count,
        'struggled': struggled_count,
        'good_pct': int((good_count / total_responses) * 100),
        'mixed_pct': int((mixed_count / total_responses) * 100),
        'struggled_pct': int((struggled_count / total_responses) * 100),
    }
    
    # Get students for evaluation if class is linked
    students = []
    if session.class_group:
        students = session.class_group.manual_students.all()

    return render(request, 'learning_sessions/summary.html', {
        'session': session,
        'star_data': star_data,
        'response_breakdown': response_breakdown,
        'students': students,
    })

@require_POST
@login_required
def submit_evaluations(request, session_id):
    session = get_object_or_404(LowerClassSession, id=session_id)
    if not session.class_group:
        messages.error(request, "No class associated with this session.")
        return redirect('teacher_dashboard')
    
    students = session.class_group.manual_students.all()
    
    for student in students:
        rating = request.POST.get(f'rating_{student.id}')
        remarks = request.POST.get(f'remarks_{student.id}', '')
        
        if rating:
            ManualStudentEvaluation.objects.create(
                student=student,
                class_group=session.class_group,
                topic=session.topic,
                rating=rating,
                remarks=remarks
            )
    
    messages.success(request, f"Evaluations for {session.class_group.name} saved successfully!")
    return redirect('teacher_dashboard')

def student_observer_view(request, session_id):
    """Placeholder or adapted observer view"""
    session = get_object_or_404(LowerClassSession, id=session_id)
    return render(request, 'learning_sessions/student_observer.html', {
        'session': session
    })

@login_required
def lower_class_analytics(request):
    """Aggregate performance data for manual students in teacher's lower classes"""
    teacher_classes = Class.objects.filter(teacher=request.user, is_lower_class=True)
    students = ManualStudent.objects.filter(class_group__in=teacher_classes)
    evaluations = ManualStudentEvaluation.objects.filter(student__in=students).select_related('student', 'topic', 'class_group')
    
    # Topic-wise aggregation
    topic_performance = {}
    for eval_obj in evaluations:
        if not eval_obj.topic: continue
        
        topic_name = eval_obj.topic.title
        if topic_name not in topic_performance:
            topic_performance[topic_name] = {'good': 0, 'mixed': 0, 'struggled': 0, 'total': 0}
        
        topic_performance[topic_name][eval_obj.rating] += 1
        topic_performance[topic_name]['total'] += 1

    # Calculate percentages and prepare insights
    insights = []
    for topic, data in topic_performance.items():
        total = data['total']
        data['good_pct'] = int((data['good'] / total) * 100) if total > 0 else 0
        data['mixed_pct'] = int((data['mixed'] / total) * 100) if total > 0 else 0
        data['struggled_pct'] = int((data['struggled'] / total) * 100) if total > 0 else 0
        
        if data['struggled_pct'] > 25:
            insights.append(f"Your class finds '{topic}' challenging. Consider spending more time on this topic.")

    # Student-wise table (Gradebook style)
    # Get all unique topics evaluated
    relevant_topics = Topic.objects.filter(id__in=evaluations.values_list('topic_id', flat=True).distinct())
    
    student_data = []
    for student in students:
        s_evals = evaluations.filter(student=student)
        topic_ratings = {}
        for t in relevant_topics:
            latest = s_evals.filter(topic=t).first() # ordered by date in model meta
            topic_ratings[t.id] = latest.rating if latest else 'N/A'
        
        student_data.append({
            'name': student.name,
            'class': student.class_group.name,
            'ratings': topic_ratings
        })

    return render(request, 'teacher/analytics.html', {
        'topic_performance': topic_performance,
        'student_data': student_data,
        'relevant_topics': relevant_topics,
        'insights': insights
    })

@login_required
def export_lower_class_data(request):
    """Export manual student evaluation data to CSV"""
    teacher_classes = Class.objects.filter(teacher=request.user, is_lower_class=True)
    evaluations = ManualStudentEvaluation.objects.filter(class_group__in=teacher_classes).select_related('student', 'topic', 'class_group')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="lower_class_analytics_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Class', 'Topic', 'Performance Rating', 'Remarks', 'Date Assigned'])
    
    for eval_obj in evaluations:
        writer.writerow([
            eval_obj.student.name,
            eval_obj.class_group.name,
            eval_obj.topic.title if eval_obj.topic else 'N/A',
            eval_obj.get_rating_display(),
            eval_obj.remarks,
            eval_obj.date_assigned.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

@login_required
def session_history(request):
    """View session history for the teacher"""
    sessions = LowerClassSession.objects.filter(teacher=request.user).order_by('-started_at')
    return render(request, 'learning_sessions/history.html', {'sessions': sessions})
