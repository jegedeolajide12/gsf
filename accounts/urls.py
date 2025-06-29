from django.urls import path

from .views import (
    publicity_dashboard, technical_dashboard, bible_study_dashboard, kpt_dashboard,
    evangelism_dashboard, ushering_dashboard, prayer_dashboard, academic_dashboard,
    follow_up_dashboard, welfare_dashboard, drama_dashboard, gen_sec_dashboard,
    workers_sec_dashboard, upload_sermon, upload_banners, upload_announcements,
    upload_photo_drives, create_semester_calendar, assign_workers, upload_heroes
)

app_name = 'accounts'

urlpatterns = [
    path('accounts/publicity-unit/dashboard/', publicity_dashboard, name="publicity_dashboard"),
    path('accounts/technical-unit/dashboard/', technical_dashboard, name="technical_dashboard"),
    path('accounts/bible-study-unit/dashboard/', bible_study_dashboard, name="bible_study_dashboard"),
    path('accounts/kpt-unit/dashboard/', kpt_dashboard, name="kpt_dashboard"),
    path('accounts/evangelism-unit/dashboard/', evangelism_dashboard, name="evangelism_dashboard"),
    path('accounts/ushering-unit/dashboard/', ushering_dashboard, name="ushering_dashboard"),
    path('accounts/prayer-unit/dashboard/', prayer_dashboard, name="prayer_dashboard"),
    path('accounts/academic-unit/dashboard/', academic_dashboard, name="academic_dashboard"),
    path('accounts/follow-up-unit/dashboard/', follow_up_dashboard, name="follow_up_dashboard"),
    path('accounts/welfare-unit/dashboard/', welfare_dashboard, name="welfare_dashboard"),
    path('accounts/drama-unit/dashboard/', drama_dashboard, name="drama_dashboard"),
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