from __future__ import unicode_literals
from django.conf.urls import patterns, url

from note.views import NoteListView, NoteView, NotePostView, delete_note

urlpatterns = patterns('',
    url(r"^view/(?P<pk>\d+)/$", NoteView.as_view(), name="note_view"),
    url(r"^list/$", NoteListView.as_view(), name="note_list"),
    url(r"^new/$", NotePostView.as_view(), name="note_new"),
    url(r"^edit/(?P<pk>\d+)/$", NotePostView.as_view(), name="note_edit"),
    url(r"^delete/(?P<pk>\d+)/$", delete_note, name="note_delete"),
    
)
