from django.contrib import admin

from .models import HomePageBanner, HomePageHero, Unit, UnitCodeOfConduct

# Register your models here.
admin.site.register(HomePageBanner)
admin.site.register(HomePageHero)
admin.site.register(Unit)
admin.site.register(UnitCodeOfConduct)
