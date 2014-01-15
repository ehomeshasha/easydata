from __future__ import unicode_literals
from django.conf.urls import patterns, url

from article.views import programming_collective_intelligence, hadoop_deployment, mahout_basic


urlpatterns = patterns('',
    url(r"^programming_collective_intelligence/(?P<pk>\d+)/$", programming_collective_intelligence, name="programming_collective_intelligence"),
    url(r"^hadoop_deployment/(?P<pk>\d+)/$", hadoop_deployment, name="hadoop_deployment"),
    url(r"^mahout_basic/(?P<pk>\d+)/$", mahout_basic, name="mahout_basic"),
    
)
