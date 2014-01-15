# -*- coding: utf-8 -*-  
from __future__ import unicode_literals

from django.shortcuts import render
from easydata.constant import HOME_BREAD



    
def programming_collective_intelligence(request, pk):
    context = {
        'head_title_text': 'programming collective intelligence',
        'breadcrumb': [HOME_BREAD,{'text': 'Article','href': '#'},{'text': 'programming collective intelligence'}],
    }
    return render(request, 'article/programming_collective_intelligence/%s.html' % pk, context)


def hadoop_deployment(request, pk):
    context = {
        'head_title_text': 'hadoop deployment',
        'breadcrumb': [HOME_BREAD,{'text': 'Article','href': '#'},{'text': 'hadoop deployment'}],
    }
    return render(request, 'article/hadoop_deployment/%s.html' % pk, context)

def mahout_basic(request, pk):
    context = {
        'head_title_text': 'mahout basic',
        'breadcrumb': [HOME_BREAD,{'text': 'Article','href': '#'},{'text': 'mahout basic'}],
    }
    return render(request, 'article/mahout_basic/%s.html' % pk, context)


