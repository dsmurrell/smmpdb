# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('repo.views',
                       url(r'^submit/$', 'submit', name='submit'),
                       url(r'^test/$', 'test', name='test'),
                       url(r'^smlogp/$', 'smlogp', name='smlogp'),
)

urlpatterns += patterns('',
  url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
  url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
  url(r'^contact/$', TemplateView.as_view(template_name="contact.html"), name='contact'),
)
