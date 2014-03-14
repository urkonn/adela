from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from administradora.views import LandingView

urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^home/$', 'administradora.views.ProfileView', name='profile'),  #ProfileView.as_view(), name='profile'),
                       url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'landing.html'}),
                       url(r'^catalogos\.json$', TemplateView.as_view(template_name='catalogos.json', content_type='aplication/json')),
                       url(r'^cedn/catalogo\.json$', TemplateView.as_view(template_name='catalogo.json', content_type='aplication/json')),
                       )
