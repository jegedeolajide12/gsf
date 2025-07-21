from django.contrib import admin

# Register your models here.
from .models import Announcement, RecentActivity, Sermon, HomePageHero, DriveLink

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'visibility', 'category')
    list_filter = ('visibility', 'category', 'is_published')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        # Override to use the custom manager
        return self.model.all_objects.all()

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'sermon_type', 'uploaded_at')
    list_filter = ('sermon_type', 'date_preached')
    search_fields = ('title', 'preacher', 'bible_reference')
    ordering = ('-date_preached',)


@admin.register(RecentActivity)
class RecentActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('title',)
    ordering = ('-timestamp',)




@admin.register(HomePageHero)
class HomePageHeroAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(DriveLink)
class DriveLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at',)
    list_filter = ('title', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

