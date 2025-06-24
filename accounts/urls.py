from django.urls import path

from .views import (
    publicity_dashboard, technical_dashboard, bible_study_dashboard, kpt_dashboard
)

app_name = 'accounts'

urlpatterns = [
    path('accounts/publicity-unit/dashboard/', publicity_dashboard, name="publicity_dashboard"),
    path('accounts/technical-unit/dashboard/', technical_dashboard, name="technical_dashboard"),
    path('accounts/bible-study-unit/dashboard/', bible_study_dashboard, name="bible_study_dashboard"),
    path('accounts/kpt-unit/dashboard/', kpt_dashboard, name="kpt_dashboard"),


]