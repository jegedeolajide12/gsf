from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import RecentActivity

from .forms import (
    SermonUploadForm, HeroCreationForm, BannerCreationForm, AnnouncementForm,
    DriveLinkForm
)

from pages.models import Unit


# Create your views here.
def logout_confirm(request):
    context = {}
    return render(request, 'account/logout_confirm.html', context)

def upload_sermon(request):
    sermon_form = SermonUploadForm(request.POST or None, request.FILES or None)
    unit = request.user.profile.units.first()
    if request.method == 'POST':
        if sermon_form.is_valid():
            print("Accepted service_type:", sermon_form.cleaned_data.get('sermon_type'))
            sermon_form.save()
            return redirect('pages:unit_dashboard', unit_slug=unit.slug) 
        else:
            
            sermon_form = SermonUploadForm(request.POST or None, request.FILES or None)
            context = {'form': sermon_form, 'errors': sermon_form.errors}
            print("Form errors:", sermon_form.errors)
            return render(request, "account/admin/publicity/upload_sermon_form.html", context)

    sermon_form = SermonUploadForm()
    context = {'form': sermon_form}
    return render(request, "account/admin/publicity/upload_sermon_form.html", context)

def upload_heroes(request):
    unit = request.user.profile.units.first()
    form = HeroCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('pages:unit_dashboard', unit_slug=unit.slug)
        else:
            form = HeroCreationForm(request.POST or None, request.FILES or None)
            context = {'form': form, 'errors': form.errors}
            return render(request, "account/admin/publicity/upload_hero.html", context)
    form = HeroCreationForm()
    context = {'form': form}
    return render(request, "account/admin/publicity/upload_hero.html", context)

def upload_banners(request):
    form = BannerCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('accounts:publicity_dashboard')
        else:
            form = BannerCreationForm(request.POST or None, request.FILES or None)
            context = {'form': form, 'errors': form.errors}
            return render(request, "account/admin/publicity/upload_banner.html", context)
    form = BannerCreationForm()
    context = {'form': form}
    return render(request, "account/admin/publicity/upload_banner.html", context)

def upload_announcements(request):
    form = AnnouncementForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('accounts:publicity_dashboard')
        else:
            form = AnnouncementForm(request.POST or None, request.FILES or None)
            context = {'form': form, 'errors': form.errors}
            return render(request, "account/admin/publicity/upload_announcement_form.html", context)
    form = AnnouncementForm()
    context = {'form': form}
    return render(request, "account/admin/publicity/upload_announcement_form.html", context)

def upload_photo_drives(request):
    form = DriveLinkForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('accounts:publicity_dashboard')
        else:
            form = DriveLinkForm(request.POST or None, request.FILES or None)
            context = {'form': form, 'errors': form.errors}
            return render(request, "account/admin/publicity/upload_photo_drives.html", context)
    form = DriveLinkForm()
    context = {'form': form}
    return render(request, "account/admin/publicity/upload_photo_drives.html", context)

def create_semester_calendar(request):
    context = {}
    return render(request, "account/admin/publicity/create_semester_calendar.html", context)

def assign_workers(request):
    context = {}
    return render(request, 'account/admin/publicity/assign_workers.html', context)


def gen_sec_dashboard(request):
    context = {}
    return render(request, 'account/admin/gen_sec_dashboard.html', context)

def workers_sec_dashboard(request):
    context = {}
    return render(request, 'account/admin/workers_sec_dashboard.html', context)

