'''
Created on Dec 19, 2013

@author: hadoop-user
'''
from __future__ import unicode_literals
from django.conf.urls import patterns, url

from easydata.category.views import CategoryPostView, CategoryListView, CategoryDeleteView



urlpatterns = patterns('',
    #url(r"^$", PDFListView.as_view(), name="pdf_list"),
    #url(r"^upload/(?P<id>\d*)/$", UploadView.as_view(), name="pdf_upload"),
    url(r"^new/$", CategoryPostView.as_view(), name="category_new"),
    url(r"^edit/(?P<pk>\d+)/$", CategoryPostView.as_view(), name="category_edit"),
    url(r"^delete/(?P<pk>\d+)/$", CategoryDeleteView.as_view(), name="category_delete"),
    url(r"^$", CategoryListView.as_view(), name="category_list"),
    #url(r"^(?P<bid>\d+)/$", DetailView.as_view(), name="blog_detail"),
    #url(r"^delete/(?P<bid>\d+)/$", DeleteView.as_view(), name="blog_delete"),
)
