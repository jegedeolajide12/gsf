from django.urls import path

from . import views

app_name="dashboard"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('testimonies/', views.testimonies, name="testimonies"),
    path('sermon/', views.upload_sermon, name="upload_sermon"),
    path('announcement/upload/', views.upload_announcements, name="upload_announcement"),
    path('hero/create/', views.create_hero, name="create_hero"),
    path('hero/update/<int:hero_id>/', views.update_hero, name="update_hero"),
    path('drive/upload/', views.upload_drive, name="upload_drive"),
]
