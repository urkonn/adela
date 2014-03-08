from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from administradora.views import LandingView  #, ProfileView

urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^home/$', 'administradora.views.ProfileView', name='profile'),  #ProfileView.as_view(), name='profile'),
                       url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'landing.html'}),
                       )
