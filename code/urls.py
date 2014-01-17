from __future__ import unicode_literals
from django.conf.urls import patterns, url

from code.views import CodePostView, mark_post, mark_view_line, mark_delete, mark_about


urlpatterns = patterns('',
    url(r"^new/$", CodePostView.as_view(), name="code_post"),
    url(r"^edit/(?P<pk>\d+)/$", CodePostView.as_view(), name="code_post"),
    #url(r"^list/$", PDFListView.as_view(), name="pdf_list"),
    #url(r"^view/(?P<pk>\d+)/(?P<page_num>\d*)/{0,1}$", PDF2HTMLView.as_view(), name="pdf_view"),
    #url(r"^delete/(?P<pk>\d+)/$", delete_pdf, name="pdf_delete"),
    #url(r"^download/(?P<pk>\d+)/$", download_pdf, name="pdf_download"),
    #url(r"^mark/(?P<action>\w+)/(?P<pk>\d+)/(?P<page_num>\d+)/(?P<line_num>\d+)/$", mark_pdf, name="pdf_mark"),
    url(r"^mark_post/(?P<pk>\d+)/(?P<line_num>\d+)/$", mark_post, name="mark_post"),
    url(r"^mark_delete/(?P<pk>\d+)/$", mark_delete, name="mark_delete"),
    url(r"^mark_view_line/(?P<pk>\d+)/(?P<line_num>\d+)/$", mark_view_line, name="mark_view_line"),
    url(r"^mark_about/(?P<pk>\d+)/(?P<line_num>\d+)/$", mark_about, name="mark_about"),
    #url(r"^comment/(?P<pdf_id>\d+)/(?P<pk>\d*)/{0,1}$", PDFCommentView.as_view(), name="comment_post"),
)