from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from administradora.views import LandingView

urlpatterns = patterns('',
                       # Examples:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', LandingView.as_view(), name='landing'),
                       url(r'^login/', 'administradora.views.login', name='login'),
                       )
