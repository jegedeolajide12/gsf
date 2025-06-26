from django.urls import path

from .views import (
                    home, AboutPageView, units, sermons,
                    events, unit_dashboard
                )

from accounts.views import logout_confirm


app_name = 'pages'

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('units/', units, name='units'),
    path('unit/<slug:unit_slug>/dashboard/', unit_dashboard, name='unit_dashboard'),
    path('sermons/', sermons, name='sermons'),
    path('events/', events, name="events"),
    path('logout/confirm/', logout_confirm, name="confirm_logout")
]
