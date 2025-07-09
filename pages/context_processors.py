from enum import member
from .models import Unit

def user_has_unit(request):
    if request.user.is_authenticated:
        unit = getattr(getattr(request.user, 'profile', None), 'unit', None)
        if unit and unit.slug:
            return {'user_has_unit': True, 'unit': unit}
        return {'user_has_unit': False, 'unit': None}
    return {'user_has_unit': False, 'unit': None}