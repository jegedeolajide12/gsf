from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

from accounts.models import Sermon

from .models import Unit, HomePageHero, HomePageBanner, DriveLink, Announcement
from .forms import SemesterForm

User = get_user_model()

def home(request):
    announcements = Announcement.objects.all()
    heroes = HomePageHero.objects.all()
    banners = HomePageBanner.objects.all()
    drives = DriveLink.objects.all()
    sermons = Sermon.objects.all()
    context = {
               'announcements': announcements,
               'heroes': heroes,
               'banners': banners,
               'drives': drives,
               'sermons': sermons,
               'units': Unit.objects.all(),}
    return render(request, 'pages/home.html', context)


def about_page(request):
    context = {
        'hero': HomePageHero.objects.first(),
        'banner': HomePageBanner.objects.first(),
        'units': Unit.objects.all(),
        'user_units': request.user.units.all() if request.user.is_authenticated else None,
    }
    return render(request, "pages/about.html", context)


def units(request):
    units = Unit.objects.all()
    context = {'units':units}
    return render(request, "pages/units.html", context)

def unit_dashboard(request, unit_slug):
    try:
        unit = Unit.objects.get(slug=unit_slug)
    except Unit.DoesNotExist:
        return render(request, "404.html", status=404)

    context = {
        'unit': unit,
        'codes_of_conduct': unit.codes_of_conduct.all(),
        'coordinator': unit.coordinator,
        'assistant_coordinator': unit.assistant_coordinator,
        'user_units': request.user.units.all() if request.user.is_authenticated else None,
    }
    user_units = request.user.units.all() if request.user.is_authenticated else None
    user_unit = user_units[0] if user_units else None
    if user_unit.slug == 'academic-unit':
        return render(request, "account/admin/academic_dashboard.html", context)
    if user_unit.slug == 'bible-study-unit':
        return render(request, "account/admin/bible_study_dashboard.html", context)
    if user_unit.slug == 'choir-unit':
        return render(request, "account/admin/kpt_dashboard.html", context)
    if user_unit.slug == 'drama-unit':
        return render(request, "account/admin/drama_dashboard.html", context)
    if user_unit.slug == 'evangelism-unit':
        return render(request, "account/admin/evangelism_dashboard.html", context)
    if user_unit.slug == 'prayer-unit':
        return render(request, "account/admin/prayer_dashboard.html", context)
    if user_unit.slug == 'publicity-unit':
        return render(request, "account/admin/publicity_dashboard.html", context)
    if user_unit.slug == 'technical-unit':
        return render(request, "account/admin/technical_dashboard.html", context)
    if user_unit.slug == 'ushering-and-organizing-unit':
        return render(request, "account/admin/ushering_dashboard.html", context)
    if user_unit.slug == 'visitation-and-follow-up-unit':
        return render(request, "account/admin/follow_up_dashboard.html", context)
    if user_unit.slug == 'welfare-unit':
        return render(request, "account/admin/welfare-unit_dashboard.html", context)
    
    return render(request, "404.html", status=404)

def sermons(request):
    sermons = Sermon.objects.all()
    context = {'sermons':sermons}
    return render(request, "pages/sermon.html", context)

def events(request):
    events = Announcement.objects.all()
    context = {'events': events}
    return render(request, "pages/events.html", context)

def give(request):
    context = {}
    return render(request, "pages/give.html", context)


def create_semester(request):
    form = SemesterForm()
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'account/admin/publicity/create_semester.html')
        else:
            form = SemesterForm(request.POST)

    context = {'form': form}
    return render(request, 'account/admin/publicity/create_semester.html', context)

