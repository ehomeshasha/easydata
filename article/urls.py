from __future__ import unicode_literals
from django.conf.urls import patterns, url

from article.views import article_view


urlpatterns = patterns('',
    #url(r"^programming_collective_intelligence/(?P<pk>\d+)/$", programming_collective_intelligence, name="programming_collective_intelligence"),
    #url(r"^hadoop_deployment/(?P<pk>\d+)/$", hadoop_deployment, name="hadoop_deployment"),
    #url(r"^mahout_basic/(?P<pk>\d+)/$", mahout_basic, name="mahout_basic"),
    url(r"(?P<article_name>\w+)/(?P<chapter_name>\w+)/$", article_view, name="article_view")
    
)
