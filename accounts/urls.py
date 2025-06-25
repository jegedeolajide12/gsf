from django.urls import path

from .views import (
    publicity_dashboard, technical_dashboard, bible_study_dashboard, kpt_dashboard,
    evangelism_dashboard, ushering_dashboard, prayer_dashboard, academic_dashboard,
    follow_up_dashboard, welfare_dashboard, drama_dashboard, gen_sec_dashboard,
    workers_sec_dashboard
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

]