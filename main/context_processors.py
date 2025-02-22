from main.models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': Notification.objects.filter(user=request.user).order_by('-created_at')[:5]}
    else:
        return Notification.objects.none()

