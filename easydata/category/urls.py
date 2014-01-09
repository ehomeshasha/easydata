from __future__ import unicode_literals
from django.conf.urls import patterns, url

from easydata.category.views import CategoryPostView, CategoryListView, CategoryDelete



urlpatterns = patterns('',
    url(r"^new/$", CategoryPostView.as_view(), name="category_new"),
    url(r"^edit/(?P<pk>\d+)/$", CategoryPostView.as_view(), name="category_edit"),
    url(r"^delete/(?P<pk>\d+)/$", CategoryDelete, name="category_delete"),
    url(r"^$", CategoryListView.as_view(), name="category_list"),
)
