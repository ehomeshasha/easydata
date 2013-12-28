'''
Created on Dec 19, 2013

@author: hadoop-user
'''
from django.conf.urls import patterns, url
from datafinder import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<cate_id>.*)/{0,1}$', views.list, name='list'),
    url(r'^(?P<data_id>\d+)/$', views.detail, name='detail'),
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # ex: /polls/5/results/
    #url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
