from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from easydata import uploads


urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r'^blog/', include("blog.urls")),
    url(r'^datafinder/', include("datafinder.urls")),
    url(r'^pdf/', include("pdf.urls")),
    url(r'bookshelf/', include("bookshelf.urls")),
    url(r'category/', include("easydata.category.urls")),
    url(r'ajax_upload/$', uploads.ajax_upload),
    url(r'^article/', include("article.urls")),
    url(r'^code/', include("code.urls")),
    #url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
