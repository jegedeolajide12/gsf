from turtle import mode
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class HomePageHero(models.Model):
    image = models.ImageField(upload_to='hero/images/')
    description = models.TextField()

    def __str__(self):
        return self.description

class HomePageBanner(models.Model):
    image = models.ImageField(upload_to='banner/images')
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.description}"

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
    description = models.TextField()
    mission = models.TextField()
    coordinator = models.OneToOneField( User, on_delete=models.CASCADE, related_name='unit_coordinator', null=True, blank=True)
    assistant_coordinator = models.OneToOneField(User, on_delete=models.CASCADE, related_name='unit_assistant_coordinator', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='unit_members', blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Units"
        ordering = ['name']

