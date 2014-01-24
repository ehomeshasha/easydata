# -*- coding: utf-8 -*-  
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from easydata.constant import HOME_BREAD
from django.conf import settings
from easydata.func.function_core import elistdir

article_title_dict = {
    "hadoop_deployment": _("Hadoop 安装与部署"),
    "mahout_development": _("Mahout 二次开发"),
    "1_mahout_install": _("Mahout 安装"),
    "2_mahout_commands": _("Mahout命令执行过程的分析"),
    "3_mahout_arguments": _("Mahout参数获取"),
    "programming_collective_intelligence": _("集体智慧编程"),
}


context = {
    'SITE_URL': settings.SITE_URL,
    'MEDIA_URL' : settings.MEDIA_URL,
}


def get_indexlist_chapterdict(article_name):
    filelist_no_order =  elistdir('article/templates/article/%s/' % article_name, find_type='file')
    filelist_dict = {}
    index_list = []
    for f in filelist_no_order:
        index = int(f.split("_")[0])
        filelist_dict[index] = f
        index_list.append(index)
    index_list.sort()
    filelist = []
    for i in index_list:
        filelist.append(filelist_dict[i])
    
    return index_list, filelist_dict


def get_last_chapter(chapter_name, index_list, filelist_dict):
    
    now_index = int(chapter_name.split("_")[0])
    pos = index_list.index(now_index)
    if pos == 0:
        return ''
    former_index = index_list[pos-1]
    return filelist_dict[former_index]
    
def get_next_chapter(chapter_name, index_list, filelist_dict):
    
    now_index = int(chapter_name.split("_")[0])
    pos = index_list.index(now_index)
    if pos == len(index_list)-1:
        return ''
    later_index = index_list[pos+1]
    return filelist_dict[later_index]
    
    
def get_title_name(dirname, name=''):
    if name != '':
        return name
    return ' '.join([w.title() for w in dirname.split("_")])    


    
def article_view(request, **kwargs):
    article_name = kwargs['article_name']
    article_verbose_name = article_title_dict[article_name]
    
    if not 'chapter_name' in kwargs:
        context.update({
            'head_title_text': article_verbose_name,
            'breadcrumb': [
                HOME_BREAD,
                {'text': 'Article', 'href': '/article/'}, 
                {'text': article_verbose_name},
            ],
            'article_name' : article_name,
        })
        return render(request, 'article/%s.html' % article_name, context)
    else: 
        
        index_list, filelist_dict = get_indexlist_chapterdict(article_name)
        
        chapter_name = kwargs['chapter_name']
        
        chapter_verbose_name = article_title_dict[chapter_name]
        
        last_chapter = get_last_chapter(chapter_name, index_list, filelist_dict)[:-5]
        next_chapter = get_next_chapter(chapter_name, index_list, filelist_dict)[:-5]
        
        context.update({
            'head_title_text': chapter_verbose_name,
            'breadcrumb': [
                HOME_BREAD,
                {'text': 'Article', 'href': '/article/'}, 
                {'text': article_verbose_name, 'href': '/article/list/%s/' % article_name},
                {'text': chapter_verbose_name},
            ],
            'article_name' : article_name,
            'last_chapter': last_chapter,
            'next_chapter': next_chapter,
            'article_title_dict': article_title_dict
            #'chapter_name' : chapter_name,
        })
        
        return render(request, 'article/%s/%s.html' % (article_name, chapter_name), context)



def chapter_list(request, **kwargs):
    article_name = kwargs['article_name']
    article_verbose_name = article_title_dict[article_name]
    
    index_list, filelist_dict = get_indexlist_chapterdict(article_name)
    filelist = []
    for i in index_list:
        filelist.append(filelist_dict[i])
    
    
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
        'article_title_dict': article_title_dict,
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
    
    
    context.update({
        'head_title_text': 'Article List',
        'breadcrumb': [
            HOME_BREAD,
            {'text': 'Article'}, 
        ],
        'article_list': article_list,
    })
    return render(request, 'article/article_list.html', context)
    