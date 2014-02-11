from django.shortcuts import render
from django.views.generic.base import TemplateView


class LandingView(TemplateView):
    template_name = 'landing.html'


def login(request):
    return render(request, 'login.html')
