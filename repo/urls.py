# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('repo.views',
                       url(r'^submit/$', 'submit', name='submit'),
                       url(r'^test/$', 'test', name='test'),
                       url(r'^(?i)smlogp/$', 'smlogp', name='smlogp'),
                       url(r'^(?i)smlogs/$', 'smlogs', name='smlogs'),
                       url(r'^(?i)smNCI60/$', 'smNCI60', name='smNCI60'),
                       url(r'^datasets/$', 'datasets', name='datasets'),
                       url(r'^predict/$', 'predict', name='predict'),
)

urlpatterns += patterns('',
  url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
  url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
  url(r'^contact/$', TemplateView.as_view(template_name="contact.html"), name='contact'),
  url(r'^submitinfo/$', TemplateView.as_view(template_name="submitinfo.html"), name='submitinfo'),
)
