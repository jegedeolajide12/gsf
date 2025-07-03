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
    units = models.ManyToManyField(Unit, related_name='user_units', null=True, blank=True)


    def __str__(self):
        return f"Profile of {self.user.username}"

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

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Sermon by {self.preacher} on {self.date_preached}"
        RecentActivity.objects.create(
            title=f"{self.title} - {self.preacher}",
            unit=Unit.objects.filter(slug__in=['publicity-unit', 'technical-unit']).first(),
            activity_type=RecentActivity.ActivityType.SERMON_UPLOAD,
            icon = 'fas fa-microphone-alt'
        )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date_preached']

    def __str__(self):
        return f"{self.title} by {self.preacher} on {self.date_preached.strftime('%Y-%m-%d') if self.date_preached else 'Unknown Date'}"

class RecentActivity(models.Model):
    class ActivityType(models.TextChoices):
        SERMON_UPLOAD = 'SERMON_UPLOAD', 'Added New Sermon'
        EVENT_UPLOAD = 'EVENT_UPLOAD', 'Added New Event'
        BANNER_UPDATE = 'BANNER_UPDATE', 'Updated the Homepage Banner'
        HERO_UPDATE = 'HERO_UPDATE', 'Updated the Homepage Hero Section'
        DRIVE_UPLOAD = 'DRIVE_UPLOAD', 'Uploaded New Photo Drive Link'
        SEMESTER_CREATE = 'SEMESTER_CREATE', 'Created New Semester'
        CALENDAR_CREATE = 'CALENDAR_CREATE', 'Created New Calendar'
        ANNOUNCEMENT_PUBLISH = 'ANNOUNCEMENT_PUBLISH', 'Published New Announcement'
        UNIT_LEAVE = 'UNIT_LEAVE', 'Unit Leave'
    title = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='recent_activities')
    icon = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.SERMON_UPLOAD,
    )


    class Meta:
        verbose_name = 'Recent Activity'
        verbose_name_plural = 'Recent Activities'
        ordering = ['-timestamp']


    def __str__(self):
        return f"{self.unit} - {self.activity_type} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"