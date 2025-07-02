from django.urls import path

from . import views

from accounts.views import logout_confirm


app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path('units/', views.units, name='units'),
    path('unit/<slug:unit_slug>/dashboard/', views.unit_dashboard, name='unit_dashboard'),
    path('sermons/', views.sermons, name='sermons'),
    path('events/', views.events, name="events"),
    # path('logout/confirm/', views.logout_confirm, name="confirm_logout"),
    path('about/', views.about_page, name='about_page'),
    path('give/', views.give, name='give'),


    path('create-semester/', views.create_semester, name='create_semester'),
    path('calendar-preview/', views.calendar_preview, name='calendar_preview'),
    path('create-event/', views.create_event, name='create_event'),

    
    path('api/events/', views.event_occurrences_json, name='events_json'),

]
