from django.urls import path

from .views import (
    publicity_dashboard, technical_dashboard
)

app_name = 'accounts'

urlpatterns = [
    path('accounts/publicity-unit/dashboard/', publicity_dashboard, name="publicity_dashboard"),
    path('accounts/technical-unit/dashboard/', technical_dashboard, name="technical_dashboard"),
]