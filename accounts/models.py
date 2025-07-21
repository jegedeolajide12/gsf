from django.contrib.auth.models import AbstractUser
from django.db import models

from pages.models import Unit



class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def get_unit_dashboard_url(self):
        if self.units.exists():
            return self.units.first().get_dashboard_url()
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    other_units = models.ManyToManyField(Unit, blank=True, related_name='other_members')


    def __str__(self):
        return f"Profile of {self.user.username}"
