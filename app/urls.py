from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^api$', views.api_call),
    url(r'^blog$', views.blog)
)