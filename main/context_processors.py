from main.models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': Notification.objects.filter()}
    else:
        return Notification.objects.none()

