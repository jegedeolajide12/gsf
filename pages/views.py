from multiprocessing import context
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from accounts.models import Sermon, RecentActivity
from .utils import create_recurring_events


from .models import Unit, HomePageHero, HomePageBanner, DriveLink, Announcement, EventOccurence, Event, Semester
from .forms import SemesterForm, EventForm, EventOccurrenceForm, UnitAnnouncementForm

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
    
    if hasattr(request.user, 'profile') and request.user.profile:
        user_units = request.user.profile.units.all()
            
    context = {
        'unit': unit,
        'codes_of_conduct': unit.codes_of_conduct.all(),
        'coordinator': unit.coordinator,
        'assistant_coordinator': unit.assistant_coordinator,
        'user_units': user_units,
    }
    user_unit = user_units[0] if user_units else None
    if user_unit.slug == 'academic-unit':
        unit = Unit.objects.get(slug='academic-unit')
        context = {'unit': unit}
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
        unit = Unit.objects.get(slug='publicity-unit')
        recent_activities = RecentActivity.objects.filter(unit=unit)
        context = {'recent_activities': recent_activities, 'unit': unit}
        return render(request, "account/admin/publicity_dashboard.html", context)
    if user_unit.slug == 'technical-unit':
        unit = Unit.objects.get(slug='technical-unit')
        context = {'unit': unit}
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
            # Create recurring events for the semester
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            create_recurring_events(start_date, end_date)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Prepare semester data for JSON response
                semester_data = {
                    'id': form.instance.id,
                    'name': form.instance.name,
                    'start_date': form.instance.start_date.strftime('%Y-%m-%d'),
                    'end_date': form.instance.end_date.strftime('%Y-%m-%d'),
                }
                return JsonResponse({'success': True, 'semester': semester_data})
            return redirect('pages:calendar_preview')
        else:
            form = SemesterForm(request.POST)

    context = {'form': form}
    return render(request, 'account/admin/publicity/create_semester.html', context)


def create_event(request):
    OccurrenceFormSet = inlineformset_factory(Event, EventOccurence, form=EventOccurrenceForm, extra=1, can_delete=True)
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        formset = OccurrenceFormSet(request.POST)
        if event_form.is_valid() and formset.is_valid():
            event = event_form.save()
            formset.instance = event
            formset.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Prepare event data for JSON response
                event_data = {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'location': event.location,
                    'image_url': event.image.url if event.image else '',
                    'occurrences': [
                        {
                            'date': occ.date.strftime('%Y-%m-%d'),
                            'time': occ.time.strftime('%H:%M:%S')
                        } for occ in event.occurrences.all()
                    ]
                }
                return JsonResponse({'success': True, 'event': event_data})
            return redirect('pages:calendar_preview')
    else:
        event_form = EventForm()
        formset = OccurrenceFormSet()
    context = {
        'event_form': event_form,
        'formset': formset,
    }
    return render(request, 'account/admin/publicity/create_event.html', context)

def event_occurrences_json(request):
    occurrences = EventOccurence.objects.select_related('event')

    data = []
    for occ in occurrences:
        data.append({
            "title": occ.event.title,
            "start": f"{occ.date}T{occ.time}",
            "id": occ.event.id,
            "url": f"/event/{occ.event.id}/"  # optional
        })
    return JsonResponse(data, safe=False)




def calendar_preview(request):
    # semesters = Semester.objects.all()
    # events = EventOccurence.objects.all()
    context = {
        
    }
    return render(request, 'account/admin/publicity/calendar_preview.html', context)

def create_unit_announcements(request, unit_slug):
    unit = get_object_or_404(Unit, slug=unit_slug)
    form = UnitAnnouncementForm()
    if request.method == 'POST':
        form = UnitAnnouncementForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.unit = unit
            new_form.save()
            
            return redirect('accounts:technical_dashboard')
        else:
            form = UnitAnnouncementForm(request.POST or None, request.FILES or None)
            context = {'form': form, 'errors': form.errors}
            return render(request, "pages/units/unit_announcement", context)
    context = {'form': form, 'unit':unit}
    return render(request, 'pages/units/unit_announcement.html', context)