from .models import Unit

def user_unit_url(request):
    user_unit = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile:
            user_units = request.user.profile.units.all()
            if user_units:
                user_unit = user_units[0]
        return {
            'user_unit': user_unit
        }
    return {}