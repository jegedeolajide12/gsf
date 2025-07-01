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

class Sermon(models.Model):
    class ServiceType(models.TextChoices):
        SUNDAY_SERVICE = 'SS', 'Sunday Service'
        BIBLE_STUDY_SERVICE = 'BS', 'Bible Study Service'
        SPECIAL_EVENT = 'SE', 'Special Event'
        
    sermon_file = models.FileField(upload_to='sermons/%Y/%m/%d/')
    preacher = models.CharField(max_length=100, blank=True, null=True)
    date_preached = models.DateField(blank=True, null=True)
    sermon_type = models.CharField(
        max_length=2,
        choices=ServiceType.choices,
        default=ServiceType.SUNDAY_SERVICE,
    )
    bible_reference = models.CharField(max_length=255, blank=True, null=True)
    bible_text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sermon_series = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_preached']

    def __str__(self):
        return f"{self.title} by {self.preacher} on {self.date_preached.strftime('%Y-%m-%d') if self.date_preached else 'Unknown Date'}"
