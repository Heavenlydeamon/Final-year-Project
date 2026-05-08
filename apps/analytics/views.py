import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import StudyProgress

@login_required
@require_POST
def mark_section_read(request):
    try:
        data = json.loads(request.body)
        progress, created = StudyProgress.objects.get_or_create(
            student=request.user,
            topic_id=data['topic_id'],
            section_id=data['section_id']
        )
        return JsonResponse({'already_read': not created, 'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
