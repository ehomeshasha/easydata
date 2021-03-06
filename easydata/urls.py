from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from easydata import uploads, views
from easydata.views import change_account_language, HomeView

urlpatterns = patterns("",
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r'^pdf/', include("pdf.urls")),
    url(r'^category/', include("easydata.category.urls")),
    url(r'^ajax_upload/$', uploads.ajax_upload),
    url(r'^article/', include("article.urls")),
    url(r'^code/', include("code.urls")),
    url(r'^note/', include("note.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^change_account_language/(?P<pk>\d+)/(?P<code>[-_\w]+)/$', change_account_language),
    url(r'^download_file/', views.download_file)
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
