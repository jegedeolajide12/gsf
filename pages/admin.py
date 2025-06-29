from django.contrib import admin

from .models import HomePageBanner, HomePageHero, Unit, UnitCodeOfConduct, Announcement

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


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_published', 'for_email', 'category')
    list_filter = ('is_published', 'for_email', 'category')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Override the get_queryset method to use all_objects manager."""
        return self.model.all_objects.all()
