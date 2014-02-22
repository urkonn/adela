from django.views.generic.base import TemplateView

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from .forms import InventoryForm


class LandingView(TemplateView):
    template_name = 'landing.html'


@login_required
def ProfileView(request):
    return render(request, 'home.html')


class UploadView(FormView):
    template_name = 'upload.html'
    form_class = InventoryForm
    success_url = '/success/'


class SuccessView(TemplateView):
    template_name = 'success.html'

