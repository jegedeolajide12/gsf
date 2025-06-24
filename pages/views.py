from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


def units(request):
    context = {}
    return render(request, "pages/units.html", context)

def sermons(request):
    context = {}
    return render(request, "pages/sermon.html", context)

def events(request):
    context = {}
    return render(request, "pages/events.html", context)

