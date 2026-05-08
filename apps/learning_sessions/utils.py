from .models import SessionResponse

def calculate_session_stars(session):
    """
    Calculate stars (1-3) based on student response data
    
    Star thresholds:
    - 75%+ "good" responses = 3 stars
    - 50-74% "good" responses = 2 stars
    - <50% "good" responses = 1 star
    """
    
    responses = SessionResponse.objects.filter(session=session)
    
    if not responses.exists():
        return {
            'stars': 1,
            'message': 'Session completed',
            'good_percentage': 0,
            'good_count': 0,
            'total_count': 0
        }
    
    good_count = responses.filter(response_level='good').count()
    total_count = responses.count()
    good_percentage = (good_count / total_count) * 100
    
    if good_percentage >= 75:
        stars = 3
        message = "Excellent work, class! ⭐⭐⭐"
    elif good_percentage >= 50:
        stars = 2
        message = "Good job! Let's practice more. ⭐⭐"
    else:
        stars = 1
        message = "Keep trying! We'll get better. ⭐"
    
    return {
        'stars': stars,
        'message': message,
        'good_percentage': int(good_percentage),
        'good_count': good_count,
        'total_count': total_count
    }
