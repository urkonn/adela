from django.views.generic.base import TemplateView

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Inventory
from .forms import InventoryForm


class LandingView(TemplateView):
    template_name = 'landing.html'


@login_required
def ProfileView(request):
    return render(request, 'home.html')


def upload(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance = Inventory(data_admin=instance.user, data_file=request.FILES['data_file'])
            instance.save()
            return HttpResponseRedirect('/success/')
    else:
        form = InventoryForm()
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))


class SuccessView(TemplateView):
    template_name = 'success.html'

