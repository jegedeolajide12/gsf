from operator import is_
from turtle import mode
from venv import create
from django.db import models

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

# MY MANAGERS
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class WorkersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_worker=True)
#MY MANGERS END 



class HomePageBanner(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLISHED = 'published', 'Pulished (Visible to everyone)'
        WORKERS = 'workers', 'Workers Only'
        DRAFT = 'draft', 'Draft (Not visible to anyone)'
    class ActionChoices(models.TextChoices):
        LEARN_MORE = 'learn_more', 'Learn More'
        SIGN_UP = 'sign_up', 'Sign Up'
        FILL_FORM = 'fill_form', 'Fill Form'
        CONTACT_US = 'contact_us', 'Contact Us'
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

    def __str__(self):
        return f"{self.title} - {self.description}"

class HomePageHero(models.Model):
    image = models.ImageField(upload_to='hero/images/')
    description = models.TextField()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Home Page Heroes"
        ordering = ['-id']

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

