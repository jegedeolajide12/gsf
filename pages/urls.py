from django.urls import path

from . import views

from accounts.views import logout_confirm


app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path('units/', views.units, name='units'),
    path('unit/<slug:unit_slug>/announcement/', views.create_unit_announcements, name="create_unit_announcements"),
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


    # Academic Unit URLs
    path('academic-articles/create/', views.create_academic_article, name='create_academic_article'),
    path('course/materials/upload', views.upload_materials, name="upload_material"),
    path('academic-articles/writeups/create/', views.post_writeup, name='create_motivational_writeup'),
    path('scholarships/create/', views.upload_scholarship, name='upload_scholarship'),
    path('academic-unit/countdown/create/', views.create_countdown, name='create_countdown'),
    path('academic-unit/countdown/update/<int:countdown_id>/', views.update_countdown, name='update_countdown'),
]
