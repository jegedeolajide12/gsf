import re
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Sermon, RecentActivity, Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'phone_number', 'address', 'date_of_birth')
    search_fields = ('user__username', 'user__email')
    list_filter = ('date_of_birth',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date_preached', 'sermon_type', 'uploaded_at')
    list_filter = ('sermon_type', 'date_preached')
    search_fields = ('title', 'preacher', 'bible_reference')

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(RecentActivity)
class RecentActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'activity_type', 'timestamp')
    list_filter = ('unit', 'activity_type', 'timestamp')
    search_fields = ('title', 'unit__name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('unit')