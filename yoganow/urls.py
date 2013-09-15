from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.index', name='home'),
    # url(r'^api$', views.api_call)
    # url(r'^/', include('app.urls')),
    url(r'^$', 'app.views.index'),
    url(r'^api$', 'app.views.api_call'),
    url(r'^blog$', 'app.views.blog'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
