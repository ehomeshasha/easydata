from __future__ import unicode_literals
from django.conf.urls import patterns, url

from article.views import article_view, article_list, chapter_list


urlpatterns = patterns('',
    #url(r"^programming_collective_intelligence/(?P<pk>\d+)/$", programming_collective_intelligence, name="programming_collective_intelligence"),
    #url(r"^hadoop_deployment/(?P<pk>\d+)/$", hadoop_deployment, name="hadoop_deployment"),
    #url(r"^mahout_basic/(?P<pk>\d+)/$", mahout_basic, name="mahout_basic"),
    url(r"^view/(?P<article_name>\w+)/(?P<chapter_name>\w+)/$", article_view, name="article_view"),
    url(r"^view/(?P<article_name>\w+)/$", article_view, name="article_view"),
    url(r"^list/(?P<article_name>\w+)/$", chapter_list, name="chapter_list"),
    url(r"^$", article_list, name="article_list"),
    
)
