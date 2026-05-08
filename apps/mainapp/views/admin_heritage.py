from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from content.models import Story, StoryPanel, Topic
from activities.models import ActivityQuestion
from mainapp.models import UserProfile

def heritage_manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.role not in ['admin', 'teacher']:
                return HttpResponseForbidden("You do not have permission to access this page.")
        except UserProfile.DoesNotExist:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@heritage_manager_required
def admin_manage_stories(request):
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.role == 'admin':
        stories = Story.objects.all().select_related('topic').order_by('-created_at')
    else:
        # Teachers see admin stories (admin_original) + their own stories
        from django.db.models import Q
        stories = Story.objects.filter(
            Q(story_type='admin_original') | Q(created_by=request.user)
        ).select_related('topic').order_by('-created_at')
    
    topics = Topic.objects.filter(class_level__in=['lower', 'both'])
    
    # Check which sidebar to show
    template = 'admin/heritage/manage_stories.html'
    if profile.role == 'teacher':
        template = 'teacher/heritage/manage_stories.html'
        
    return render(request, template, {
        'stories': stories,
        'topics': topics,
        'profile': profile
    })

@login_required
@heritage_manager_required
def admin_create_story(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        title = request.POST.get('title')
        tagline = request.POST.get('tagline')
        cover_image = request.FILES.get('cover_image')
        char_name = request.POST.get('character_name')
        char_age = request.POST.get('character_age')
        char_avatar = request.POST.get('character_avatar')
        char_desc = request.POST.get('character_description')
        
        story = Story.objects.create(
            topic_id=topic_id,
            title=title,
            tagline=tagline,
            cover_image=cover_image,
            character_name=char_name,
            character_age=char_age,
            character_avatar=char_avatar,
            character_description=char_desc,
            created_by=request.user,
            status='draft',
            story_type='teacher_created' if request.user.userprofile.role == 'teacher' else 'admin_original'
        )
        messages.success(request, f"Story '{title}' created successfully!")
        return redirect('admin_edit_story', story_id=story.id)
    
    return redirect('admin_manage_stories')

@login_required
@heritage_manager_required
def admin_edit_story(request, story_id):
    profile = UserProfile.objects.get(user=request.user)
    story = get_object_or_404(Story, id=story_id)
    
    # Permission check: Teachers can only edit their own
    if profile.role == 'teacher' and story.created_by != request.user:
        return HttpResponseForbidden("You can only edit your own stories.")
        
    panels = story.panels.all().order_by('order')
    
    # Teachers only see their own activities or global activities
    from django.db.models import Q
    activities = ActivityQuestion.objects.filter(Q(created_by=request.user) | Q(created_by__isnull=True))
    
    topics = Topic.objects.filter(class_level__in=['lower', 'both'])

    if request.method == 'POST':
        story.title = request.POST.get('title')
        story.tagline = request.POST.get('tagline')
        if request.FILES.get('cover_image'):
            story.cover_image = request.FILES.get('cover_image')
        story.character_name = request.POST.get('character_name')
        story.character_age = request.POST.get('character_age')
        story.character_avatar = request.POST.get('character_avatar')
        story.character_description = request.POST.get('character_description')
        story.status = request.POST.get('status', 'draft')
        story.save()
        messages.success(request, "Story updated!")
        return redirect('admin_edit_story', story_id=story.id)

    template = 'admin/heritage/edit_story.html'
    if profile.role == 'teacher':
        template = 'teacher/heritage/edit_story.html'

    return render(request, template, {
        'story': story,
        'panels': panels,
        'activities': activities,
        'topics': topics,
        'profile': profile
    })

@login_required
@heritage_manager_required
def admin_add_story_panel(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.role == 'teacher' and story.created_by != request.user:
        return HttpResponseForbidden("Permission denied.")
        
    if request.method == 'POST':
        panel_type = request.POST.get('panel_type')
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image')
        activity_id = request.POST.get('linked_activity')
        order = story.panels.count() + 1
        
        StoryPanel.objects.create(
            story=story,
            panel_type=panel_type,
            title=title,
            text=text,
            image=image,
            linked_activity_id=activity_id if activity_id else None,
            order=order
        )
        messages.success(request, "Panel added!")
    
    return redirect('admin_edit_story', story_id=story.id)

@login_required
@heritage_manager_required
def admin_delete_story_panel(request, panel_id):
    panel = get_object_or_404(StoryPanel, id=panel_id)
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.role == 'teacher' and panel.story.created_by != request.user:
        return HttpResponseForbidden("Permission denied.")
        
    story_id = panel.story.id
    panel.delete()
    messages.success(request, "Panel deleted!")
    return redirect('admin_edit_story', story_id=story_id)

@login_required
@heritage_manager_required
def admin_manage_activities(request):
    profile = UserProfile.objects.get(user=request.user)
    
    if profile.role == 'admin':
        activities = ActivityQuestion.objects.all().select_related('topic').order_by('-id')
    else:
        from django.db.models import Q
        activities = ActivityQuestion.objects.filter(
            Q(created_by__isnull=True) | Q(created_by__is_staff=True) | Q(created_by=request.user)
        ).select_related('topic').order_by('-id')
        
    topics = Topic.objects.filter(class_level__in=['lower', 'both'])
    
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        q_type = request.POST.get('question_type')
        text = request.POST.get('question_text')
        items_raw = request.POST.get('items_json', '{}')
        answer_raw = request.POST.get('answer_json', '{}')
        
        import json
        try:
            ActivityQuestion.objects.create(
                topic_id=topic_id,
                question_type=q_type,
                question_text=text,
                items=json.loads(items_raw),
                answer=json.loads(answer_raw),
                created_by=request.user
            )
            messages.success(request, "Activity created!")
        except Exception as e:
            messages.error(request, f"Error creating activity: {e}")
            
    template = 'admin/heritage/manage_activities.html'
    if profile.role == 'teacher':
        template = 'teacher/heritage/manage_activities.html'
            
    return render(request, template, {
        'activities': activities,
        'topics': topics,
        'profile': profile
    })
