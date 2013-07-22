# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('repo.views',
                       url(r'^list/$', 'list', name='list'),
                       url(r'^test/$', 'test', name='test'),
                       url(r'^smlogp/$', 'smlogp', name='smlogp'),
)

urlpatterns += patterns('django.views.generic.simple',
  url(r'^base/$', 'direct_to_template', {'template': 'base.html'}, name="base"),
)
