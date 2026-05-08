import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mainapp.models import Story, StoryNode, StoryProgress, UserProfile
from mainapp.ai_engine import AIEngine

logger = logging.getLogger(__name__)

@login_required
def story_list(request):
    """
    Renders a list of available narrative stories.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('login')
        
    stories = Story.objects.filter(is_active=True)
    
    # Get user progress for each story
    user_progress = {sp.story_id: sp for sp in StoryProgress.objects.filter(user=request.user)}
    
    context = {
        'profile': profile,
        'stories': stories,
        'user_progress': user_progress,
    }
    return render(request, 'stories/story_list.html', context)

@login_required
def story_detail(request, story_id):
    """
    Renders the current node of a story for the user.
    """
    story = get_object_or_404(Story, id=story_id)
    progress, created = StoryProgress.objects.get_or_create(
        user=request.user, 
        story=story,
        defaults={'current_node': story.nodes.first()}
    )
    
    if created: # Fallback if first node wasn't set correctly
        if progress.current_node is None:
            progress.current_node = story.nodes.first()
            progress.save()

    current_node = progress.current_node
    
    # Check for next node
    next_node = story.nodes.filter(order__gt=current_node.order).first()
    
    context = {
        'story': story,
        'node': current_node,
        'next_node': next_node,
        'progress': progress,
    }
    return render(request, 'stories/story_detail.html', context)

@login_required
@csrf_exempt
def next_story_node(request, story_id):
    """
    Advances the user to the next story node.
    """
    story = get_object_or_404(Story, id=story_id)
    progress = get_object_or_404(StoryProgress, user=request.user, story=story)
    
    next_node = story.nodes.filter(order__gt=progress.current_node.order).first()
    if next_node:
        progress.current_node = next_node
        progress.save()
    else:
        progress.completed = True
        progress.save()
        
    return redirect('story_detail', story_id=story_id)

@login_required
@csrf_exempt
def story_companion_api(request):
    """
    AI Story Companion API.
    Handles questions about the story context.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
    story_id = request.POST.get('story_id')
    node_id = request.POST.get('node_id')
    question = request.POST.get('question')
    
    if not all([story_id, node_id, question]):
        return JsonResponse({'error': 'Missing parameters'}, status=400)
        
    story = get_object_or_404(Story, id=story_id)
    node = get_object_or_404(StoryNode, id=node_id)
    
    try:
        story_context = f"Story: {story.title}\nCurrent Chapter: {node.title}\nContent: {node.content}"
        response = AIEngine.generate_story_interaction(story_context, question)
        return JsonResponse({'success': True, 'answer': response})
    except Exception as e:
        logger.error(f"Story companion failed: {str(e)}")
        return JsonResponse({'error': 'Companion failed to respond'}, status=500)
