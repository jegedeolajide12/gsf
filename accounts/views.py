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