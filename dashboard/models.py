from encodings.punycode import T
from unicodedata import category
from django.db import models

from taggit.managers import TaggableManager

# Create your models here.

# MY MANAGERS
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)




class Sermon(models.Model):
    class ServiceType(models.TextChoices):
        SUNDAY_SERVICE = 'SS', 'Sunday Service'
        BIBLE_STUDY_SERVICE = 'BS', 'Bible Study Service'
        SPECIAL_EVENT = 'SE', 'Special Event'
        
    # sermon_file = models.FileField(upload_to='sermons/%Y/%m/%d/')
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
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Sermon by {self.preacher} on {self.date_preached}"
        RecentActivity.objects.create(
            title=f"{self.title} - {self.preacher}",
            # unit=Unit.objects.filter(slug__in=['publicity-unit', 'technical-unit']).first(),
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
        return f"{self.activity_type} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    


class Announcement(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    class CategoryChoices(models.TextChoices):
        GENERAL = 'general', 'General'
        EVENT = 'event', 'Event'
        NEWS = 'news', 'News'
        ALERT = 'alert', 'Alert'
        REMINDER = 'reminder', 'Reminder'
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcements/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # for_website = models.BooleanField(default=True)
    # for_email = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this announcement?"
    )
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.GENERAL,
        help_text="Category of the announcement"
    )

    def save(self, *args, **kwargs):
        if visibility := self.visibility:
            if visibility == self.VisibilityChoices.PUBLISHED:
                self.is_published = True
                # self.for_workers = False
            elif visibility == self.VisibilityChoices.WORKERS:
                self.is_published = False
                # self.for_workers = True
            elif visibility == self.VisibilityChoices.DRAFT:
                self.is_published = False
                # self.for_workers = False
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.start_date}-{self.end_date})",
            activity_type=RecentActivity.ActivityType.ANNOUNCEMENT_PUBLISH,
            icon='fas fa-bullhorn'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-created_at']



class HomePageHero(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='hero/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.created_at})",
            activity_type=RecentActivity.ActivityType.HERO_UPDATE,
            icon='fas fa-images'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.description}"

    class Meta:
        verbose_name_plural = "Home Page Heroes"
        ordering = ['-id']



class DriveLink(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)
    event = models.CharField(max_length=250, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True, help_text="Date of the event related to this drive link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.created_at})",
            activity_type=RecentActivity.ActivityType.DRIVE_UPLOAD,
            icon='fas fa-link'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Drive Links"
        ordering = ['-created_at']
