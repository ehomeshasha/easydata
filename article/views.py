# -*- coding: utf-8 -*-  
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from easydata.constant import HOME_BREAD
from django.conf import settings
from easydata.func.function_core import elistdir

context = {
    'SITE_URL': settings.SITE_URL
}

def get_title_name(dirname, name=''):
    if name != '':
        return name
    return ' '.join([w.title() for w in dirname.split("_")])    


    
def article_view(request, **kwargs):
    article_name = kwargs['article_name']
    chapter_name = kwargs['chapter_name']
    article_verbose_name = _(article_name.replace("_", " "))
    chapter_verbose_name = _(chapter_name.replace("_", " "))
    context.update({
        'head_title_text': chapter_verbose_name,
        'breadcrumb': [
            HOME_BREAD,
            {'text': 'Article', 'href': '/article/'}, 
            {'text': article_verbose_name, 'href': '/article/%s/' % article_name},
            {'text': chapter_verbose_name},
        ],
    })
    return render(request, 'article/%s/%s.html' % (article_name, chapter_name), context)



def chapter_list(request, **kwargs):
    article_name = kwargs['article_name']
    article_verbose_name = _(article_name.replace("_", " "))
    
    filelist =  elistdir('article/templates/article/%s/' % article_name, find_type='file')
    chapter_list = []
    for f in filelist:
        chapter_list.append({
            'filename': f[:-5],
            'chapter_name': get_title_name(f[:-5]),
        })
    
    context.update({
        'head_title_text': article_verbose_name,
        'breadcrumb': [
            HOME_BREAD,
            {'text': 'Article', 'href': '/article/'}, 
            {'text': article_verbose_name},
        ],
        'article_name': article_name,
        'chapter_list': chapter_list,
    })
    return render(request, 'article/chapter_list.html', context)
    

def article_list(request, **kwargs):
    
    
    dirnamelist =  elistdir('article/templates/article', find_type='directory')
    article_list = []
    for dirname in dirnamelist:
        article_list.append({
            'dirname': dirname,
            'article_name': get_title_name(dirname),
        })
    
    #print article_list
    
    context.update({
        'head_title_text': 'Article List',
        'breadcrumb': [
            HOME_BREAD,
            {'text': 'Article'}, 
        ],
        'article_list': article_list,
    })
    return render(request, 'article/article_list.html', context)
    