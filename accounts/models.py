from django.contrib.auth.models import AbstractUser
from django.db import models

from pages.models import Unit



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    units = models.ManyToManyField(Unit, related_name='user_units', null=True, blank=True)

    def get_unit_dashboard_url(self):
        if self.units.exists():
            return self.units.first().get_dashboard_url()
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"