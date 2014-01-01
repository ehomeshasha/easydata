'''
Created on Dec 19, 2013

@author: hadoop-user
'''
from __future__ import unicode_literals
from django.conf.urls import patterns, url

from pdf_new.views import PDF2HTMLView



urlpatterns = patterns('',
    #url(r"^$", IndexView.as_view(), name="blog_index"),
    url(r"^view/(?P<id>\d+)/$", PDF2HTMLView.as_view(), name="pdf_new_detail"),
    #url(r"^(?P<bid>\d+)/$", DetailView.as_view(), name="blog_detail"),
    #url(r"^delete/(?P<bid>\d+)/$", DeleteView.as_view(), name="blog_delete"),
)
