from datetime import date, timedelta
import random
from django.utils import timezone

# Eco-Evolutionary Levels
LEVEL_TITLES = {
    1: "Seedling",
    3: "Sprout",
    5: "Western Ghats Scout",
    7: "Forest Guardian",
    9: "Heritage Custodian",
    11: "Eternal Protector"
}

def get_level_title(level):
    """Get the narrative title for a given level."""
    sorted_levels = sorted(LEVEL_TITLES.keys(), reverse=True)
    for l in sorted_levels:
        if level >= l:
            return LEVEL_TITLES[l]
    return LEVEL_TITLES[1]

def update_streak(profile):
    """
    Update the user's daily login streak.
    Returns True if the streak was incremented, False otherwise.
    """
    today = date.today()
    if profile.last_activity_date == today:
        return False
    
    if profile.last_activity_date == today - timedelta(days=1):
        profile.current_streak += 1
    else:
        profile.current_streak = 1
        
    if profile.current_streak > profile.max_streak:
        profile.max_streak = profile.current_streak
        
    profile.last_activity_date = today
    profile.save()
    return True

# Spirit Guide: The Nilgiri Tahr "Spirit Guide"
SPIRIT_GUIDE_MESSAGES = [
    "The mist on the Ghats reveals paths to those who persist. Keep studying, Guardian!",
    "Just as the Neelakurinji blooms in its own time, your knowledge is growing deep roots.",
    "The Malabar Squirrel is swift, but the patient Tahr sees the whole mountain. Take your time with the archives.",
    "A sprout today, a canopy tomorrow. Your XP is the sunlight of your journey.",
    "Have you explored the Folklore chronicles? Treasures of wisdom are hidden there.",
]

def get_spirit_guide_message(user, profile):
    """Return a contextual or random spirit guide message."""
    from mainapp.views.ai_recommendations import get_personalized_dashboard_data
    
    # Try to get contextual data
    try:
        data = get_personalized_dashboard_data(user)
        weak_topics = data.get('weak_topics', [])
        
        if weak_topics:
            topic_name = weak_topics[0]['topic'].name
            return f"The mountain winds whisper that you should revisit '{topic_name}'. Deepening those roots will make you a stronger Guardian."
        
        if profile.xp < 50:
            return "Welcome, Seedling. Every lesson you master is a drop of rain for your growth."
            
    except:
        pass
        
    return random.choice(SPIRIT_GUIDE_MESSAGES)

def get_rarity_color(rarity):
    """Get the hex color for a collectible rarity."""
    colors = {
        'common': '#757575',    # Muted Grey
        'rare': '#2196F3',      # Blue
        'epic': '#9C27B0',      # Purple
        'legendary': '#FF9800'  # Orange/Gold
    }
    return colors.get(rarity.lower(), '#757575')

def award_random_collectible(profile, rarity=None):
    """Award a random collectible to the user profile."""
    from mainapp.models import CollectibleItem, UserCollectible
    
    # Get items the user profile doesn't have yet
    obtained_ids = UserCollectible.objects.filter(profile=profile).values_list('item_id', flat=True)
    available_items = CollectibleItem.objects.exclude(id__in=obtained_ids)
    
    if rarity:
        available_items = available_items.filter(rarity=rarity)
        
    if not available_items.exists():
        # Fallback to any item if rarity specific not found
        available_items = CollectibleItem.objects.exclude(id__in=obtained_ids)
        
    if available_items.exists():
        new_item = random.choice(list(available_items))
        UserCollectible.objects.create(profile=profile, item=new_item)
        return new_item
    return None

def check_for_artifact_shard(profile, probability=0.3):
    """Randomly award an artifact shard to the user profile."""
    if random.random() > probability:
        return None
        
    from mainapp.models import ArtifactShard, UserArtifactShard
    obtained_ids = UserArtifactShard.objects.filter(profile=profile).values_list('shard_id', flat=True)
    available_shards = ArtifactShard.objects.exclude(id__in=obtained_ids)
    
    if available_shards.exists():
        new_shard = random.choice(list(available_shards))
        UserArtifactShard.objects.create(profile=profile, shard=new_shard)
        return new_shard
    return None


# ============================================
# HERITAGE LEAGUE — Competitive Mechanics
# ============================================

def calculate_weekly_leaderboard(league=None, limit=10):
    """
    Get the weekly leaderboard, optionally filtered by league.
    Returns a ranked list of dicts.
    """
    from mainapp.models import UserLeague
    
    qs = UserLeague.objects.select_related('profile__user', 'league').filter(
        league__isnull=False
    )
    if league:
        qs = qs.filter(league=league)
    
    qs = qs.order_by('-points_this_week')[:limit]
    
    leaderboard = []
    for rank, ul in enumerate(qs, 1):
        leaderboard.append({
            'rank': rank,
            'username': ul.profile.user.username,
            'points': ul.points_this_week,
            'level': ul.profile.level,
            'league_name': ul.league.name if ul.league else 'None',
            'profile_id': ul.profile.id,
        })
    return leaderboard


def process_league_promotions(promote_count=3, relegate_count=3):
    """
    Weekly reset: promote top players, relegate bottom players, reset points.
    - Top `promote_count` per league → next league (higher min_xp)
    - Bottom `relegate_count` per league → previous league (lower min_xp)
    - All points_this_week reset to 0
    Returns a summary dict.
    """
    from mainapp.models import League, UserLeague, LeagueNotification
    
    leagues = list(League.objects.order_by('min_xp'))
    summary = {'promotions': 0, 'relegations': 0, 'reset_count': 0}
    
    for idx, league in enumerate(leagues):
        members = UserLeague.objects.filter(league=league).order_by('-points_this_week')
        member_list = list(members)
        
        if len(member_list) < 2:
            continue  # Skip leagues with too few members
        
        # Promote top players (skip if already in highest league)
        if idx < len(leagues) - 1:
            next_league = leagues[idx + 1]
            for ul in member_list[:promote_count]:
                if ul.points_this_week > 0:  # Only promote active players
                    LeagueNotification.objects.create(
                        profile=ul.profile,
                        notification_type='promotion',
                        old_league=league,
                        new_league=next_league,
                        message=f"🎉 Promoted to {next_league.name}! Your performance earned you a spot in a higher league."
                    )
                    ul.league = next_league
                    ul.save()
                    summary['promotions'] += 1
        
        # Relegate bottom players (skip if already in lowest league)
        if idx > 0:
            prev_league = leagues[idx - 1]
            # Get bottom players (those with activity, to avoid relegating inactive)
            bottom = [m for m in member_list[-relegate_count:] if m.points_this_week >= 0]
            for ul in bottom:
                LeagueNotification.objects.create(
                    profile=ul.profile,
                    notification_type='relegation',
                    old_league=league,
                    new_league=prev_league,
                    message=f"📉 Relegated to {prev_league.name}. Earn more XP next week to reclaim your rank!"
                )
                ul.league = prev_league
                ul.save()
                summary['relegations'] += 1
    
    # Reset all weekly points
    reset = UserLeague.objects.all().update(points_this_week=0)
    summary['reset_count'] = reset
    
    return summary


def get_unread_league_notifications(profile):
    """Fetch unread league notifications for this profile."""
    from mainapp.models import LeagueNotification
    return LeagueNotification.objects.filter(profile=profile, is_read=False)


# ============================================
# DAILY TOPIC CHALLENGE LOGIC
# ============================================

def get_daily_challenge_for_topic(topic):
    """
    Get the current daily challenge for a topic, or create one if it doesn't exist.
    """
    from mainapp.models import DailyTopicChallenge, Question
    
    # First check for any active (non-expired) challenge for this topic
    active_challenge = DailyTopicChallenge.objects.filter(
        topic=topic, 
        expiry_time__gt=timezone.now()
    ).first()
    
    if active_challenge:
        return active_challenge
        
    # If no active challenge, check if one was created today already
    today = timezone.now().date()
    challenge = DailyTopicChallenge.objects.filter(topic=topic, date=today).first()
    
    if not challenge:
        # Pick a random question from this topic
        questions = Question.objects.filter(topic=topic)
        if questions.exists():
            question = random.choice(list(questions))
            challenge = DailyTopicChallenge.objects.create(
                topic=topic,
                question=question,
                expiry_time=timezone.now() + timedelta(hours=8),
                points_bonus=15
            )
    return challenge

def get_global_daily_challenges(limit=3):
    """
    Get a set of global daily challenges from different general topics.
    Refreshes every 8 hours.
    """
    from mainapp.models import DailyTopicChallenge, Topic, Question
    
    # 1. Get all currently active (non-expired) challenges from general topics
    active_challenges = list(DailyTopicChallenge.objects.filter(
        topic__is_general=True,
        expiry_time__gt=timezone.now()
    ).select_related('topic', 'topic__section'))
    
    # 2. If we have enough active ones, return them
    if len(active_challenges) >= limit:
        return random.sample(active_challenges, limit)
    
    # 3. If not enough, create new ones from general topics that don't have active challenges
    existing_topic_ids = [c.topic_id for c in active_challenges]
    available_topics = Topic.objects.filter(
        is_general=True,
        questions__isnull=False
    ).exclude(id__in=existing_topic_ids).distinct()
    
    if available_topics.exists():
        new_needed = limit - len(active_challenges)
        selected_topics = random.sample(
            list(available_topics), 
            min(new_needed, available_topics.count())
        )
        
        for topic in selected_topics:
            new_c = get_daily_challenge_for_topic(topic)
            if new_c:
                active_challenges.append(new_c)
                
    return active_challenges[:limit]

def update_challenge_streak(profile):
    """
    Update the user's daily challenge streak.
    Called when a user completes a daily challenge correctly.
    """
    today = timezone.now().date()
    
    if profile.last_challenge_date == today:
        # Already updated today
        return False
    
    if profile.last_challenge_date == today - timedelta(days=1):
        # Consecutive day
        profile.challenge_streak += 1
    else:
        # Streak broken or first time
        profile.challenge_streak = 1
        
    if profile.challenge_streak > profile.max_challenge_streak:
        profile.max_challenge_streak = profile.challenge_streak
        
    profile.last_challenge_date = today
    profile.save()
    return True

def get_challenge_leaderboard(limit=10):
    """
    Get the top players based on daily challenge points.
    """
    from mainapp.models import UserProfile
    return UserProfile.objects.filter(role='student').order_by('-challenge_points', '-challenge_streak')[:limit]

def get_user_challenge_status(user, challenge):
    """
    Check if a user has already attempted the daily challenge.
    """
    from mainapp.models import DailyChallengeSubmission
    if not challenge:
        return None
    return DailyChallengeSubmission.objects.filter(user=user, challenge=challenge).first()

def get_mode_leaderboard(challenge_type, limit=10):
    """
    Get the top players for a specific challenge mode.
    """
    from mainapp.models import ChallengeAttempt
    from django.db.models import Max, Sum
    
    # Get highest score per user for this mode
    # We want to show the top individuals
    leaderboard = ChallengeAttempt.objects.filter(
        challenge_type=challenge_type,
        is_completed=True
    ).values('user__username', 'user__id').annotate(
        max_score=Max('score'),
        total_xp=Sum('total_xp_earned')
    ).order_by('-max_score')[:limit]
    
    return leaderboard

def get_pvp_leaderboard(limit=10):
    """
    Get the top players for PvP Head-to-Head challenges based on total wins.
    """
    from django.contrib.auth.models import User
    from django.db.models import Count
    from gamification.models import ChallengeSession
    
    leaderboard = ChallengeSession.objects.filter(
        status='completed',
        winner__isnull=False
    ).values('winner__username', 'winner__id').annotate(
        wins=Count('id')
    ).order_by('-wins')[:limit]
    
    return leaderboard

def get_class_leaderboard(class_obj, type='quiz', limit=10):
    """
    Get the leaderboard for a specific class.
    type can be 'quiz' or 'challenge'.
    """
    from mainapp.models import QuizAttempt, ChallengeAttempt, UserProfile
    from django.db.models import Sum, Count
    
    if type == 'quiz':
        # Sum of scores for quiz attempts in this class
        results = QuizAttempt.objects.filter(
            class_obj=class_obj
        ).values('user__username', 'user__id').annotate(
            total_score=Sum('score'),
            attempt_count=Count('id')
        ).order_by('-total_score')[:limit]
    else:
        # Sum of scores for challenge attempts in this class
        results = ChallengeAttempt.objects.filter(
            class_obj=class_obj,
            is_completed=True
        ).values('user__username', 'user__id').annotate(
            total_score=Sum('score'),
            total_xp=Sum('total_xp_earned'),
            attempt_count=Count('id')
        ).order_by('-total_score')[:limit]
        
    return results
