from django.shortcuts import render

# Create your views here.
def logout_confirm(request):
    context = {}
    return render(request, 'account/logout_confirm.html', context)

def publicity_dashboard(request):
    context = {}
    return render(request, 'account/admin/publicity_dashboard.html', context)

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