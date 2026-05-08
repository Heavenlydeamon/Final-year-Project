from mainapp.models import Teacher

def teacher_mode(request):
    """
    Context processor to add 'dashboard_mode' to all templates for teachers.
    - 'basic': For LP (Lower Primary) and UP (Upper Primary)
    - 'advanced': For HS (High School) and HSS (Higher Secondary)
    """
    if request.user.is_authenticated:
        # Check if user has a teacher profile
        if hasattr(request.user, 'teacher'):
            teacher = request.user.teacher
            is_lower = teacher.class_level in ['LP', 'UP']
            return {
                'dashboard_mode': 'basic' if is_lower else 'advanced',
                'is_lower_class_teacher': is_lower
            }
    return {}
