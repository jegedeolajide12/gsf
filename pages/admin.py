from django.contrib import admin

from pages.forms import AcademicArticleForm

from .models import (
    HomePageBanner, HomePageHero, Unit, UnitCodeOfConduct, Announcement,
    DriveLink, Event, EventOccurence,  Semester, UnitAnnouncement,
    AcademicArticle, EducationalMaterial, MotivationalWriteup
)
# Register your models here.
admin.site.register(HomePageHero)
admin.site.register(UnitCodeOfConduct)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'coordinator', 'assistant_coordinator')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('coordinator', 'assistant_coordinator')
    ordering = ('name',)

    def get_queryset(self, request):
        """Override the get_queryset method to optimize the query."""
        # Use select_related to fetch related coordinator and assistant_coordinator in a single query
        return super().get_queryset(request).select_related('coordinator', 'assistant_coordinator')


@admin.register(HomePageBanner)
class HomePageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'visibility')
    list_filter = ('visibility',)
    search_fields = ('title', 'description')
    ordering = ('-start_date',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()

@admin.register(UnitAnnouncement)
class UnitAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published', 'for_email', 'category')
    list_filter = ('is_published', 'for_email', 'category')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()



@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published', 'for_email', 'category')
    list_filter = ('is_published', 'for_email', 'category')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()

@admin.register(DriveLink)
class DriveLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published', 'for_workers', 'visibility')
    list_filter = ('is_published', 'for_workers', 'visibility')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('semester', 'title', 'location')
    list_filter = ('semester',)
    search_fields = ('title', 'description')
    ordering = ('-semester',)

@admin.register(EventOccurence)
class EventOccurenceAdmin(admin.ModelAdmin):
    list_display = ('event', 'time', 'date')
    list_filter = ('event__semester',)
    search_fields = ('event__title', 'location')
    ordering = ('-time',)


@admin.register(AcademicArticle)
class AcademicArticleAdmin(admin.ModelAdmin):
    form = AcademicArticleForm
    list_display = ('title', 'author', 'publication_date', 'visibility')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('visibility', 'publication_date')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-publication_date',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()

@admin.register(EducationalMaterial)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'user']
    list_filter = ['course', 'user', 'uploaded_at']
    ordering = ['-uploaded_at', '-updated_at']

@admin.register(MotivationalWriteup)
class WriteupAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'quote']
    list_filter = ['title', 'author', 'upload_date', 'visibility']
    ordering = ['-upload_date']

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()