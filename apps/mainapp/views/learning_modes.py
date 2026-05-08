from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from mainapp.models import Topic, StoryScene, UserProfile


def story_mode(request, topic_id):
    """
    Renders the Story Mode for a specific topic, with scene data for hybrid switching.
    """
    topic = get_object_or_404(Topic, id=topic_id)
    scenes = topic.story_scenes.all().order_by('scene_number')
    
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass

    context = {
        'topic': topic,
        'scenes': scenes,
        'profile': profile,
        'initial_mode': 'story',
    }
    return render(request, 'mainapp/comic_mode.html', context)



@login_required
def kerala_map_view(request):
    """
    Renders the interactive Kerala map explorer with gamification progress.
    """
    from mainapp.models import District, TopicProgress, UserCollectible
    
    districts = District.objects.all().select_related('topic', 'folklore_topic')
    
    district_data = []
    
    # Get user progress for map coloring
    completed_topic_ids = list(TopicProgress.objects.filter(
        user=request.user, 
        status='completed'
    ).values_list('topic_id', flat=True))
    
    # Get earned badges (UserCollectibles)
    profile = None
    if hasattr(request.user, 'userprofile'):
        profile = request.user.userprofile
        
    earned_collectibles = []
    if profile:
        earned_collectibles = UserCollectible.objects.filter(profile=profile).select_related('item__associated_topic')
    
    for index, d in enumerate(districts):
        is_completed = d.topic.id in completed_topic_ids if d.topic else False
        
        # Find if any earned collectible associates with this district's topic
        badge = None
        for uc in earned_collectibles:
            if uc.item.associated_topic_id == d.topic_id:
                badge = uc.item
                break
                
        # Calculate Y position mathematically since SVG transforms don't evaluate expressions
        y_pos = index * 80 + 40
        y_center = index * 80 + 60
                
        district_data.append({
            'district': d,
            'is_completed': is_completed,
            'badge': badge,
            'general_topic': d.topic,
            'folklore_topic': d.folklore_topic,
            'y_pos': y_pos,
            'y_center': y_center
        })
    
    return render(request, 'mainapp/kerala_map.html', {
        'district_data': district_data,
        'districts': districts # Keep for backward compatibility if needed
    })


@login_required
def district_view(request, id):
    """
    Redirects a district click to its associated topic study page.
    """
    from mainapp.models import District
    district = get_object_or_404(District, id=id)
    return redirect('topic_study', topic_id=district.topic.id)
