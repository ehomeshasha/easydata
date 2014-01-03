'''
Created on Dec 19, 2013

@author: hadoop-user
'''
from __future__ import unicode_literals
from django.conf.urls import patterns, url

from pdf.views import PDFUploadView, PDF2HTMLView, PDFListView



urlpatterns = patterns('',
    url(r"^$", PDFListView.as_view(), name="pdf_list"),
    #url(r"^upload/(?P<id>\d*)/$", UploadView.as_view(), name="pdf_upload"),
    url(r"^upload/$", PDFUploadView.as_view(), name="pdf_upload"),
    url(r"^list/$", PDFListView.as_view(), name="pdf_list"),
    url(r"^view/(?P<pk>\d+)/(?P<page_num>\d*)/$", PDF2HTMLView.as_view(), name="pdf_view"),
    #url(r"^(?P<bid>\d+)/$", DetailView.as_view(), name="blog_detail"),
    #url(r"^delete/(?P<bid>\d+)/$", DeleteView.as_view(), name="blog_delete"),
)
