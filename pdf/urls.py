from __future__ import unicode_literals
from django.conf.urls import patterns, url

from pdf.views import PDFUploadView, PDF2HTMLView, PDFListView, download_pdf, delete_pdf



urlpatterns = patterns('',
    url(r"^upload/$", PDFUploadView.as_view(), name="pdf_upload"),
    url(r"^edit/(?P<pk>\d+)/$", PDFUploadView.as_view(), name="pdf_upload"),
    url(r"^list/$", PDFListView.as_view(), name="pdf_list"),
    url(r"^view/(?P<pk>\d+)/(?P<page_num>\d*)/{0,1}$", PDF2HTMLView.as_view(), name="pdf_view"),
    url(r"^delete/(?P<pk>\d+)/$", delete_pdf, name="pdf_delete"),
    url(r"^download/(?P<pk>\d+)/$", download_pdf, name="pdf_download"),
)
