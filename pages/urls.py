from django.urls import path

from .views import (
                    home, units, sermons, events, 
                    unit_dashboard, about_page
                )

from accounts.views import logout_confirm


app_name = 'pages'

urlpatterns = [
    path("", home, name="home"),
    path('units/', units, name='units'),
    path('unit/<slug:unit_slug>/dashboard/', unit_dashboard, name='unit_dashboard'),
    path('sermons/', sermons, name='sermons'),
    path('events/', events, name="events"),
    path('logout/confirm/', logout_confirm, name="confirm_logout"),
    path('about/', about_page, name='about_page'),
]
