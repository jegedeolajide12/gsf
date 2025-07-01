from .models import Unit

def user_unit_url(request):
    user_unit = None
    if request.user.is_authenticated:
        units = Unit.objects.all()
        user_units = request.user.units.all()
        if user_units:
            user_unit = user_units[0]
        return {
            'user_unit': user_unit
        }
    return {}