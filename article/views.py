# -*- coding: utf-8 -*-  
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from easydata.constant import HOME_BREAD
from django.conf import settings

context = {
    'SITE_URL': settings.SITE_URL
}

    
def article_view(request, **kwargs):
    article_name = kwargs['article_name']
    chapter_name = kwargs['chapter_name']
    article_verbose_name = _(article_name.replace("_", " "))
    context.update({
        'head_title_text': article_verbose_name,
        'breadcrumb': [HOME_BREAD,{'text': 'Article','href': '#'},{'text': article_verbose_name}],
    })
    return render(request, 'article/%s/%s.html' % (article_name, chapter_name), context)



