from multiprocessing import context
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages

from .forms import SermonCreationForm, AnnouncementForm, HeroCreationForm, HomePageHero, DriveLinkForm

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

def testimonies(request):
    context = {}
    return render(request, 'dashboard/testimony_requests.html', context)

def upload_sermon(request):
    form = SermonCreationForm()
    if request.method == 'POST':
        form = SermonCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    context = {'form':form}
    return render(request, 'dashboard/uploads/sermon.html', context)



def upload_announcements(request):
    form = AnnouncementForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    form = AnnouncementForm()
    context = {'form': form}
    return render(request, "dashboard/uploads/announcement_upload.html", context)

def create_hero(request):
    hero = HomePageHero.objects.first()
    if hero:
        return redirect('dashboard:update_hero', hero_id=hero.id)
    else:
        form = HeroCreationForm()
        if request.method == 'POST':
            form = HeroCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Hero created successfully!")
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, "There was an error creating the hero. Please check the form.")
                form = HeroCreationForm(request.POST)
        context = {'form':form}
        return render(request, 'dashboard/uploads/create_hero.html', context)

def update_hero(request, hero_id):
    hero = get_object_or_404(HomePageHero, id=hero_id)
    form = HeroCreationForm(request.POST, instance=hero)
    if request.method == 'POST':
        form = HeroCreationForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            form.save()
            messages.success(request, "Hero updated successfully!")
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "There was an error updating the hero. Please check the form.")
    context = {'form': form, 'hero': hero}
    return render(request, 'dashboard/uploads/update_hero.html', context)

def upload_drive(request):
    form = DriveLinkForm()
    if request.method == 'POST':
        form = DriveLinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Drive link uploaded successfully!")
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "There was an error uploading the drive link. Please check the form.")
    context = {'form': form}
    return render(request, 'dashboard/uploads/upload_drive_link.html', context)