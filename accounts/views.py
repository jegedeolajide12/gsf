from multiprocessing import context
from django.shortcuts import render

# Create your views here.
def logout_confirm(request):
    context = {}
    return render(request, 'account/logout_confirm.html', context)

def publicity_dashboard(request):
    context = {}
    return render(request, 'account/admin/publicity_dashboard.html', context)


def upload_sermon(request):
    context = {}
    return render(request, "account/admin/publicity/upload_sermon_form.html", context)

def upload_banners(request):
    context = {}
    return render(request, "account/admin/publicity/upload_banner.html", context)

def upload_announcements(request):
    context = {}
    return render(request, "account/admin/publicity/upload_announcement_form.html", context)

def upload_photo_drives(request):
    context = {}
    return render(request, "account/admin/publicity/upload_photo_drives.html", context)

def technical_dashboard(request):
    context = {}
    return render(request, 'account/admin/technical_dashboard.html', context)

def bible_study_dashboard(request):
    context = {}
    return render(request, 'account/admin/bible_study_dashboard.html', context)

def kpt_dashboard(request):
    context = {}
    return render(request, 'account/admin/kpt_dashboard.html', context)


def evangelism_dashboard(request):
    context = {}
    return render(request, 'account/admin/evangelism_dashboard.html', context)



def ushering_dashboard(request):
    context = {}
    return render(request, 'account/admin/ushering_dashboard.html', context)


def prayer_dashboard(request):
    context = {}
    return render(request, 'account/admin/prayer_dashboard.html', context)

def academic_dashboard(request):
    context = {}
    return render(request, 'account/admin/academic_dashboard.html', context)

def follow_up_dashboard(request):
    context = {}
    return render(request, 'account/admin/follow_up_dashboard.html', context)

def welfare_dashboard(request):
    context = {}
    return render(request, 'account/admin/welfare_dashboard.html', context)

def drama_dashboard(request):
    context = {}
    return render(request, 'account/admin/drama_dashboard.html', context)

def gen_sec_dashboard(request):
    context = {}
    return render(request, 'account/admin/gen_sec_dashboard.html', context)

def workers_sec_dashboard(request):
    context = {}
    return render(request, 'account/admin/workers_sec_dashboard.html', context)

