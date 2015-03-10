# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('repo.views',
                       url(r'^list/$', 'list', name='list'),
                       url(r'^test/$', 'test', name='test'),
                       url(r'^smlogp/$', 'smlogp', name='smlogp'),
)

#urlpatterns += patterns('django.views.generic.simple',
#  url(r'^base/$', 'direct_to_template', {'template': 'base.html'}, name="base"),
#)

urlpatterns += patterns('',
  (r'^base/$', TemplateView.as_view(template_name="base.html")),
  (r'^predict/$', TemplateView.as_view(template_name="predict.html")),
  (r'^$', TemplateView.as_view(template_name="home.html")),
  (r'^tmp/$', TemplateView.as_view(template_name="tmp.html")),
)
