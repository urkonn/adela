from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class LandingView(TemplateView):
    template_name = 'landing.html'


@login_required
def ProfileView(request):
    return render(request, 'home.html')
