from django.urls import path

from .views import (
    gen_sec_dashboard, workers_sec_dashboard, upload_sermon, upload_banners, 
    upload_announcements, upload_photo_drives, create_semester_calendar, assign_workers, 
    upload_heroes
)

app_name = 'accounts'

urlpatterns = [
    path('accounts/gen-sec-unit/dashboard/', gen_sec_dashboard, name="gen_sec_dashboard"),
    path('accounts/workers-sec-unit/dashboard/', workers_sec_dashboard, name="workers_sec_dashboard"),


    path('upload-sermon/', upload_sermon, name='upload_sermon'),
    path('upload-heroes/', upload_heroes, name='upload_heroes'),
    path('upload-banners/', upload_banners, name='upload_banners'),
    path('upload-announcements/', upload_announcements, name='upload_announcements'),
    path('upload-photo-drives/', upload_photo_drives, name='upload_photo_drives'),
    path('create-semester-calendar/', create_semester_calendar, name='create_semester_calendar'),
    path('assign-workers/', assign_workers, name='assign_workers'),


]