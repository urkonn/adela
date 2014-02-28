from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from administradora.views import LandingView, SuccessView


urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^home/$', 'administradora.views.ProfileView', name='profile'),
                       url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
                       url(r'logout/$', 'django.contrib.auth.views.logout', {'template_name': 'landing.html'}),
                       url(r'upload/$', 'administradora.views.upload', name='upload'),
                       url(r'success/$', SuccessView.as_view(), name='success'),
                       )
