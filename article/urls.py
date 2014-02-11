from __future__ import unicode_literals
from django.conf.urls import patterns, url

#from article.views import article_view, article_list, chapter_list
from article.views import ArticlePostView, ArticleView, ArticleIndexListView,\
    ArticleListView, ArticleIndexPostView, delete_article, delete_articleindex

urlpatterns = patterns('',
    url(r"^view/(?P<pk>\d+)/$", ArticleView.as_view(), name="article_view"),
    url(r"^list/$", ArticleListView.as_view(), name="article_list"),
    url(r"^new/$", ArticlePostView.as_view(), name="article_new"),
    url(r"^edit/(?P<pk>\d+)/$", ArticlePostView.as_view(), name="article_edit"),
    url(r"^delete/(?P<pk>\d+)/$", delete_article, name="article_delete"),
    
    #url(r"^indexview/(?P<pk>\d+)/$", ArticleIndexView.as_view(), name="articleindex_view"),
    url(r"^indexlist/$", ArticleIndexListView.as_view(), name="articleindex_list"),
    url(r"^indexnew/$", ArticleIndexPostView.as_view(), name="articleindex_new"),
    url(r"^indexedit/(?P<pk>\d+)/$", ArticleIndexPostView.as_view(), name="articleindex_edit"),
    url(r"^indexdelete/(?P<pk>\d+)/$", delete_articleindex, name="articleindex_delete"),
)
