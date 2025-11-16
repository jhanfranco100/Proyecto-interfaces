from .models import Notificacion

def notification_count(request):
    if request.user.is_authenticated:
        count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return {'notification_count': count}
    return {'notification_count': 0}
