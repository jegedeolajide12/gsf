from django.urls import path

from .views import (
                    HomePageView, AboutPageView, units, sermons,
                    events
                )

from accounts.views import logout_confirm


app_name = 'pages'

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('units/', units, name='units'),
    path('sermons/', sermons, name='sermons'),
    path('events/', events, name="events"),
    path('logout/confirm/', logout_confirm, name="confirm_logout")
]
