from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime

import accounts

from taggit.managers import TaggableManager



# Create your models here.

# MY MANAGERS
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class WorkersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(for_workers=True)
#MY MANGERS END 



class HomePageBanner(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    class ActionChoices(models.TextChoices):
        LEARN_MORE = 'learn_more', _('Learn More')
        SIGN_UP = 'sign_up', _('Sign Up')
        FILL_FORM = 'fill_form', _('Fill Form')
        CONTACT_US = 'contact_us', _('Contact Us')
    image = models.ImageField(upload_to='banner/images')
    mobile_image = models.ImageField(upload_to='banner/mobile_images', null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    event = models.CharField(max_length=250, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ActionChoices.choices, default=ActionChoices.LEARN_MORE)
    action_url = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField()
    objects = PublishedManager()
    all_objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this banner?"
    )
    is_published = models.BooleanField(default=True)
    for_workers = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Home Page Banners"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if visibility := self.visibility:
            if visibility == self.VisibilityChoices.PUBLISHED:
                self.is_published = True
                self.for_workers = False
            elif visibility == self.VisibilityChoices.WORKERS:
                self.is_published = False
                self.for_workers = True
            elif visibility == self.VisibilityChoices.DRAFT:
                self.is_published = False
                self.for_workers = False
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.start_date}-{self.end_date})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.BANNER_UPDATE,
            icon='fas fa-images'
        )
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if end_date := self.end_date:
            if end_date < datetime.date.today():
                self.is_published = False
                self.for_workers = False
                self.end_date = None
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.description}"

class HomePageHero(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='hero/images/')
    mobile_image = models.ImageField(upload_to='hero/mobile_images', null=True, blank=True)
    event = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.created_at})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.HERO_UPDATE,
            icon='fas fa-images'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.description}"

    class Meta:
        verbose_name_plural = "Home Page Heroes"
        ordering = ['-id']
    
class Announcement(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
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
    for_website = models.BooleanField(default=True)
    for_email = models.BooleanField(default=False)
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
                self.for_workers = False
            elif visibility == self.VisibilityChoices.WORKERS:
                self.is_published = False
                self.for_workers = True
            elif visibility == self.VisibilityChoices.DRAFT:
                self.is_published = False
                self.for_workers = False
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.start_date}-{self.end_date})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.ANNOUNCEMENT_PUBLISH,
            icon='fas fa-bullhorn'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-created_at']

class DriveLink(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    description = models.TextField(blank=True, null=True)
    event = models.CharField(max_length=250, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True, help_text="Date of the event related to this drive link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this drive link?"
    )
    is_published = models.BooleanField(default=True)
    for_workers = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if visibility := self.visibility:
            if visibility == self.VisibilityChoices.PUBLISHED:
                self.is_published = True
                self.for_workers = False
            elif visibility == self.VisibilityChoices.WORKERS:
                self.is_published = False
                self.for_workers = True
            elif visibility == self.VisibilityChoices.DRAFT:
                self.is_published = False
                self.for_workers = False
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.created_at})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.DRIVE_UPLOAD,
            icon='fas fa-link'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Drive Links"
        ordering = ['-created_at']

class UnitCodeOfConduct(models.Model):
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='codes_of_conduct')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Code of Conduct for {self.unit.name} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "Unit Codes of Conduct"
        ordering = ['-created_at']


class Unit(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    description = models.TextField()
    mission = models.TextField()
    coordinator = models.OneToOneField( 'accounts.CustomUser', on_delete=models.CASCADE, related_name='unit_coordinator', null=True, blank=True)
    assistant_coordinator = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='unit_assistant_coordinator', null=True, blank=True)

    def get_dashboard_url(self):
        return reverse('pages:unit_dashboard', kwargs={'unit_slug': self.slug})



    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Units"
        ordering = ['name']


class Semester(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start_year(self):
        return self.start_date.year
    @property
    def end_year(self):
        return self.end_date.year

    def __str__(self):
        if self.start_year == self.end_year:
            return f"{self.name} ({self.start_year})"
        else:
            return f"{self.name} ({self.start_year} - {self.end_year})"
    
    def save(self, *args, **kwargs):
        if not self.name:
            if self.start_year == self.end_year:
                self.name = f"Semester {self.start_year}"
            else:
                self.name = f"Semester {self.start_year} - {self.end_year}"
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.name} - ({self.start_date} to {self.end_date})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.SEMESTER_CREATE,
            icon='fas fa-calendar-alt'
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Semesters"
        ordering = ['-start_date']

class Event(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='events/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False, help_text="Is this a default event that recurs every semester?")

    def save(self, *args, **kwargs):
        if not self.semester:
            self.semester = Semester.objects.filter(start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today()).first()
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.created_at})",
            unit=Unit.objects.get(slug='publicity-unit'),
            activity_type=RecentActivity.ActivityType.EVENT_UPLOAD,
            icon='fas fa-calendar'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['created_at']

class EventOccurence(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='occurrences')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event.title} on {self.date} at {self.time}"

    class Meta:
        verbose_name_plural = "Event Occurrences"
        ordering = ['-date', '-time']
    

class UnitAnnouncement(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone, Pending approval from the General Secretary)'
        UNIT_MEMBERS = 'unit_members', 'Unit Members (Visible to only your unit members)'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    class CategoryChoices(models.TextChoices):
        GENERAL = 'general', 'General'
        EVENT = 'event', 'Event'
        NEWS = 'news', 'News'
        ALERT = 'alert', 'Alert'
        REMINDER = 'reminder', 'Reminder'
    
    unit = models.ForeignKey(Unit, related_name='unit_announcements', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='unit-announcements/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    for_website = models.BooleanField(default=True)
    for_email = models.BooleanField(default=False)
    objects = PublishedManager()
    is_approved = models.BooleanField(default=False)
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
                self.for_workers = False
            elif visibility == self.VisibilityChoices.UNIT_MEMBERS:
                self.is_published = False
                self.for_workers = True
            elif visibility == self.VisibilityChoices.DRAFT:
                self.is_published = False
                self.for_workers = False
        from accounts.models import RecentActivity
        RecentActivity.objects.create(
            title=f"{self.title} - ({self.start_date}-{self.end_date})",
            unit=Unit.objects.get(slug=f"{self.unit.slug}"),
            activity_type=RecentActivity.ActivityType.ANNOUNCEMENT_PUBLISH,
            icon='fas fa-bullhorn'
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Unit Announcements"
        ordering = ['-created_at']



#  ACADEMIC UNIT PERMISSIONS
class AcademicArticle(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='academic-articles/thumbnails/', null=True, blank=True, help_text="Thumbnail image for the article")
    tags = TaggableManager(blank=True, help_text="Tags for the article, e.g., 'Book, God, Faith'")
    content = models.TextField(help_text="Content of the article in Markdown format")
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='academic_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(null=True, blank=True, help_text="Date of publication")
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    for_workers = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this article?"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Academic Articles"
        ordering = ['-created_at']


class EducationalMaterial(models.Model):
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    file = models.FileField(upload_to='course/materials')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, related_name='materials_posted', null=True, blank=True)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at', 'title']
        verbose_name_plural = 'Educational Materials'
        verbose_name = 'Educational Material'
    
    def __str__(self):
        return f"{self.course}'s material - {self.title}"

class MotivationalWriteup(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    title = models.CharField(max_length=200)
    quote = models.TextField()
    author = models.ForeignKey('accounts.CustomUser', related_name='writeups', on_delete=models.CASCADE)
    upload_date = models.DateTimeField(null=True, blank=True, help_text="Date of upload")
    is_published = models.BooleanField(default=False)
    for_workers = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this article?"
    )

class Scholarship(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(max_length=500, help_text="Link to the scholarship application")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of the scholarship")
    eligibility_criteria = models.TextField(help_text="Eligibility criteria for the scholarship")
    deadline = models.DateTimeField(null=True, blank=True, help_text="Application deadline")
    image = models.ImageField(upload_to='scholarships/images/', null=True, blank=True, help_text="Image related to the scholarship")
    tags = TaggableManager(blank=True, help_text="Tags for the scholarship, e.g., 'Undergraduate, Scholarship, Funding'")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    for_workers = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this scholarship?"
    )

    def __str__(self):
        return self.title

class Countdown(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the countdown")
    description = models.TextField(help_text="Description of the countdown")
    target_date = models.DateField(help_text="Target date for the countdown")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.target_date}"
    
    class Meta:
        verbose_name_plural = "Countdowns"
        ordering = ['-created_at']


class Timetable(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'
    course = models.CharField(max_length=200)
    day = models.CharField(
        max_length=20,
        choices=DayChoices.choices,
        default=DayChoices.MONDAY,
        help_text='Select the day of the week for this course'
    )
    start_time = models.TimeField(null=True, blank=True, help_text='Select the tutorial starting time for this course')
    end_time = models.TimeField(null=True, blank=True, help_text='Select the tutorial starting time for this course')
    tutor = models.ForeignKey('accounts.CustomUser', related_name='timetables', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'timetables'



# BIBLE STUDY UNIT PERMISSIONS
class StudyGuides(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Published (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='study-guides/thumbnails/', null=True, blank=True, help_text="Thumbnail image for the study guide")
    tags = TaggableManager(blank=True, help_text="Tags for the study guide, e.g., 'Bible Study, Faith'")
    content = models.TextField(help_text="Content of the study guide in Markdown format")
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='study_guides')
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(null=True, blank=True, help_text="Date of publication")
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    for_workers = models.BooleanField(default=False)
    objects = PublishedManager()
    all_objects = models.Manager()
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLISHED,
        help_text="Who can see this study guide?"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Study Guides"
        ordering = ['-created_at']